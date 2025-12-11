from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Project, Event, Announcement, ContactMessage
from accounts.models import Department


class HomeView(TemplateView):
    """Home page"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_projects'] = Project.objects.filter(featured=True)[:6]
        context['recent_events'] = Event.objects.all()[:3]
        context['departments'] = Department.objects.all()
        context['announcements'] = Announcement.objects.filter(published=True)[:3]
        return context


class AboutView(TemplateView):
    """About ICT Club page"""
    template_name = 'core/about.html'


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
        
        # Send email notification
        context = {'message': form.instance}
        email_html = render_to_string('emails/contact_message.html', context)
        try:
            send_mail(
                subject=f'New Contact Message: {form.instance.subject}',
                message='A new contact message has been received.',
                from_email='mwecauictclub@gmail.com',
                recipient_list=['mwecauictclub@gmail.com'],
                html_message=email_html,
                fail_silently=True,
            )
        except Exception:
            pass
        
        messages.success(self.request, 'Thank you! We have received your message and will respond shortly.')
        return response
