from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView, PasswordChangeDoneView as DjangoPasswordChangeDoneView
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
import logging
from .forms import CustomUserCreationForm, CustomUserChangeForm, PictureUploadForm
from .models import CustomUser, Department
from .decorators import picture_required, approval_required, leadership_required, department_leader_required
from .email_service import EmailService

logger = logging.getLogger(__name__)


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
        """Send registration confirmation to user and notify staff/department leader"""
        context = {
            'user': user,
            'department': user.department,
        }
        
        try:
            # Email to user (staff notification is handled in email service)
            user_success, user_error = EmailService.send_registration_email(user, user.department)
            if user_success:
                logger.info(f"Registration confirmation sent to {user.email}")
            else:
                logger.warning(f"Failed to send registration email to {user.email}: {user_error}")
            
            # Email to department leader
            if user.department and user.department.leader:
                try:
                    leader_success, leader_error = EmailService.send_single_email(
                        subject=f'New {user.department.name} Member Registration',
                        recipient_email=user.department.leader.email,
                        html_template='emails/new_registration_leader.html',
                        context=context,
                        plain_message=f'New member registration for {user.department.name}',
                        fail_silently=True
                    )
                    if leader_success:
                        logger.info(f"Department leader notification sent to {user.department.leader.email}")
                    else:
                        logger.warning(f"Failed to send leader notification: {leader_error}")
                except Exception as e:
                    logger.error(f"Exception sending leader notification: {str(e)}", exc_info=True)
                    
        except Exception as e:
            logger.error(f"Exception in registration email sending: {str(e)}", exc_info=True)


class LoginView(View):
    """Custom login view"""
    template_name = 'accounts/login.html'
    
    def get(self, request):
        """Display login form"""
        return render(request, self.template_name)
    
    def post(self, request):
        """Handle login form submission"""
        username_or_email_or_reg = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate using custom backend (supports email, reg number, or username)
        user = authenticate(request, username=username_or_email_or_reg, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect unapproved users to pending approval page
            if not user.is_approved:
                return redirect('accounts:pending_approval')
            
            return redirect('accounts:member_dashboard')
        else:
            messages.error(request, 'Invalid registration number, email, or password.')
            return redirect('accounts:login')


@login_required(login_url='accounts:login')
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('core:home')


@login_required(login_url='accounts:login')
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
    login_url = 'accounts:login'
    
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


@login_required(login_url='accounts:login')
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
            return redirect('accounts:member_dashboard')
    else:
        form = PictureUploadForm(instance=user)
    
    context = {
        'form': form,
        'deadline': user.picture_upload_deadline(),
        'hours_remaining': user.time_until_picture_deadline(),
    }
    return render(request, 'accounts/upload_picture.html', context)


@login_required(login_url='accounts:login')
def member_dashboard(request):
    """Member dashboard"""
    user = request.user
    
    # Check approval status
    if not user.is_approved:
        messages.warning(request, 'Your account is pending approval. Please check your email for updates.')
        return render(request, 'accounts/pending_approval.html')
    
    # Check if picture is overdue
    if user.is_picture_overdue():
        return redirect('accounts:upload_picture')
    
    # Calculate readable time remaining
    time_delta = user.time_until_picture_deadline()
    if time_delta:
        total_seconds = int(time_delta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        time_display = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
    else:
        time_display = "No deadline"
    
    context = {
        'user': user,
        'department': user.department,
        'picture_uploaded': bool(user.picture),
        'time_until_deadline': user.time_until_picture_deadline(),
        'time_display': time_display,
    }
    return render(request, 'accounts/member_dashboard.html', context)


@login_required(login_url='accounts:login')
def department_members(request):
    """View department members (for leaders) with filtering and pagination"""
    user = request.user
    
    if not user.is_department_leader and not user.is_staff:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('accounts:member_dashboard')
    
    # Get members based on user role
    if user.is_staff:
        # Admins see all members
        members = CustomUser.objects.all().order_by('-registered_at')
    elif user.is_department_leader:
        # Department leaders see only their department members
        try:
            members = user.led_department.members.all().order_by('-registered_at')
        except Department.DoesNotExist:
            messages.error(request, 'You are not assigned as a leader to any department.')
            return redirect('accounts:member_dashboard')
    else:
        # Shouldn't reach here, but fallback to empty queryset
        members = CustomUser.objects.none()
    
    # Handle filtering before pagination
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'approved':
        members = members.filter(is_approved=True, is_active=True)
    elif filter_type == 'pending':
        members = members.filter(is_approved=False, is_active=True)
    elif filter_type == 'rejected':
        members = members.filter(is_active=False)
    
    # Count different statuses for display - count from correct source
    # For staff: count from all members; for dept leaders: count from their department only
    if user.is_staff:
        base_members = CustomUser.objects.all().order_by('-registered_at')
    else:
        base_members = members  # Use department members for leaders
    
    approved_count = base_members.filter(is_approved=True, is_active=True).count()
    pending_count = base_members.filter(is_approved=False, is_active=True).count()
    rejected_count = base_members.filter(is_active=False).count()
    
    # Add pagination - 50 members per page
    paginator = Paginator(members, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'members': page_obj.object_list,
        'filter_type': filter_type,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'accounts/department_members.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(['POST'])
def approve_member(request, pk):
    """Approve a member (for department leaders and admins)"""
    member = get_object_or_404(CustomUser, pk=pk)
    user = request.user
    
    # Check permissions
    has_permission = user.is_staff
    if user.is_department_leader:
        try:
            has_permission = member.department == user.led_department
        except Department.DoesNotExist:
            has_permission = False
    
    if not has_permission:
        messages.error(request, 'You do not have permission to approve this member.')
        return redirect('accounts:department_members')
    
    if not member.is_approved:
        member.is_approved = True
        # Save with update_fields to trigger signal
        member.save(update_fields=['is_approved'])
        messages.success(request, f'{member.full_name} has been approved!')
    else:
        messages.info(request, f'{member.full_name} is already approved.')
    
    return redirect('accounts:department_members')


@login_required(login_url='accounts:login')
@require_http_methods(['POST'])
def reject_member(request, pk):
    """Reject a member (for department leaders and admins)"""
    member = get_object_or_404(CustomUser, pk=pk)
    user = request.user
    
    # Check permissions
    has_permission = user.is_staff
    if user.is_department_leader:
        try:
            has_permission = member.department == user.led_department
        except Department.DoesNotExist:
            has_permission = False
    
    if not has_permission:
        messages.error(request, 'You do not have permission to reject this member.')
        return redirect('accounts:department_members')
    
    try:
        member.is_active = False
        member.save()
        
        # Send rejection email with error handling
        success, error = EmailService.send_rejection_email(member)
        if success:
            logger.info(f"Rejection email sent to {member.email} for user {member.full_name}")
        else:
            logger.warning(f"Failed to send rejection email to {member.email}: {error}")
        
        messages.success(request, f'{member.full_name} has been rejected.')
    except Exception as e:
        logger.error(f"Exception in reject_member: {str(e)}", exc_info=True)
        messages.error(request, 'An error occurred while rejecting the member.')
    
    return redirect('accounts:department_members')


class UserPasswordChangeView(LoginRequiredMixin, DjangoPasswordChangeView):
    """Change password view"""
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')
    login_url = 'accounts:login'


class UserPasswordChangeDoneView(LoginRequiredMixin, DjangoPasswordChangeDoneView):
    """Password change confirmation view"""
    template_name = 'accounts/password_change_done.html'
    login_url = 'accounts:login'
