from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Count, Prefetch
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import logging
from .models import Project, Event, Announcement, ContactMessage
from accounts.models import Department, CustomUser
from accounts.email_service import EmailService

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    """Home page with optimized queries"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Use select_related and prefetch_related for optimization
        context['featured_projects'] = Project.objects.select_related(
            'department', 'leader'
        ).filter(featured=True)[:6]
        
        context['recent_events'] = Event.objects.select_related(
            'department'
        ).prefetch_related('attendees').order_by('-date')[:3]
        
        context['departments'] = Department.objects.select_related(
            'leader'
        ).prefetch_related(
            Prefetch(
                'members',
                queryset=CustomUser.objects.filter(is_approved=True)
            )
        ).all()
        
        context['announcements'] = Announcement.objects.select_related(
            'author', 'department'
        ).filter(published=True).order_by('-created_at')[:3]
        
        # Calculate department stats in one place
        if context['departments']:
            context['dept_stats'] = {
                dept.id: dept.members.filter(is_approved=True).count()
                for dept in context['departments']
            }
        
        return context


class AboutView(TemplateView):
    """About ICT Club page"""
    template_name = 'core/about.html'


class FAQView(TemplateView):
    """FAQ page"""
    template_name = 'core/faq.html'


class DepartmentListView(ListView):
    """List all departments"""
    model = Department
    template_name = 'core/department_list.html'
    context_object_name = 'departments'
    paginate_by = 6


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
            '-date'
        )[:5]
        
        return context


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


class ProjectDetailView(DetailView):
    """Project detail page"""
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'


class EventListView(ListView):
    """List all events"""
    model = Event
    template_name = 'core/event_list.html'
    context_object_name = 'events'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Event.objects.all()
        department_slug = self.request.GET.get('department')
        if department_slug:
            queryset = queryset.filter(department__slug=department_slug)
        return queryset.order_by('-event_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        return context


class AnnouncementListView(ListView):
    """List all announcements"""
    model = Announcement
    template_name = 'core/announcement_list.html'
    context_object_name = 'announcements'
    paginate_by = 10
    
    def get_queryset(self):
        return Announcement.objects.filter(published=True).order_by('-created_at')


class ContactFormView(CreateView):
    """Contact form page"""
    model = ContactMessage
    template_name = 'core/contact.html'
    fields = ('name', 'email', 'phone', 'subject', 'message')
    success_url = reverse_lazy('core:home')
    
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
