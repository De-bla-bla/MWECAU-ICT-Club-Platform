"""
Custom template tags for accounts app - user utilities
"""
from django import template

register = template.Library()


@register.filter
def first_name(user):
    """Get first name from full name"""
    if user and hasattr(user, 'full_name'):
        return user.full_name.split()[0] if user.full_name else 'User'
    return 'User'


@register.filter
def initials(user):
    """Get user initials from full name"""
    if user and hasattr(user, 'full_name') and user.full_name:
        parts = user.full_name.split()
        return ''.join(p[0].upper() for p in parts)[:2]
    return 'U'


@register.filter
def profile_complete(user):
    """Check if user profile is complete"""
    required_fields = ['full_name', 'phone', 'picture']
    return all(getattr(user, field, None) for field in required_fields)


@register.filter
def course_display(course):
    """Display course name with code"""
    if course:
        return f'{course.name} ({course.code})'
    return 'Not Assigned'


@register.filter
def department_display(department):
    """Display department name"""
    if department:
        return department.name
    return 'Not Assigned'
