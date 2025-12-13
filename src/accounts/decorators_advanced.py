"""
Utility decorators for common operations
"""
from functools import wraps
import time
import logging
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.http import cache_page

logger = logging.getLogger(__name__)


def timer(func):
    """Decorator to time function execution"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f'{func.__name__} took {duration:.3f}s')
        return result
    return wrapper


def log_exception(func):
    """Decorator to log exceptions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Exception in {func.__name__}: {str(e)}', exc_info=True)
            raise
    return wrapper


def cached_result(timeout=300):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f'{func.__name__}_{str(args)}_{str(kwargs)}'
            
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        
        return wrapper
    return decorator


def retry(max_attempts=3, delay=1):
    """Decorator to retry function on failure"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(
                        f'{func.__name__} attempt {attempt + 1} failed: {str(e)}'
                    )
                    time.sleep(delay)
        
        return wrapper
    return decorator


def require_http_method(*methods):
    """Decorator to require specific HTTP methods"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                from django.http import HttpResponseNotAllowed
                return HttpResponseNotAllowed(methods)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


class ObjectPermissionMixin:
    """Mixin for object-level permissions"""
    
    def has_object_permission(self, request, obj):
        """Override in subclass to implement object permissions"""
        return False
    
    def get_queryset(self):
        """Filter queryset based on permissions"""
        queryset = super().get_queryset()
        return [obj for obj in queryset if self.has_object_permission(self.request, obj)]
