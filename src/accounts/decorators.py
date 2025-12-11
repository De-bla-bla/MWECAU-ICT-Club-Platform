from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.utils import timezone


def picture_required(view_func):
    """
    Decorator to enforce profile picture upload within 72 hours.
    Redirects user to picture upload page if deadline is passed.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            # Only enforce for approved members
            if user.is_approved:
                if user.is_picture_overdue():
                    messages.warning(
                        request,
                        'Your profile picture upload deadline has passed. '
                        'Please upload a picture to continue.'
                    )
                    return redirect('accounts:upload_picture')
                elif user.registered_at:
                    time_left = user.time_until_picture_deadline()
                    if time_left and time_left.total_seconds() > 0:
                        hours_left = int(time_left.total_seconds() / 3600)
                        if hours_left <= 24 and not user.picture:
                            messages.info(
                                request,
                                f'You have {hours_left} hours left to upload your profile picture.'
                            )
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def approval_required(view_func):
    """
    Decorator to ensure user account is approved.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if not request.user.is_approved:
            messages.warning(
                request,
                'Your account is still pending approval. '
                'Please wait for admin or department leader approval.'
            )
            return redirect('accounts:pending_approval')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def leadership_required(view_func):
    """
    Decorator to restrict access to leadership (Admin, Katibu, Department Leader).
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if not request.user.is_leadership():
            messages.error(
                request,
                'You do not have permission to access this page.'
            )
            return redirect('core:home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def department_leader_required(view_func):
    """
    Decorator to restrict access to department leaders only.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if not request.user.is_department_leader and not request.user.is_staff:
            messages.error(
                request,
                'Only department leaders can access this page.'
            )
            return redirect('core:home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
