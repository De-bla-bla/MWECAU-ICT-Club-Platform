from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Count, Prefetch
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
import logging
from .models import Project, Event, Announcement, ContactMessage
from .rate_limiting import RateLimiter
from accounts.models import Department, CustomUser
from accounts.email_service import EmailService

logger = logging.getLogger(__name__)


@method_decorator(cache_page(60 * 5), name='dispatch')  # Cache for 5 minutes
class HomeView(TemplateView):
    """Home page with optimized queries and caching"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Use select_related and prefetch_related for optimization
        context['featured_projects'] = Project.objects.select_related(
            'department', 'leader'
        ).filter(featured=True)[:6]
        
        context['recent_events'] = Event.objects.select_related(
            'department'
        ).prefetch_related('attendees').order_by('-event_date')[:3]
        
        context['departments'] = Department.objects.select_related(
            'leader'
        ).prefetch_related(
            Prefetch(
                'members',
                queryset=CustomUser.objects.filter(is_approved=True)
            )
        ).all()
        
        context['announcements'] = Announcement.objects.select_related(
            'created_by', 'department'
        ).filter(published=True).order_by('-created_at')[:3]
        
        return context


@method_decorator(cache_page(60 * 10), name='dispatch')  # Cache for 10 minutes
class AboutView(TemplateView):
    """About ICT Club page"""
    template_name = 'core/about.html'


@method_decorator(cache_page(60 * 10), name='dispatch')  # Cache for 10 minutes
class FAQView(TemplateView):
    """FAQ page"""
    template_name = 'core/faq.html'


@method_decorator(cache_page(60 * 5), name='dispatch')  # Cache for 5 minutes
class DepartmentListView(ListView):
    """List all departments"""
    model = Department
    template_name = 'core/department_list.html'
    context_object_name = 'departments'
    paginate_by = 6
    
    def get_queryset(self):
        return Department.objects.select_related('leader').prefetch_related(
            Prefetch('members', queryset=CustomUser.objects.filter(is_approved=True))
        )


class DepartmentDetailView(DetailView):
    """Department detail page with optimized queries"""
    model = Department
    template_name = 'core/department_detail.html'
    context_object_name = 'department'
    slug_field = 'slug'
    
    def get_queryset(self):
        """Optimize query with select_related and prefetch_related"""
        return Department.objects.select_related('leader').prefetch_related(
            Prefetch(
                'members',
                queryset=CustomUser.objects.filter(is_approved=True)
            ),
            'projects',
            'events'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        
        # Use prefetch data to avoid additional queries
        context['members_count'] = department.members.filter(is_approved=True).count()
        context['projects'] = department.projects.select_related('leader').filter(
            featured=True
        )[:6]
        context['events'] = department.events.select_related('department').order_by(
            '-event_date'
        )[:5]
        
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')  # Cache for 5 minutes
class ProjectListView(ListView):
    """List all projects with optimized queries"""
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    
    def get_queryset(self):
        """Optimize with select_related and filter efficiently"""
        queryset = Project.objects.select_related(
            'department', 'leader'
        ).prefetch_related('members')
        
        department_slug = self.request.GET.get('department')
        if department_slug:
            queryset = queryset.filter(department__slug=department_slug)
        
        return queryset.order_by('-featured', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.values('id', 'name', 'slug').order_by('name')
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class ProjectDetailView(DetailView):
    """Project detail page"""
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'


@method_decorator(cache_page(60 * 5), name='dispatch')  # Cache for 5 minutes
class EventListView(ListView):
    """List all events"""
    model = Event
    template_name = 'core/event_list.html'
    context_object_name = 'events'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Event.objects.select_related('department')
        department_slug = self.request.GET.get('department')
        if department_slug:
            queryset = queryset.filter(department__slug=department_slug)
        return queryset.order_by('-event_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')  # Cache for 5 minutes
class AnnouncementListView(ListView):
    """List all announcements"""
    model = Announcement
    template_name = 'core/announcement_list.html'
    context_object_name = 'announcements'
    paginate_by = 10
    
    def get_queryset(self):
        return Announcement.objects.select_related('created_by', 'department').filter(
            published=True
        ).order_by('-created_at')


class ContactFormView(CreateView):
    """Contact form page with rate limiting to prevent spam"""
    model = ContactMessage
    template_name = 'core/contact.html'
    fields = ('name', 'email', 'phone', 'subject', 'message')
    success_url = reverse_lazy('core:home')
    
    def dispatch(self, request, *args, **kwargs):
        """Check rate limit before processing request"""
        # Allow 5 contact submissions per IP/user per hour
        if RateLimiter.is_rate_limited(request, 'contact_form', max_attempts=5, window_seconds=3600):
            logger.warning(f"Contact form spam attempt from {RateLimiter.get_client_identifier(request)}")
            messages.error(request, 'Too many contact form submissions. Please try again later.')
            return HttpResponseForbidden('Rate limit exceeded. Please try again later.')
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        try:
            # Send email notification using EmailService
            success, error = EmailService.send_contact_message_notification(form.instance)
            if success:
                logger.info(f"Contact form notification sent for message from {form.instance.email}")
            else:
                logger.warning(f"Failed to send contact notification: {error}")
        except Exception as e:
            logger.error(f"Exception sending contact notification: {str(e)}", exc_info=True)
        
        messages.success(self.request, 'Thank you! We have received your message and will respond shortly.')
        return response


@method_decorator(cache_page(60 * 10), name='dispatch')  # Cache for 10 minutes
class PrivacyPolicyView(TemplateView):
    """Privacy Policy page"""
    template_name = 'core/privacy_policy.html'


class TermsConditionsView(TemplateView):
    """Terms and Conditions page"""
    template_name = 'core/terms_conditions.html'


class LeadershipView(TemplateView):
    """Leadership and team structure page"""
    template_name = 'core/leadership.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You can add leadership data here
        # For now, this is a placeholder that can be expanded with actual team member data
        context['leadership_positions'] = [
            {
                'title': 'Chairperson',
                'icon': 'fas fa-crown',
                'color': 'warning',
                'description': 'Overall leadership and strategic direction of the club'
            },
            {
                'title': 'Vice Chairperson',
                'icon': 'fas fa-user-tie',
                'color': 'primary',
                'description': 'Assists the Chairperson and deputizes when needed'
            },
            {
                'title': 'Secretary',
                'icon': 'fas fa-file-alt',
                'color': 'info',
                'description': 'Records, communication, and administrative tasks'
            },
            {
                'title': 'Assistant Secretary',
                'icon': 'fas fa-clipboard',
                'color': 'secondary',
                'description': 'Assists the Secretary with administrative duties'
            },
            {
                'title': 'Product Manager',
                'icon': 'fas fa-project-diagram',
                'color': 'success',
                'description': 'Manages projects and technical initiatives'
            },
            {
                'title': 'Assistant Product Manager',
                'icon': 'fas fa-tasks',
                'color': 'secondary',
                'description': 'Assists with project management and coordination'
            },
        ]
        return context
