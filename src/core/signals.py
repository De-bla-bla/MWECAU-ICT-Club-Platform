"""
Signal handlers for model updates and automated tasks
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from accounts.models import CustomUser
from core.models import Project, Event, Announcement
from core.activity_log import ActivityLog


@receiver(post_save, sender=CustomUser)
def log_user_creation(sender, instance, created, **kwargs):
    """Log when a new user is created"""
    if created:
        ActivityLog.objects.create(
            user=instance,
            action='register',
            description=f'User {instance.full_name} registered'
        )


@receiver(post_save, sender=CustomUser)
def log_user_approval(sender, instance, created, update_fields=None, **kwargs):
    """Log when user approval status changes"""
    if not created and update_fields and 'is_approved' in update_fields:
        if instance.is_approved:
            ActivityLog.objects.create(
                user=instance,
                action='approve',
                description=f'User {instance.full_name} was approved'
            )


@receiver(post_save, sender=CustomUser)
def log_picture_upload(sender, instance, created, update_fields=None, **kwargs):
    """Log when user uploads profile picture"""
    if not created and update_fields and 'picture' in update_fields:
        if instance.picture:
            ActivityLog.objects.create(
                user=instance,
                action='picture_upload',
                description=f'User {instance.full_name} uploaded profile picture'
            )


@receiver(post_save, sender=Project)
def log_project_creation(sender, instance, created, **kwargs):
    """Log when a new project is created"""
    if created:
        ActivityLog.objects.create(
            user=instance.created_by,
            action='create',
            description=f'Project "{instance.title}" was created',
            object_id=instance.id,
            content_type='Project'
        )


@receiver(post_save, sender=Event)
def log_event_creation(sender, instance, created, **kwargs):
    """Log when a new event is created"""
    if created:
        ActivityLog.objects.create(
            user=None,
            action='create',
            description=f'Event "{instance.title}" was created',
            object_id=instance.id,
            content_type='Event'
        )


@receiver(post_save, sender=Announcement)
def log_announcement_creation(sender, instance, created, **kwargs):
    """Log when a new announcement is created"""
    if created:
        ActivityLog.objects.create(
            user=None,
            action='create',
            description=f'Announcement "{instance.title}" was published',
            object_id=instance.id,
            content_type='Announcement'
        )
