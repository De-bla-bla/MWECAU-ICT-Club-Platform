"""
Django signals for accounts app
- Send email when user account is approved
- Send email when user account is rejected
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_approval_notification(sender, instance, created, update_fields, **kwargs):
    """
    Signal to send approval email when user's is_approved field changes to True
    """
    # Only process update signals (not create)
    if created:
        return
    
    # Check if is_approved was just updated to True
    if update_fields and 'is_approved' in update_fields:
        if instance.is_approved:
            _send_approval_email(instance)
            # Set approved_at timestamp
            if not instance.approved_at:
                instance.approved_at = timezone.now()
                instance.save(update_fields=['approved_at'])


def _send_approval_email(user):
    """Send approval confirmation email to user"""
    context = {
        'user': user,
        'department': user.department,
    }
    
    email_html = render_to_string('emails/member_approved.html', context)
    send_mail(
        subject='🎉 Your ICT Club Account Has Been Approved!',
        message='Your account has been approved. Welcome to the ICT Club!',
        from_email='mwecauictclub@gmail.com',
        recipient_list=[user.email],
        html_message=email_html,
        fail_silently=True,
    )


def _send_rejection_email(user):
    """Send rejection email to user"""
    context = {
        'user': user,
        'department': user.department,
    }
    
    email_html = render_to_string('emails/member_rejected.html', context)
    send_mail(
        subject='ICT Club Registration - Status Update',
        message='Your registration has been reviewed.',
        from_email='mwecauictclub@gmail.com',
        recipient_list=[user.email],
        html_message=email_html,
        fail_silently=True,
    )
