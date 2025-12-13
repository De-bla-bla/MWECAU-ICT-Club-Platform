from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pending-approval/', views.pending_approval_view, name='pending_approval'),
    
    # Profile Management
    path('profile/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.UserPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('upload-picture/', views.upload_picture, name='upload_picture'),
    
    # Member Dashboard
    path('dashboard/', views.member_dashboard, name='member_dashboard'),
    
    # Department Management (Leaders)
    path('department/members/', views.department_members, name='department_members'),
    path('members/<int:pk>/approve/', views.approve_member, name='approve_member'),
    path('members/<int:pk>/reject/', views.reject_member, name='reject_member'),
]
