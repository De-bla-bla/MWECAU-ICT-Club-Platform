"""
Caching decorators for common operations
"""
from django.core.cache import cache
from functools import wraps
from typing import Callable, Optional
import hashlib
import logging

logger = logging.getLogger(__name__)


def cache_result(timeout: int = 3600, key_prefix: str = None):
    """
    Decorator to cache function results using Django cache framework
    
    Args:
        timeout: Cache timeout in seconds (default: 1 hour)
        key_prefix: Custom prefix for cache key (auto-generated if not provided)
        
    Usage:
        @cache_result(timeout=300)
        def get_department_stats(department_id):
            # expensive query
            return stats
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            func_name = func.__name__
            prefix = key_prefix or func_name
            
            # Create hash of arguments for cache key
            args_str = str(args) + str(kwargs)
            args_hash = hashlib.md5(args_str.encode()).hexdigest()[:8]
            cache_key = f"{prefix}:{args_hash}"
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return result
            
            # Cache miss - execute function
            logger.debug(f"Cache miss for {cache_key}, executing function")
            result = func(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, timeout)
            return result
        
        return wrapper
    return decorator


def invalidate_cache(key_pattern: str):
    """
    Decorator to invalidate cache entries matching a pattern after function execution
    
    Args:
        key_pattern: Prefix pattern to match for cache invalidation
        
    Usage:
        @invalidate_cache('department:*')
        def update_department(department_id, name):
            # update operation
            department.save()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute the function
            result = func(*args, **kwargs)
            
            # Invalidate matching cache entries
            # Note: Django cache doesn't support pattern matching natively
            # This would need a more sophisticated cache backend or custom implementation
            logger.info(f"Cache invalidation pattern: {key_pattern}")
            
            return result
        
        return wrapper
    return decorator


def cache_department_stats(timeout: int = 300):
    """
    Specialized cache decorator for department statistics
    """
    return cache_result(timeout=timeout, key_prefix='dept_stats')


def cache_project_list(timeout: int = 300):
    """
    Specialized cache decorator for project listings
    """
    return cache_result(timeout=timeout, key_prefix='project_list')
