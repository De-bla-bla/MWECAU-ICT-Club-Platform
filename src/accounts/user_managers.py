"""
User management and profile utilities
"""
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


class UserManager:
    """Manage user operations"""
    
    @staticmethod
    def approve_user(user, approved_by=None):
        """Approve a user"""
        from accounts.models import CustomUser
        
        user.is_approved = True
        user.picture_deadline = timezone.now() + timedelta(hours=72)
        user.save()
        
        return user
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        from accounts.models import CustomUser
        
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_by_reg_number(reg_number):
        """Get user by registration number"""
        from accounts.models import CustomUser
        
        try:
            return CustomUser.objects.get(reg_number=reg_number)
        except CustomUser.DoesNotExist:
            return None
    
    @staticmethod
    def count_pending_users():
        """Count pending approval users"""
        from accounts.models import CustomUser
        
        return CustomUser.objects.filter(is_approved=False).count()
    
    @staticmethod
    def count_active_users():
        """Count active users"""
        from accounts.models import CustomUser
        
        return CustomUser.objects.filter(
            is_approved=True,
            is_active=True
        ).count()


class ProfileManager:
    """Manage user profiles"""
    
    @staticmethod
    def update_profile(user, **kwargs):
        """Update user profile"""
        allowed_fields = [
            'full_name',
            'phone_number',
            'bio',
            'location',
            'website',
            'department',
            'course',
        ]
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(user, field, value)
        
        user.save()
        return user
    
    @staticmethod
    def get_profile_completion_percentage(user):
        """Calculate profile completion percentage"""
        fields = [
            'full_name',
            'email',
            'phone_number',
            'department',
            'course',
            'profile_picture',
        ]
        
        completed = sum(1 for field in fields if getattr(user, field, None))
        return int((completed / len(fields)) * 100)
    
    @staticmethod
    def is_profile_complete(user):
        """Check if profile is complete"""
        percentage = ProfileManager.get_profile_completion_percentage(user)
        return percentage >= 100


class RoleManager:
    """Manage user roles"""
    
    @staticmethod
    def make_department_leader(user, department):
        """Make user a department leader"""
        user.is_department_leader = True
        user.department = department
        user.save()
        return user
    
    @staticmethod
    def make_secretary(user):
        """Make user a secretary"""
        user.is_secretary = True
        user.save()
        return user
    
    @staticmethod
    def make_treasurer(user):
        """Make user a treasurer"""
        user.is_treasurer = True
        user.save()
        return user
    
    @staticmethod
    def remove_leadership_role(user):
        """Remove leadership role from user"""
        user.is_department_leader = False
        user.is_secretary = False
        user.is_treasurer = False
        user.save()
        return user
