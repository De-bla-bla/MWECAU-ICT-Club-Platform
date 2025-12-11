"""
Email utility functions for ICT Club
"""
from django.core.mail import send_mass_mail, send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_bulk_email(recipients_list, subject, template_name, context, html=True):
    """
    Send bulk emails to multiple recipients
    
    Args:
        recipients_list: List of email addresses
        subject: Email subject
        template_name: Template path (e.g., 'emails/notification.html')
        context: Context dictionary for template rendering
        html: Whether to use HTML email (default: True)
    
    Returns:
        Number of emails sent
    """
    if not recipients_list:
        return 0
    
    try:
        if html:
            message_html = render_to_string(template_name, context)
            send_mail(
                subject=subject,
                message='Please view this email in HTML format.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients_list,
                html_message=message_html,
                fail_silently=False,
            )
        else:
            message_text = render_to_string(template_name, context)
            send_mail(
                subject=subject,
                message=message_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients_list,
                fail_silently=False,
            )
        return len(recipients_list)
    except Exception as e:
        print(f"Error sending emails: {str(e)}")
        return 0


def send_notification_email(user_email, subject, template_name, context):
    """
    Send a single notification email
    
    Args:
        user_email: Recipient email address
        subject: Email subject
        template_name: Template path
        context: Context dictionary
    
    Returns:
        Boolean indicating success
    """
    try:
        message_html = render_to_string(template_name, context)
        send_mail(
            subject=subject,
            message='Please view this email in HTML format.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=message_html,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email to {user_email}: {str(e)}")
        return False


def send_to_leadership(subject, template_name, context):
    """
    Send email to all leadership (staff members)
    
    Args:
        subject: Email subject
        template_name: Template path
        context: Context dictionary
    
    Returns:
        Number of emails sent
    """
    from accounts.models import CustomUser
    
    leaders = CustomUser.objects.filter(
        is_staff=True
    ).values_list('email', flat=True)
    
    return send_bulk_email(
        list(leaders),
        subject,
        template_name,
        context
    )


def send_to_department_leaders(subject, template_name, context):
    """
    Send email to all department leaders
    
    Args:
        subject: Email subject
        template_name: Template path
        context: Context dictionary
    
    Returns:
        Number of emails sent
    """
    from accounts.models import CustomUser
    
    leaders = CustomUser.objects.filter(
        is_department_leader=True
    ).values_list('email', flat=True)
    
    return send_bulk_email(
        list(leaders),
        subject,
        template_name,
        context
    )
