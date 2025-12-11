"""
Caching utilities and decorators
"""
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from functools import wraps
import hashlib
import json


class CacheManager:
    """Manage cache operations"""
    
    # Cache key prefixes
    USER_PREFIX = 'user:'
    DEPARTMENT_PREFIX = 'department:'
    PROJECT_PREFIX = 'project:'
    EVENT_PREFIX = 'event:'
    ANNOUNCEMENT_PREFIX = 'announcement:'
    
    # Default cache timeouts (in seconds)
    DEFAULT_TIMEOUT = 300  # 5 minutes
    LONG_TIMEOUT = 3600  # 1 hour
    SHORT_TIMEOUT = 60  # 1 minute
    
    @classmethod
    def generate_key(cls, prefix, identifier):
        """Generate cache key"""
        return f'{prefix}{identifier}'
    
    @classmethod
    def get_user(cls, user_id):
        """Get user from cache"""
        key = cls.generate_key(cls.USER_PREFIX, user_id)
        return cache.get(key)
    
    @classmethod
    def set_user(cls, user_id, data, timeout=None):
        """Set user in cache"""
        key = cls.generate_key(cls.USER_PREFIX, user_id)
        cache.set(key, data, timeout or cls.DEFAULT_TIMEOUT)
    
    @classmethod
    def delete_user(cls, user_id):
        """Delete user from cache"""
        key = cls.generate_key(cls.USER_PREFIX, user_id)
        cache.delete(key)
    
    @classmethod
    def get_department(cls, dept_id):
        """Get department from cache"""
        key = cls.generate_key(cls.DEPARTMENT_PREFIX, dept_id)
        return cache.get(key)
    
    @classmethod
    def set_department(cls, dept_id, data, timeout=None):
        """Set department in cache"""
        key = cls.generate_key(cls.DEPARTMENT_PREFIX, dept_id)
        cache.set(key, data, timeout or cls.LONG_TIMEOUT)
    
    @classmethod
    def delete_department(cls, dept_id):
        """Delete department from cache"""
        key = cls.generate_key(cls.DEPARTMENT_PREFIX, dept_id)
        cache.delete(key)
    
    @classmethod
    def get_project(cls, project_id):
        """Get project from cache"""
        key = cls.generate_key(cls.PROJECT_PREFIX, project_id)
        return cache.get(key)
    
    @classmethod
    def set_project(cls, project_id, data, timeout=None):
        """Set project in cache"""
        key = cls.generate_key(cls.PROJECT_PREFIX, project_id)
        cache.set(key, data, timeout or cls.LONG_TIMEOUT)
    
    @classmethod
    def delete_project(cls, project_id):
        """Delete project from cache"""
        key = cls.generate_key(cls.PROJECT_PREFIX, project_id)
        cache.delete(key)
    
    @classmethod
    def clear_all(cls):
        """Clear all cache"""
        cache.clear()
    
    @classmethod
    def clear_user_cache(cls):
        """Clear all user cache entries"""
        cache.delete_pattern(f'{cls.USER_PREFIX}*')
    
    @classmethod
    def clear_department_cache(cls):
        """Clear all department cache entries"""
        cache.delete_pattern(f'{cls.DEPARTMENT_PREFIX}*')


def cache_result(timeout=300, key_prefix=''):
    """
    Decorator to cache function results
    
    Usage:
        @cache_result(timeout=600)
        def get_expensive_data(user_id):
            # expensive operation
            return data
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [key_prefix or func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f'{k}={v}' for k, v in kwargs.items())
            
            cache_key = ':'.join(key_parts)
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # If not in cache, call function
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            
            return result
        
        return wrapper
    
    return decorator


def cache_model(timeout=3600):
    """
    Decorator to cache model querysets
    
    Usage:
        @cache_model(timeout=3600)
        def get_active_users():
            return CustomUser.objects.filter(is_active=True)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f'model:{func.__name__}:{hash(str(args) + str(kwargs))}'
            
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            
            return result
        
        return wrapper
    
    return decorator


def invalidate_cache(*keys):
    """
    Decorator to invalidate cache after function execution
    
    Usage:
        @invalidate_cache('user:123', 'department:5')
        def update_user(user_id):
            # update operation
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for key in keys:
                cache.delete(key)
            return result
        
        return wrapper
    
    return decorator


class CacheStats:
    """Track cache statistics"""
    
    @staticmethod
    def get_cache_info():
        """Get cache information"""
        try:
            from django.core.cache import cache
            if hasattr(cache, 'get_stats'):
                return cache.get_stats()
        except Exception:
            pass
        
        return {
            'hits': 0,
            'misses': 0,
            'ratio': 0
        }
    
    @staticmethod
    def reset_stats():
        """Reset cache statistics"""
        try:
            from django.core.cache import cache
            if hasattr(cache, 'reset_stats'):
                cache.reset_stats()
        except Exception:
            pass
