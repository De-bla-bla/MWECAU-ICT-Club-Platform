from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
import logging
from .models import Project, Event, Announcement, ContactMessage
from accounts.models import Department
from accounts.email_service import EmailService

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    """Home page"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_projects'] = Project.objects.filter(featured=True)[:6]
        context['recent_events'] = Event.objects.all()[:3]
        context['departments'] = Department.objects.all()
        context['announcements'] = Announcement.objects.filter(published=True)[:3]
        
        # Add member counts for each department (optimized single query)
        if self.request.user.is_authenticated:
            departments = Department.objects.all()
            for dept in departments:
                dept.approved_members_count = dept.members.filter(is_approved=True).count()
            context['dept_member_counts'] = {dept.name: dept.approved_members_count for dept in departments}
        
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
    """Department detail page"""
    model = Department
    template_name = 'core/department_detail.html'
    context_object_name = 'department'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        context['members_count'] = department.members.filter(is_approved=True).count()
        context['projects'] = department.projects.filter(featured=True)[:6]
        context['events'] = department.events.all()[:5]
        return context


class ProjectListView(ListView):
    """List all projects"""
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Project.objects.all()
        department_slug = self.request.GET.get('department')
        if department_slug:
            queryset = queryset.filter(department__slug=department_slug)
        return queryset.order_by('-featured', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
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
