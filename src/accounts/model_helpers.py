"""
User profile and model helper utilities
"""
from django.db.models import Q, QuerySet
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class UserProfileHelper:
    """Helper utilities for user profile management"""
    
    @staticmethod
    def is_profile_complete(user):
        """Check if user profile is complete"""
        required_fields = [
            'full_name',
            'email',
            'reg_number',
            'department',
            'course',
            'phone_number',
            'profile_picture'
        ]
        
        for field in required_fields:
            if not getattr(user, field, None):
                return False
        
        return True
    
    @staticmethod
    def get_profile_completion_percentage(user):
        """Get profile completion percentage"""
        fields = [
            'full_name',
            'email',
            'reg_number',
            'department',
            'course',
            'phone_number',
            'profile_picture',
            'bio',
            'location'
        ]
        
        completed = sum(1 for field in fields if getattr(user, field, None))
        return int((completed / len(fields)) * 100)
    
    @staticmethod
    def get_missing_profile_fields(user):
        """Get list of missing profile fields"""
        required_fields = {
            'full_name': 'Full Name',
            'email': 'Email',
            'reg_number': 'Registration Number',
            'department': 'Department',
            'course': 'Course',
            'phone_number': 'Phone Number',
            'profile_picture': 'Profile Picture'
        }
        
        missing = []
        for field, label in required_fields.items():
            if not getattr(user, field, None):
                missing.append(label)
        
        return missing
    
    @staticmethod
    def send_profile_completion_reminder(user):
        """Send reminder to complete profile"""
        from accounts.tasks import EmailTask
        
        # Check if profile is incomplete
        if UserProfileHelper.is_profile_complete(user):
            return False
        
        # Send reminder email
        missing_fields = UserProfileHelper.get_missing_profile_fields(user)
        
        logger.info(f'Sending profile completion reminder to {user.email}')
        # EmailTask.send_profile_reminder(user, missing_fields)
        
        return True


class UserStatusHelper:
    """Helper utilities for user status management"""
    
    @staticmethod
    def get_user_status(user):
        """Get current status of user"""
        if not user.is_approved:
            return 'pending'
        elif user.picture_deadline and user.picture_deadline < timezone.now():
            return 'picture_overdue'
        elif not user.is_active:
            return 'inactive'
        else:
            return 'active'
    
    @staticmethod
    def get_user_status_display(user):
        """Get user status display text"""
        status = UserStatusHelper.get_user_status(user)
        
        status_map = {
            'pending': 'Pending Approval',
            'picture_overdue': 'Picture Upload Overdue',
            'inactive': 'Inactive',
            'active': 'Active'
        }
        
        return status_map.get(status, 'Unknown')
    
    @staticmethod
    def get_picture_deadline_info(user):
        """Get information about picture deadline"""
        if not user.picture_deadline:
            return None
        
        now = timezone.now()
        deadline = user.picture_deadline
        
        if deadline < now:
            return {
                'status': 'overdue',
                'days': (now - deadline).days,
                'message': f'Picture upload is {(now - deadline).days} days overdue'
            }
        else:
            remaining = deadline - now
            return {
                'status': 'pending',
                'days': remaining.days,
                'message': f'{remaining.days} days remaining to upload picture'
            }
    
    @staticmethod
    def get_users_with_overdue_pictures():
        """Get all users with overdue picture uploads"""
        from accounts.models import CustomUser
        
        return CustomUser.objects.filter(
            is_approved=True,
            picture_deadline__lt=timezone.now(),
            profile_picture=''
        )
    
    @staticmethod
    def send_picture_reminder_to_all():
        """Send picture upload reminder to all users with overdue pictures"""
        from accounts.tasks import EmailTask
        
        users = UserStatusHelper.get_users_with_overdue_pictures()
        
        for user in users:
            logger.info(f'Sending picture reminder to {user.email}')
            # EmailTask.send_picture_reminder_email(user)


class UserRoleHelper:
    """Helper utilities for user roles and permissions"""
    
    @staticmethod
    def is_leadership(user):
        """Check if user is in leadership"""
        return user.is_department_leader or user.is_secretary or user.is_treasurer or user.is_admin
    
    @staticmethod
    def get_user_roles(user):
        """Get all roles for user"""
        roles = []
        
        if user.is_superuser:
            roles.append('Super Admin')
        if user.is_staff:
            roles.append('Staff')
        if user.is_department_leader:
            roles.append('Department Leader')
        if user.is_secretary:
            roles.append('Secretary')
        if user.is_treasurer:
            roles.append('Treasurer')
        if user.is_approved:
            roles.append('Approved Member')
        
        return roles or ['Member']
    
    @staticmethod
    def get_role_display(user):
        """Get display name for primary role"""
        if user.is_superuser:
            return 'Super Admin'
        elif user.is_department_leader:
            return 'Department Leader'
        elif user.is_secretary:
            return 'Secretary'
        elif user.is_treasurer:
            return 'Treasurer'
        elif user.is_approved:
            return 'Member'
        else:
            return 'Pending'
    
    @staticmethod
    def can_manage_users(user):
        """Check if user can manage other users"""
        return user.is_superuser or user.is_department_leader
    
    @staticmethod
    def can_create_content(user):
        """Check if user can create content"""
        return user.is_approved and user.is_active


class UserBulkOperations:
    """Bulk operations on users"""
    
    @staticmethod
    def approve_users(user_ids):
        """Approve multiple users"""
        from accounts.models import CustomUser
        
        users = CustomUser.objects.filter(id__in=user_ids)
        count = users.update(is_approved=True)
        
        # Set picture deadline for approved users
        for user in users:
            user.picture_deadline = timezone.now() + timedelta(hours=72)
            user.save()
        
        logger.info(f'Approved {count} users')
        return count
    
    @staticmethod
    def reject_users(user_ids):
        """Reject/delete multiple users"""
        from accounts.models import CustomUser
        
        users = CustomUser.objects.filter(id__in=user_ids)
        count, _ = users.delete()
        
        logger.info(f'Rejected {count} users')
        return count
    
    @staticmethod
    def deactivate_users(user_ids):
        """Deactivate multiple users"""
        from accounts.models import CustomUser
        
        count = CustomUser.objects.filter(id__in=user_ids).update(is_active=False)
        
        logger.info(f'Deactivated {count} users')
        return count
    
    @staticmethod
    def activate_users(user_ids):
        """Activate multiple users"""
        from accounts.models import CustomUser
        
        count = CustomUser.objects.filter(id__in=user_ids).update(is_active=True)
        
        logger.info(f'Activated {count} users')
        return count
    
    @staticmethod
    def add_to_department(user_ids, department):
        """Add multiple users to department"""
        from accounts.models import CustomUser
        
        count = CustomUser.objects.filter(id__in=user_ids).update(
            department=department
        )
        
        logger.info(f'Added {count} users to {department.name}')
        return count
    
    @staticmethod
    def remove_from_department(user_ids):
        """Remove multiple users from department"""
        from accounts.models import CustomUser
        
        count = CustomUser.objects.filter(id__in=user_ids).update(
            department=None
        )
        
        logger.info(f'Removed {count} users from departments')
        return count


class UserQueryHelper:
    """Helper utilities for user queries"""
    
    @staticmethod
    def get_active_users():
        """Get all active users"""
        from accounts.models import CustomUser
        
        return CustomUser.objects.filter(is_active=True, is_approved=True)
    
    @staticmethod
    def get_pending_users():
        """Get all pending approval users"""
        from accounts.models import CustomUser
        
        return CustomUser.objects.filter(is_approved=False)
    
    @staticmethod
    def get_inactive_users():
        """Get all inactive users"""
        from accounts.models import CustomUser
        
        return CustomUser.objects.filter(is_active=False)
    
    @staticmethod
    def get_users_by_department(department):
        """Get all users in a department"""
        from accounts.models import CustomUser
        
        return CustomUser.objects.filter(department=department, is_active=True)
    
    @staticmethod
    def get_leadership_users():
        """Get all leadership users"""
        from accounts.models import CustomUser
        
        return CustomUser.objects.filter(
            Q(is_department_leader=True) |
            Q(is_secretary=True) |
            Q(is_treasurer=True) |
            Q(is_superuser=True)
        )
    
    @staticmethod
    def search_users(query):
        """Search users by name or email"""
        from accounts.models import CustomUser
        
        return CustomUser.objects.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(reg_number__icontains=query)
        )
