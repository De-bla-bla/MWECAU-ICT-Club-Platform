from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Public pages
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/<slug:slug>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('announcements/', views.AnnouncementListView.as_view(), name='announcement_list'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-conditions/', views.TermsConditionsView.as_view(), name='terms_conditions'),
    path('leadership/', views.LeadershipView.as_view(), name='leadership'),
]
