"""
Custom validation utilities and validators
"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


class RegistrationNumberValidator:
    """Validate registration number format"""
    
    def __init__(self, pattern=r'^[A-Z]{2}\d{4,6}$'):
        self.pattern = pattern
    
    def __call__(self, value):
        if not re.match(self.pattern, value):
            raise ValidationError(
                _('Invalid registration number format. Expected format: 2 letters followed by 4-6 digits'),
                code='invalid'
            )


class PhoneValidator:
    """Validate phone number format"""
    
    def __init__(self, pattern=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'):
        self.pattern = pattern
    
    def __call__(self, value):
        if not re.match(self.pattern, value):
            raise ValidationError(
                _('Invalid phone number format'),
                code='invalid'
            )


def validate_image_size(file, max_size_mb=5):
    """Validate image file size"""
    file_size = file.size
    limit_bytes = max_size_mb * 1024 * 1024
    
    if file_size > limit_bytes:
        raise ValidationError(
            _(f'File size must not exceed {max_size_mb}MB. Current size: {file_size / (1024 * 1024):.2f}MB'),
            code='file_too_large'
        )


def validate_image_format(file, allowed_formats=None):
    """Validate image file format"""
    if allowed_formats is None:
        allowed_formats = ['JPEG', 'JPG', 'PNG', 'GIF', 'WEBP']
    
    # Get file extension
    ext = file.name.split('.')[-1].upper()
    
    if ext not in allowed_formats:
        raise ValidationError(
            _(f'Unsupported image format. Allowed formats: {", ".join(allowed_formats)}'),
            code='invalid_format'
        )


def validate_profile_completeness(user):
    """Validate if user profile is complete"""
    required_fields = {
        'full_name': 'Full Name',
        'phone': 'Phone Number',
        'department': 'Department',
        'course': 'Course',
    }
    
    missing_fields = []
    for field, label in required_fields.items():
        if not getattr(user, field, None):
            missing_fields.append(label)
    
    if missing_fields:
        raise ValidationError(
            _(f'Incomplete profile. Missing: {", ".join(missing_fields)}'),
            code='incomplete_profile'
        )


def validate_url(url):
    """Validate URL format"""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    if not re.match(pattern, url, re.IGNORECASE):
        raise ValidationError(
            _('Invalid URL format'),
            code='invalid_url'
        )


def validate_email_format(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError(
            _('Invalid email format'),
            code='invalid_email'
        )


def validate_username(username):
    """Validate username format"""
    if len(username) < 3:
        raise ValidationError(
            _('Username must be at least 3 characters long'),
            code='too_short'
        )
    
    if len(username) > 30:
        raise ValidationError(
            _('Username must not exceed 30 characters'),
            code='too_long'
        )
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValidationError(
            _('Username can only contain letters, numbers, underscores, and hyphens'),
            code='invalid_characters'
        )


def validate_strong_password(password):
    """Validate password strength"""
    errors = []
    
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long')
    
    if not re.search(r'[a-z]', password):
        errors.append('Password must contain at least one lowercase letter')
    
    if not re.search(r'[A-Z]', password):
        errors.append('Password must contain at least one uppercase letter')
    
    if not re.search(r'\d', password):
        errors.append('Password must contain at least one digit')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append('Password must contain at least one special character')
    
    if errors:
        raise ValidationError(errors)


def validate_no_duplicate_email(email, user=None):
    """Validate that email is not already in use"""
    from accounts.models import CustomUser
    
    queryset = CustomUser.objects.filter(email__iexact=email)
    
    if user:
        queryset = queryset.exclude(pk=user.pk)
    
    if queryset.exists():
        raise ValidationError(
            _('This email address is already in use'),
            code='duplicate_email'
        )


def validate_no_duplicate_registration(reg_number, user=None):
    """Validate that registration number is not already in use"""
    from accounts.models import CustomUser
    
    queryset = CustomUser.objects.filter(reg_number__iexact=reg_number)
    
    if user:
        queryset = queryset.exclude(pk=user.pk)
    
    if queryset.exists():
        raise ValidationError(
            _('This registration number is already in use'),
            code='duplicate_registration'
        )


class PasswordStrengthValidator:
    """Validate password strength"""
    
    def __init__(self, min_length=8):
        self.min_length = min_length
    
    def __call__(self, password):
        validate_strong_password(password)
    
    def get_help_text(self):
        return (
            f'Your password must contain at least {self.min_length} characters, '
            'including uppercase, lowercase, digits, and special characters.'
        )
