"""
Custom authentication backend for ICT Club
Supports authentication using email, registration number, or username
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class EmailOrRegNumberBackend(ModelBackend):
    """
    Custom backend to authenticate users using email, registration number, or username
    Allows flexible login using any of these credentials
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Override authenticate to support email and registration number
        
        Args:
            request: HTTP request object
            username: Can be username, email, or registration number
            password: User's password
            
        Returns:
            User instance if authentication successful, None otherwise
        """
        if not username or not password:
            return None
        
        try:
            # Try to find user by email, registration number, or username (case-insensitive)
            user = User.objects.get(
                Q(email__iexact=username.strip()) |
                Q(reg_number__iexact=username.strip()) |
                Q(username__iexact=username.strip())
            )
        except User.DoesNotExist:
            # Run the default password hasher once to reduce timing
            # difference between existing and non-existing users
            User().set_password(password)
            logger.debug(f"Authentication failed: User not found with identifier '{username}'")
            return None
        except User.MultipleObjectsReturned:
            # This shouldn't happen with unique constraints, but handle it
            user = User.objects.filter(
                Q(email__iexact=username.strip()) |
                Q(reg_number__iexact=username.strip()) |
                Q(username__iexact=username.strip())
            ).first()
            if user is None:
                logger.warning(f"Multiple users found for identifier '{username}', none selected")
                return None
        
        # Check password and active status
        if user and user.check_password(password) and self.user_can_authenticate(user):
            logger.info(f"User '{user.username}' (ID: {user.id}) authenticated successfully")
            return user
        
        if user:
            logger.debug(f"Authentication failed for user '{username}': Invalid password or account inactive")
        
        return None
    
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
