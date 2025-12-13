"""
Custom validation utilities for registration
"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from datetime import datetime


def validate_registration_number(value):
    """
    Validate registration number format: T/XXXX/YYYY/NNNN
    Example: T/DEG/2025/001, T/CERT/2024/045, T/PHD/2025/1003
    Year must be between 2020 and current year (or next year if October+)
    """
    pattern = r'^T/(DEG|CERT|DIP|MASTER|PHD)/(\d{4})/(\d{3,4})$'
    match = re.match(pattern, value.upper())
    
    if not match:
        raise ValidationError(
            _('Invalid format. Use T/XXXX/YYYY/NNNN (e.g., T/DEG/2025/001)'),
            code='invalid_format'
        )
    
    level, year_str, number = match.groups()
    year = int(year_str)
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # Allow registration year range: last 5 years to current year
    min_year = current_year - 5
    max_year = current_year + 1 if current_month >= 10 else current_year
    
    if year < min_year or year > max_year:
        raise ValidationError(
            _(f'Year must be between {min_year} and {max_year}'),
            code='invalid_year'
        )


def validate_full_name(value):
    """
    Validate full name format: First Last Surname
    Must have at least 2 parts, only letters, spaces, and hyphens
    """
    # Remove extra spaces
    clean_name = ' '.join(value.split())
    
    # Check if has at least 2 parts
    parts = clean_name.split()
    if len(parts) < 2:
        raise ValidationError(
            _('Full name must have at least first name and last name'),
            code='invalid_name_format'
        )
    
    if len(parts) > 3:
        raise ValidationError(
            _('Full name should have at most 3 parts (first, last, surname)'),
            code='too_many_name_parts'
        )
    
    # Check for valid characters
    if not re.match(r"^[a-zA-Z\s\-']+$", value):
        raise ValidationError(
            _('Name can only contain letters, spaces, hyphens, and apostrophes'),
            code='invalid_characters'
        )


def validate_strong_password(value):
    """
    Validate password strength:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    if len(value) < 8:
        raise ValidationError(
            _('Password must be at least 8 characters long'),
            code='password_too_short'
        )
    
    if not re.search(r'[A-Z]', value):
        raise ValidationError(
            _('Password must contain at least one uppercase letter'),
            code='no_uppercase'
        )
    
    if not re.search(r'[a-z]', value):
        raise ValidationError(
            _('Password must contain at least one lowercase letter'),
            code='no_lowercase'
        )
    
    if not re.search(r'\d', value):
        raise ValidationError(
            _('Password must contain at least one digit'),
            code='no_digit'
        )
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:,.<>?]', value):
        raise ValidationError(
            _('Password must contain at least one special character (!@#$%^&*...)'),
            code='no_special_char'
        )
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
