"""
Custom Django middleware for security, caching, and request tracking
"""
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.core.cache import cache
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to all responses"""
    
    def process_response(self, request, response):
        """Add security headers"""
        # Prevent clickjacking
        response['X-Frame-Options'] = 'SAMEORIGIN'
        
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # HSTS (only in production)
        if not self.is_dev():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
    
    @staticmethod
    def is_dev():
        """Check if in development"""
        from django.conf import settings
        return settings.DEBUG


class RequestLoggingMiddleware(MiddlewareMixin):
    """Log all requests with timing information"""
    
    def process_request(self, request):
        """Log incoming request"""
        request._start_time = time.time()
        logger.info(f'Request: {request.method} {request.path}')
    
    def process_response(self, request, response):
        """Log response with timing"""
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
            
            logger.info(
                f'Response: {request.method} {request.path} '
                f'{response.status_code} {duration:.3f}s'
            )
            
            # Add timing header
            response['X-Response-Time'] = f'{duration:.3f}s'
        
        return response


class CacheControlMiddleware(MiddlewareMixin):
    """Add cache control headers based on response type"""
    
    def process_response(self, request, response):
        """Set cache control headers"""
        # Default no cache
        if 'Cache-Control' not in response:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        # Cache static assets for 1 year
        if self.is_static(request.path):
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
        
        # Cache API responses for 5 minutes
        elif self.is_api(request.path):
            response['Cache-Control'] = 'public, max-age=300'
        
        return response
    
    @staticmethod
    def is_static(path):
        """Check if path is static asset"""
        return path.startswith('/static/') or path.endswith(('.js', '.css', '.png', '.jpg', '.gif'))
    
    @staticmethod
    def is_api(path):
        """Check if path is API endpoint"""
        return path.startswith('/api/')


class ErrorHandlingMiddleware(MiddlewareMixin):
    """Catch and log exceptions"""
    
    def process_exception(self, request, exception):
        """Log exceptions"""
        logger.error(
            f'Exception in {request.method} {request.path}: {str(exception)}',
            exc_info=True
        )
        
        # Log to file for debugging
        self.log_error_details(request, exception)
    
    @staticmethod
    def log_error_details(request, exception):
        """Log detailed error information"""
        error_logger = logging.getLogger('error_details')
        
        error_logger.error(
            f'Method: {request.method}\n'
            f'Path: {request.path}\n'
            f'User: {request.user}\n'
            f'IP: {request.META.get("REMOTE_ADDR")}\n'
            f'Exception: {str(exception)}',
            exc_info=True
        )


class RateLimitMiddleware(MiddlewareMixin):
    """Simple rate limiting middleware"""
    
    LIMIT = 100  # requests per minute
    WINDOW = 60  # seconds
    
    def process_request(self, request):
        """Check rate limit"""
        if request.user.is_authenticated:
            identifier = f'user_{request.user.id}'
        else:
            identifier = f'ip_{self.get_client_ip(request)}'
        
        cache_key = f'rate_limit_{identifier}'
        
        # Get current count
        current = cache.get(cache_key, 0)
        
        if current >= self.LIMIT:
            return HttpResponse('Rate limit exceeded', status=429)
        
        # Increment counter
        cache.set(cache_key, current + 1, self.WINDOW)
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RequestContextMiddleware(MiddlewareMixin):
    """Add useful information to request context"""
    
    def process_request(self, request):
        """Add context to request"""
        # Store client IP
        request.client_ip = self.get_client_ip(request)
        
        # Store request start time
        request.request_start = time.time()
        
        # Store request ID for tracking
        import uuid
        request.request_id = str(uuid.uuid4())
        
        # Add custom user info
        if request.user.is_authenticated:
            request.user_dept = getattr(request.user, 'department', None)
            request.is_leader = getattr(request.user, 'is_department_leader', False)
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """Monitor and log slow requests"""
    
    SLOW_REQUEST_THRESHOLD = 1.0  # 1 second
    
    def process_request(self, request):
        """Mark request start time"""
        request._perf_start = time.time()
    
    def process_response(self, request, response):
        """Check if request was slow"""
        if hasattr(request, '_perf_start'):
            duration = time.time() - request._perf_start
            
            if duration > self.SLOW_REQUEST_THRESHOLD:
                logger.warning(
                    f'Slow request: {request.method} {request.path} '
                    f'took {duration:.3f}s'
                )
        
        return response


class AuditLoggingMiddleware(MiddlewareMixin):
    """Log sensitive operations for audit trail"""
    
    SENSITIVE_METHODS = ['POST', 'PUT', 'DELETE', 'PATCH']
    SENSITIVE_PATHS = [
        '/approve/',
        '/reject/',
        '/delete/',
        '/admin/',
        '/api/'
    ]
    
    def process_request(self, request):
        """Log sensitive operations"""
        if request.method in self.SENSITIVE_METHODS:
            if any(request.path.startswith(path) for path in self.SENSITIVE_PATHS):
                self.log_audit(request)
    
    @staticmethod
    def log_audit(request):
        """Log audit information"""
        audit_logger = logging.getLogger('audit')
        
        user = request.user.get_full_name() if request.user.is_authenticated else 'Anonymous'
        
        audit_logger.info(
            f'AUDIT: {request.method} {request.path} '
            f'by {user} from {request.META.get("REMOTE_ADDR")}'
        )


def cache_page_if_not_authenticated(timeout=300):
    """Decorator to cache page only for anonymous users"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            
            # Check cache
            cache_key = f'page_{request.path}'
            cached = cache.get(cache_key)
            
            if cached:
                return cached
            
            # Get response
            response = view_func(request, *args, **kwargs)
            
            # Cache it
            cache.set(cache_key, response, timeout)
            
            return response
        
        return wrapper
    
    return decorator
