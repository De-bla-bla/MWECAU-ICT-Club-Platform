from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomUserChangeForm, PictureUploadForm
from .models import CustomUser, Department
from .decorators import picture_required, approval_required, leadership_required, department_leader_required


class RegisterView(CreateView):
    """User registration view"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        # The form's save() method already set the username
        user.save()
        
        # Send notification emails
        self._send_registration_email(user)
        
        messages.success(
            self.request,
            'Registration successful! Please log in. Your account is pending approval from the club leadership.'
        )
        return redirect(self.success_url)
    
    def _send_registration_email(self, user):
        """Send registration confirmation to user, admin, and department leader"""
        context = {
            'user': user,
            'department': user.department,
        }
        
        # Email to user
        user_email_html = render_to_string('emails/registration_confirmation.html', context)
        send_mail(
            subject='Welcome to ICT Club - Account Pending Approval',
            message='Your account has been created and is pending approval.',
            from_email='mwecauictclub@gmail.com',
            recipient_list=[user.email],
            html_message=user_email_html,
            fail_silently=True,
        )
        
        # Email to admin (superusers)
        admin_emails = CustomUser.objects.filter(is_staff=True).values_list('email', flat=True)
        if admin_emails:
            admin_email_html = render_to_string('emails/new_registration_admin.html', context)
            send_mail(
                subject=f'New Registration: {user.full_name}',
                message=f'New member registration from {user.full_name}',
                from_email='mwecauictclub@gmail.com',
                recipient_list=list(admin_emails),
                html_message=admin_email_html,
                fail_silently=True,
            )
        
        # Email to department leader
        if user.department.leader:
            leader_email_html = render_to_string('emails/new_registration_leader.html', context)
            send_mail(
                subject=f'New {user.department.name} Member Registration',
                message=f'New member registration for {user.department.name}',
                from_email='mwecauictclub@gmail.com',
                recipient_list=[user.department.leader.email],
                html_message=leader_email_html,
                fail_silently=True,
            )


class LoginView(View):
    """Custom login view"""
    template_name = 'accounts/login.html'
    
    def get(self, request):
        """Display login form"""
        return render(request, self.template_name)
    
    def post(self, request):
        """Handle login form submission"""
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect unapproved users to pending approval page
            if not user.is_approved:
                return redirect('accounts:pending_approval')
            
            return redirect('accounts:member_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('accounts:login')


@login_required(login_url='login')
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required(login_url='login')
def pending_approval_view(request):
    """View for users pending approval"""
    user = request.user
    
    # If user is approved, redirect to dashboard
    if user.is_approved:
        return redirect('accounts:member_dashboard')
    
    # If user is inactive, logout
    if not user.is_active:
        logout(request)
        messages.error(request, 'Your account has been rejected.')
        return redirect('accounts:login')
    
    context = {
        'user': user,
        'department': user.department,
    }
    return render(request, 'accounts/pending_approval.html', context)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """View user profile"""
    model = CustomUser
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile_user'
    login_url = 'login'
    
    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update user profile"""
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile_detail')
    login_url = 'accounts:login'
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


@login_required(login_url='login')
@picture_required
def upload_picture(request):
    """Upload profile picture"""
    user = request.user
    
    if request.method == 'POST':
        form = PictureUploadForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.picture_uploaded_at = timezone.now()
            user.save()
            messages.success(request, 'Profile picture uploaded successfully!')
            return redirect('member_dashboard')
    else:
        form = PictureUploadForm(instance=user)
    
    context = {
        'form': form,
        'deadline': user.picture_upload_deadline(),
        'hours_remaining': user.time_until_picture_deadline(),
    }
    return render(request, 'accounts/upload_picture.html', context)


@login_required(login_url='login')
def member_dashboard(request):
    """Member dashboard"""
    user = request.user
    
    # Check approval status
    if not user.is_approved:
        messages.warning(request, 'Your account is pending approval. Please check your email for updates.')
        return render(request, 'accounts/pending_approval.html')
    
    # Check if picture is overdue
    if user.is_picture_overdue():
        return redirect('upload_picture')
    
    context = {
        'user': user,
        'department': user.department,
        'picture_uploaded': bool(user.picture),
        'time_until_deadline': user.time_until_picture_deadline(),
    }
    return render(request, 'accounts/member_dashboard.html', context)


@login_required(login_url='login')
def department_members(request):
    """View department members (for leaders)"""
    user = request.user
    
    if not user.is_department_leader and not user.is_staff:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('member_dashboard')
    
    if user.is_department_leader:
        members = user.led_department.members.all().order_by('-registered_at')
    else:
        members = CustomUser.objects.all().order_by('-registered_at')
    
    context = {
        'members': members,
        'pending_members': members.filter(is_approved=False),
    }
    return render(request, 'accounts/department_members.html', context)


@login_required(login_url='login')
@require_http_methods(['POST'])
def approve_member(request, pk):
    """Approve a member (for department leaders and admins)"""
    member = get_object_or_404(CustomUser, pk=pk)
    user = request.user
    
    # Check permissions
    if not (user.is_staff or (user.is_department_leader and member.department == user.led_department)):
        messages.error(request, 'You do not have permission to approve this member.')
        return redirect('department_members')
    
    if not member.is_approved:
        member.is_approved = True
        # Save with update_fields to trigger signal
        member.save(update_fields=['is_approved'])
        messages.success(request, f'{member.full_name} has been approved!')
    else:
        messages.info(request, f'{member.full_name} is already approved.')
    
    return redirect('department_members')


@login_required(login_url='login')
@require_http_methods(['POST'])
def reject_member(request, pk):
    """Reject a member (for department leaders and admins)"""
    member = get_object_or_404(CustomUser, pk=pk)
    user = request.user
    
    # Check permissions
    if not (user.is_staff or (user.is_department_leader and member.department == user.led_department)):
        messages.error(request, 'You do not have permission to reject this member.')
        return redirect('department_members')
    
    member.is_active = False
    member.save()
    
    # Send rejection email
    _send_rejection_email(member)
    messages.success(request, f'{member.full_name} has been rejected.')
    
    return redirect('department_members')


def _send_approval_email(user):
    """Send approval confirmation email"""
    context = {'user': user}
    email_html = render_to_string('emails/member_approved.html', context)
    send_mail(
        subject='Your ICT Club Account Has Been Approved!',
        message='Your account has been approved.',
        from_email='mwecauictclub@gmail.com',
        recipient_list=[user.email],
        html_message=email_html,
        fail_silently=True,
    )


def _send_rejection_email(user):
    """Send rejection email"""
    context = {'user': user}
    email_html = render_to_string('emails/member_rejected.html', context)
    send_mail(
        subject='ICT Club Registration - Status Update',
        message='Your registration has been reviewed.',
        from_email='mwecauictclub@gmail.com',
        recipient_list=[user.email],
        html_message=email_html,
        fail_silently=True,
    )
