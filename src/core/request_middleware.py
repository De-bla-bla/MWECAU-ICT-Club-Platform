"""
Request and response logging utilities
"""
import logging
import time
from functools import wraps
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLogger:
    """Log incoming HTTP requests"""
    
    @staticmethod
    def log_request(request):
        """Log request details"""
        logger.info(
            f'Request: {request.method} {request.path} '
            f'from {RequestLogger.get_client_ip(request)}'
        )
    
    @staticmethod
    def log_response(request, response, duration):
        """Log response details"""
        logger.info(
            f'Response: {request.method} {request.path} '
            f'{response.status_code} ({duration:.3f}s)'
        )
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RequestTracker:
    """Track requests with unique IDs"""
    
    @staticmethod
    def generate_request_id():
        """Generate unique request ID"""
        import uuid
        return str(uuid.uuid4())
    
    @staticmethod
    def add_request_id_to_response(response, request_id):
        """Add request ID header to response"""
        response['X-Request-ID'] = request_id
        return response


class RequestMetrics:
    """Collect request metrics"""
    
    def __init__(self):
        self.total_requests = 0
        self.total_errors = 0
        self.total_response_time = 0
    
    def record_request(self, status_code, response_time):
        """Record request metrics"""
        self.total_requests += 1
        self.total_response_time += response_time
        
        if status_code >= 400:
            self.total_errors += 1
    
    def get_average_response_time(self):
        """Get average response time"""
        if self.total_requests == 0:
            return 0
        return self.total_response_time / self.total_requests
    
    def get_error_rate(self):
        """Get error rate percentage"""
        if self.total_requests == 0:
            return 0
        return (self.total_errors / self.total_requests) * 100


class ResponseLogger:
    """Log response details"""
    
    @staticmethod
    def log_response_headers(response):
        """Log response headers"""
        logger.debug(f'Response headers: {dict(response.items())}')
    
    @staticmethod
    def log_response_body(response, max_length=1000):
        """Log response body (truncated)"""
        try:
            body = response.content.decode('utf-8')
            if len(body) > max_length:
                body = body[:max_length] + '...'
            logger.debug(f'Response body: {body}')
        except Exception as e:
            logger.debug(f'Could not decode response body: {str(e)}')


class ErrorLogger:
    """Log error responses"""
    
    @staticmethod
    def log_4xx_error(request, response):
        """Log client error (4xx)"""
        logger.warning(
            f'Client error {response.status_code}: {request.method} {request.path} '
            f'from {RequestLogger.get_client_ip(request)}'
        )
    
    @staticmethod
    def log_5xx_error(request, response):
        """Log server error (5xx)"""
        logger.error(
            f'Server error {response.status_code}: {request.method} {request.path}'
        )
    
    @staticmethod
    def log_exception(request, exception):
        """Log exception"""
        logger.error(
            f'Exception in {request.method} {request.path}: {str(exception)}',
            exc_info=True
        )


def log_view_execution(func):
    """Decorator to log view execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f'{func.__name__} executed in {duration:.3f}s')
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f'{func.__name__} failed after {duration:.3f}s: {str(e)}',
                exc_info=True
            )
            raise
    
    return wrapper


def log_database_query(func):
    """Decorator to log database queries"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        from django.db import connection, reset_queries
        from django.conf import settings
        
        if settings.DEBUG:
            reset_queries()
        
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        
        if settings.DEBUG:
            num_queries = len(connection.queries)
            logger.debug(
                f'{func.__name__}: {num_queries} queries in {duration:.3f}s'
            )
        
        return result
    
    return wrapper


class SlowQueryLogger:
    """Log slow database queries"""
    
    THRESHOLD = 1.0  # 1 second
    
    @staticmethod
    def check_slow_queries(request, duration):
        """Check if request took too long"""
        if duration > SlowQueryLogger.THRESHOLD:
            logger.warning(
                f'Slow request: {request.method} {request.path} '
                f'took {duration:.3f}s'
            )
