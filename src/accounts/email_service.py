from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_registration_email(user, department):
    """Send registration confirmation email"""
    context = {'user': user, 'department': department}
    html_message = render_to_string('emails/registration_confirmation.html', context)
    
    try:
        send_mail(
            subject='Welcome to ICT Club - Account Pending Approval',
            message='Your account has been created.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending registration email: {e}")
        return False


def send_approval_email(user):
    """Send account approval email"""
    context = {'user': user}
    html_message = render_to_string('emails/member_approved.html', context)
    
    try:
        send_mail(
            subject='Your ICT Club Account Has Been Approved!',
            message='Congratulations! Your account has been approved.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending approval email: {e}")
        return False


def send_rejection_email(user):
    """Send account rejection email"""
    context = {'user': user}
    html_message = render_to_string('emails/member_rejected.html', context)
    
    try:
        send_mail(
            subject='ICT Club Registration - Status Update',
            message='Thank you for your interest in ICT Club.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending rejection email: {e}")
        return False


def send_picture_reminder_email(user):
    """Send picture upload reminder email"""
    deadline = user.picture_upload_deadline()
    context = {'user': user, 'deadline': deadline}
    html_message = render_to_string('emails/picture_reminder.html', context)
    
    try:
        send_mail(
            subject='Picture Upload Reminder - ICT Club',
            message='Please upload your profile picture.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending picture reminder email: {e}")
        return False


def send_announcement_email(announcement, recipients):
    """Send announcement to members"""
    context = {'announcement': announcement}
    html_message = render_to_string('emails/announcement.html', context)
    
    try:
        send_mail(
            subject=f'Announcement: {announcement.title}',
            message=announcement.content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=list(recipients),
            html_message=html_message,
            fail_silently=True,
        )
        return True
    except Exception as e:
        print(f"Error sending announcement email: {e}")
        return False
