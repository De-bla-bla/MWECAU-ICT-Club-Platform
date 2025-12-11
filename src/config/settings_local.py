"""
Settings overrides and environment-specific configuration
"""
import os
from pathlib import Path

# Get environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Local Settings
SHELL_PLUS_PRE_IMPORTS = [
    ('accounts.models', ['CustomUser', 'Department', 'Course']),
    ('core.models', ['Project', 'Event', 'Announcement', 'ContactMessage']),
    ('core.activity_log', ['ActivityLog']),
]

# Development overrides
if ENVIRONMENT == 'development':
    DEBUG = True
    LOGGING_LEVEL = 'DEBUG'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    SILENCED_SYSTEM_CHECKS = [
        'fields.W903',  # AutoField -> BigAutoField
    ]

# Production overrides
elif ENVIRONMENT == 'production':
    DEBUG = False
    LOGGING_LEVEL = 'INFO'
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Testing overrides
elif ENVIRONMENT == 'testing':
    DEBUG = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

# Feature Flags
FEATURES = {
    'enable_api': True,
    'enable_cloudinary': os.getenv('USE_CLOUDINARY', 'False') == 'True',
    'enable_payments': True,
    'enable_notifications': True,
    'enable_analytics': True,
    'maintenance_mode': False,
}

# Cache settings
if ENVIRONMENT == 'production':
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/1',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'mwecau-memcache',
        }
    }
