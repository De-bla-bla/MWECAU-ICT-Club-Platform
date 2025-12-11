"""
Custom template tags for accounts app
"""
from django import template
from accounts.permissions import get_user_role

register = template.Library()


@register.filter
def user_role(user):
    """Get user role as a string"""
    return get_user_role(user)


@register.filter
def can_approve(user, target_user):
    """Check if user can approve target user"""
    from accounts.permissions import can_approve_member
    return can_approve_member(user, target_user)


@register.filter
def can_edit(editor, target_user):
    """Check if editor can edit target user"""
    from accounts.permissions import can_edit_user
    return can_edit_user(editor, target_user)


@register.filter
def has_department_permission(user, department):
    """Check if user has permission for department"""
    from accounts.permissions import has_department_permission
    return has_department_permission(user, department)


@register.filter
def is_picture_overdue(user):
    """Check if user's picture upload is overdue"""
    return user.is_picture_overdue()


@register.filter
def picture_deadline_color(user):
    """Get color class for picture deadline status"""
    if user.picture:
        return 'success'
    
    time_remaining = user.picture_upload_deadline()
    if not time_remaining:
        return 'danger'
    
    from django.utils import timezone
    time_left = (time_remaining - timezone.now()).total_seconds()
    
    if time_left <= 0:
        return 'danger'
    elif time_left <= 3600:  # 1 hour
        return 'warning'
    else:
        return 'info'


@register.filter
def format_deadline(deadline):
    """Format a deadline datetime"""
    from django.utils import timezone
    if not deadline:
        return 'No deadline'
    
    time_left = deadline - timezone.now()
    if time_left.total_seconds() <= 0:
        return 'Overdue'
    
    total_seconds = int(time_left.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    if hours > 24:
        days = hours // 24
        return f'{days}d remaining'
    elif hours > 0:
        return f'{hours}h {minutes}m remaining'
    else:
        return f'{minutes}m remaining'


@register.simple_tag
def user_status_badge(user):
    """Get HTML badge for user status"""
    from accounts.permissions import get_user_role
    role = get_user_role(user)
    
    if not user.is_active:
        return '<span class="badge bg-danger">Inactive</span>'
    elif not user.is_approved:
        return '<span class="badge bg-warning">Pending</span>'
    elif user.is_picture_overdue():
        return '<span class="badge bg-danger">Picture Overdue</span>'
    else:
        return '<span class="badge bg-success">Active</span>'


@register.simple_tag
def role_badge(user):
    """Get HTML badge for user role"""
    from accounts.permissions import user_role_display
    role = user_role_display(user)
    
    if user.is_superuser:
        return f'<span class="badge bg-danger">{role}</span>'
    elif user.is_staff:
        return f'<span class="badge bg-dark">{role}</span>'
    elif user.is_katibu:
        return f'<span class="badge bg-primary">{role}</span>'
    elif user.is_department_leader:
        return f'<span class="badge bg-info">{role}</span>'
    else:
        return f'<span class="badge bg-secondary">{role}</span>'
