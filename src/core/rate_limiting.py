"""
Rate limiting utilities for protecting against spam and abuse
"""
from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Rate limiter for protecting endpoints from abuse
    Uses Django's cache framework for distributed rate limiting
    """
    
    @staticmethod
    def get_client_identifier(request) -> str:
        """
        Get unique identifier for client (user ID or IP address)
        
        Args:
            request: Django request object
            
        Returns:
            str: Unique client identifier
        """
        if request.user.is_authenticated:
            return f"user_{request.user.id}"
        else:
            # Get IP address, considering proxies
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return f"ip_{ip}"
    
    @staticmethod
    def is_rate_limited(request, action: str, max_attempts: int = 5, window_seconds: int = 3600) -> bool:
        """
        Check if client has exceeded rate limit for action
        
        Args:
            request: Django request object
            action: Action name (e.g., 'contact_form', 'register')
            max_attempts: Maximum attempts allowed in time window
            window_seconds: Time window in seconds
            
        Returns:
            bool: True if rate limited, False if allowed
        """
        client_id = RateLimiter.get_client_identifier(request)
        cache_key = f"rate_limit:{action}:{client_id}"
        
        # Get current count
        current_count = cache.get(cache_key, 0)
        
        if current_count >= max_attempts:
            logger.warning(f"Rate limit exceeded for {action} from {client_id}")
            return True
        
        # Increment counter
        cache.set(cache_key, current_count + 1, window_seconds)
        return False
    
    @staticmethod
    def reset_rate_limit(request, action: str) -> None:
        """
        Reset rate limit for client action
        
        Args:
            request: Django request object
            action: Action name
        """
        client_id = RateLimiter.get_client_identifier(request)
        cache_key = f"rate_limit:{action}:{client_id}"
        cache.delete(cache_key)
