"""
Logging utilities and configuration
"""
import logging
from django.conf import settings


def get_logger(name):
    """Get a logger instance"""
    return logging.getLogger(name)


class AuditLogger:
    """Audit logger for important user actions"""
    
    logger = logging.getLogger('audit')
    
    @classmethod
    def log_login(cls, user, ip_address=None):
        """Log user login"""
        message = f'User {user.full_name} ({user.email}) logged in'
        if ip_address:
            message += f' from {ip_address}'
        cls.logger.info(message)
    
    @classmethod
    def log_logout(cls, user):
        """Log user logout"""
        cls.logger.info(f'User {user.full_name} ({user.email}) logged out')
    
    @classmethod
    def log_registration(cls, user):
        """Log new user registration"""
        cls.logger.info(f'New user registered: {user.full_name} ({user.email})')
    
    @classmethod
    def log_profile_update(cls, user):
        """Log profile update"""
        cls.logger.info(f'User {user.full_name} ({user.email}) updated profile')
    
    @classmethod
    def log_approval(cls, user, approved_by):
        """Log user approval"""
        action = 'approved' if user.is_approved else 'rejected'
        cls.logger.info(
            f'User {user.full_name} ({user.email}) was {action} by {approved_by.full_name}'
        )
    
    @classmethod
    def log_picture_upload(cls, user):
        """Log picture upload"""
        cls.logger.info(f'User {user.full_name} ({user.email}) uploaded profile picture')
    
    @classmethod
    def log_permission_denied(cls, user, action, resource):
        """Log permission denied"""
        cls.logger.warning(
            f'Permission denied: User {user.full_name} attempted to {action} {resource}'
        )
    
    @classmethod
    def log_error(cls, message, exception=None):
        """Log error"""
        if exception:
            cls.logger.error(message, exc_info=True)
        else:
            cls.logger.error(message)


class PerformanceLogger:
    """Logger for performance monitoring"""
    
    logger = logging.getLogger('performance')
    
    @classmethod
    def log_slow_query(cls, query, duration, threshold=1.0):
        """Log slow database queries"""
        if duration > threshold:
            cls.logger.warning(f'Slow query detected ({duration:.2f}s): {query}')
    
    @classmethod
    def log_api_call(cls, endpoint, method, duration):
        """Log API calls"""
        cls.logger.debug(f'{method} {endpoint} - {duration:.2f}s')


class ActivityLogger:
    """Logger for general activities"""
    
    logger = logging.getLogger('activity')
    
    @classmethod
    def log_activity(cls, user, action, description):
        """Log user activity"""
        user_info = f'{user.full_name} ({user.email})' if user else 'System'
        cls.logger.info(f'{user_info} - {action}: {description}')


def configure_logging():
    """Configure logging for the application"""
    
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'level': 'INFO',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/app.log',
                'maxBytes': 1024 * 1024 * 10,  # 10MB
                'backupCount': 10,
                'formatter': 'verbose',
                'level': 'INFO',
            },
            'audit_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/audit.log',
                'maxBytes': 1024 * 1024 * 10,
                'backupCount': 10,
                'formatter': 'verbose',
                'level': 'INFO',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
            'audit': {
                'handlers': ['audit_file'],
                'level': 'INFO',
                'propagate': False,
            },
            'performance': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'activity': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }
    
    return logging_config
