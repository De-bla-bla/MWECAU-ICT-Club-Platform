"""
Settings and environment configuration utilities
"""
import os
from pathlib import Path


class SettingsHelper:
    """Helper functions for settings management"""
    
    @staticmethod
    def get_env_variable(var_name, default=None):
        """Get environment variable with optional default"""
        return os.environ.get(var_name, default)
    
    @staticmethod
    def get_env_bool(var_name, default=False):
        """Get environment variable as boolean"""
        value = os.environ.get(var_name, str(default))
        return value.lower() in ('true', '1', 'yes', 'on')
    
    @staticmethod
    def get_env_int(var_name, default=0):
        """Get environment variable as integer"""
        try:
            return int(os.environ.get(var_name, default))
        except ValueError:
            return default
    
    @staticmethod
    def get_env_list(var_name, default=None):
        """Get environment variable as list"""
        if default is None:
            default = []
        
        value = os.environ.get(var_name)
        if value:
            return [item.strip() for item in value.split(',')]
        return default


class SecuritySettings:
    """Security-related settings"""
    
    @staticmethod
    def get_secure_settings(debug=False):
        """Get security settings based on environment"""
        if debug:
            return {
                'SECURE_SSL_REDIRECT': False,
                'SECURE_HSTS_SECONDS': 0,
                'SESSION_COOKIE_SECURE': False,
                'CSRF_COOKIE_SECURE': False,
            }
        else:
            return {
                'SECURE_SSL_REDIRECT': True,
                'SECURE_HSTS_SECONDS': 31536000,
                'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
                'SECURE_HSTS_PRELOAD': True,
                'SESSION_COOKIE_SECURE': True,
                'CSRF_COOKIE_SECURE': True,
                'SECURE_CONTENT_TYPE_NOSNIFF': True,
                'SECURE_BROWSER_XSS_FILTER': True,
                'X_FRAME_OPTIONS': 'DENY',
            }


class DatabaseSettings:
    """Database configuration helpers"""
    
    @staticmethod
    def get_database_config(engine='sqlite'):
        """Get database configuration"""
        base_dir = Path(__file__).resolve().parent.parent
        
        if engine == 'sqlite':
            return {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': base_dir / 'db.sqlite3',
            }
        elif engine == 'postgresql':
            return {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': SettingsHelper.get_env_variable('DB_NAME', 'mwecau_ict'),
                'USER': SettingsHelper.get_env_variable('DB_USER', 'postgres'),
                'PASSWORD': SettingsHelper.get_env_variable('DB_PASSWORD', ''),
                'HOST': SettingsHelper.get_env_variable('DB_HOST', 'localhost'),
                'PORT': SettingsHelper.get_env_int('DB_PORT', 5432),
            }
        elif engine == 'mysql':
            return {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': SettingsHelper.get_env_variable('DB_NAME', 'mwecau_ict'),
                'USER': SettingsHelper.get_env_variable('DB_USER', 'root'),
                'PASSWORD': SettingsHelper.get_env_variable('DB_PASSWORD', ''),
                'HOST': SettingsHelper.get_env_variable('DB_HOST', 'localhost'),
                'PORT': SettingsHelper.get_env_int('DB_PORT', 3306),
            }


class CacheSettings:
    """Cache configuration helpers"""
    
    @staticmethod
    def get_cache_config(backend='locmem'):
        """Get cache configuration"""
        if backend == 'locmem':
            return {
                'default': {
                    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                    'LOCATION': 'unique-snowflake',
                }
            }
        elif backend == 'redis':
            return {
                'default': {
                    'BACKEND': 'django_redis.cache.RedisCache',
                    'LOCATION': SettingsHelper.get_env_variable('REDIS_URL', 'redis://127.0.0.1:6379/1'),
                    'OPTIONS': {
                        'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                    }
                }
            }


class EmailSettings:
    """Email configuration helpers"""
    
    @staticmethod
    def get_email_config(backend='smtp'):
        """Get email configuration"""
        if backend == 'console':
            return {
                'EMAIL_BACKEND': 'django.core.mail.backends.console.EmailBackend',
            }
        elif backend == 'file':
            return {
                'EMAIL_BACKEND': 'django.core.mail.backends.filebased.EmailBackend',
                'EMAIL_FILE_PATH': '/tmp/app-messages',
            }
        elif backend == 'smtp':
            return {
                'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
                'EMAIL_HOST': SettingsHelper.get_env_variable('EMAIL_HOST', 'smtp.gmail.com'),
                'EMAIL_PORT': SettingsHelper.get_env_int('EMAIL_PORT', 587),
                'EMAIL_USE_TLS': SettingsHelper.get_env_bool('EMAIL_USE_TLS', True),
                'EMAIL_HOST_USER': SettingsHelper.get_env_variable('EMAIL_HOST_USER', ''),
                'EMAIL_HOST_PASSWORD': SettingsHelper.get_env_variable('EMAIL_HOST_PASSWORD', ''),
            }
