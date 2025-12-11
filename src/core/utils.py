"""
Utility functions for common operations
"""
from datetime import timedelta
from django.utils import timezone


def get_time_remaining(user):
    """Get time remaining for picture upload"""
    if user.picture:
        return None
    
    deadline = user.picture_upload_deadline()
    if not deadline:
        return None
    
    time_left = deadline - timezone.now()
    if time_left.total_seconds() <= 0:
        return None
    
    return time_left


def is_within_deadline(user):
    """Check if user is within picture upload deadline"""
    if user.picture:
        return True
    
    time_remaining = get_time_remaining(user)
    return time_remaining is not None and time_remaining.total_seconds() > 0


def format_time_remaining(time_delta):
    """Format timedelta to human readable string"""
    if not time_delta:
        return "No time remaining"
    
    total_seconds = int(time_delta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def get_user_status_badge(user):
    """Get status badge for user"""
    if not user.is_active:
        return 'danger', 'Inactive'
    elif not user.is_approved:
        return 'warning', 'Pending Approval'
    elif user.is_picture_overdue():
        return 'danger', 'Picture Overdue'
    else:
        return 'success', 'Active'


def get_payment_status_badge(payment):
    """Get status badge for payment"""
    status_colors = {
        'pending': 'warning',
        'processing': 'info',
        'success': 'success',
        'failed': 'danger',
        'cancelled': 'secondary',
    }
    return status_colors.get(payment.status, 'secondary'), payment.get_status_display()
