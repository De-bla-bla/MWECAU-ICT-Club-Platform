"""
Email service module for ICT Club
Provides robust email sending with error handling and logging
Supports both single and bulk email operations
"""
import logging
from typing import List, Dict, Tuple, Optional
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone

logger = logging.getLogger(__name__)


def get_staff_emails() -> List[str]:
    """
    Get email addresses of all superusers and staff members
    
    Returns:
        List[str]: List of email addresses
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Get all superusers and staff members
    staff_users = User.objects.filter(
        is_staff=True
    ).exclude(
        email__isnull=True
    ).exclude(
        email=''
    ).values_list('email', flat=True).distinct()
    
    return list(staff_users)


class EmailService:
    """
    Service class for handling email operations with comprehensive error handling
    Supports single emails, bulk emails, and HTML templates
    """
    
    DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER
    
    @classmethod
    def _validate_email_config(cls) -> bool:
        """
        Validate that email is properly configured
        
        Returns:
            bool: True if email config is valid
            
        Raises:
            ImproperlyConfigured: If email configuration is missing
        """
        if not settings.EMAIL_HOST:
            logger.error("EMAIL_HOST not configured")
            return False
        if not settings.EMAIL_HOST_USER:
            logger.error("EMAIL_HOST_USER not configured")
            return False
        if not settings.EMAIL_HOST_PASSWORD:
            logger.warning("EMAIL_HOST_PASSWORD not configured - emails may fail")
        return True
    
    @classmethod
    def send_single_email(
        cls,
        subject: str,
        recipient_email: str,
        html_template: str,
        context: Dict = None,
        plain_message: str = None,
        fail_silently: bool = False
    ) -> Tuple[bool, Optional[str]]:
        """
        Send a single email with HTML template support
        
        Args:
            subject: Email subject line
            recipient_email: Recipient's email address
            html_template: Path to HTML template (e.g., 'emails/registration_confirmation.html')
            context: Dictionary of template variables
            plain_message: Plain text fallback message
            fail_silently: Whether to suppress exceptions
            
        Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
        """
        if not cls._validate_email_config():
            error_msg = "Email service not properly configured"
            logger.error(error_msg)
            return False, error_msg
        
        try:
            if not recipient_email:
                error_msg = "Recipient email address is required"
                logger.error(error_msg)
                return False, error_msg
            
            # Render HTML template
            context = context or {}
            
            # Validate template path
            if not html_template:
                error_msg = "Email template path cannot be empty or None"
                logger.error(error_msg)
                if not fail_silently:
                    raise ValueError(error_msg)
                return False, error_msg
            
            try:
                html_message = render_to_string(html_template, context)
            except Exception as e:
                error_msg = f"Failed to render email template '{html_template}': {str(e)}"
                logger.error(error_msg)
                if not fail_silently:
                    raise
                return False, error_msg
            
            # Use plain text message as fallback if not provided
            if not plain_message:
                plain_message = f"Please view this email in an HTML-capable client. Subject: {subject}"
            
            # Send email
            sent = send_mail(
                subject=subject,
                message=plain_message,
                from_email=cls.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            if sent:
                logger.info(f"Email sent successfully to {recipient_email} - Subject: {subject}")
                return True, None
            else:
                error_msg = f"Failed to send email to {recipient_email}"
                logger.error(error_msg)
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Exception while sending email to {recipient_email}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            if not fail_silently:
                raise
            return False, error_msg
    
    @classmethod
    def send_bulk_emails(
        cls,
        subject: str,
        recipients: List[str],
        html_template: str,
        context_data: Dict = None,
        plain_message: str = None,
        fail_silently: bool = True,
        batch_size: int = 100
    ) -> Dict:
        """
        Send emails to multiple recipients with batch processing
        Useful for announcements, notifications to all members, etc.
        
        Args:
            subject: Email subject line
            recipients: List of email addresses
            html_template: Path to HTML template
            context_data: Dictionary of template variables (shared across all emails)
            plain_message: Plain text fallback message
            fail_silently: Whether to continue on individual email failures
            batch_size: Number of emails to send per batch (default 100)
            
        Returns:
            Dict: {
                'total': total recipients,
                'successful': number of successful sends,
                'failed': number of failed sends,
                'errors': list of error details
            }
        """
        if not cls._validate_email_config():
            error_msg = "Email service not properly configured"
            logger.error(error_msg)
            return {
                'total': len(recipients),
                'successful': 0,
                'failed': len(recipients),
                'errors': [error_msg]
            }
        
        results = {
            'total': len(recipients),
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        if not recipients:
            logger.warning("No recipients provided for bulk email send")
            return results
        
        # Remove duplicates and validate emails
        unique_recipients = list(set(recipients))
        valid_recipients = [email for email in unique_recipients if email and '@' in email]
        
        if len(valid_recipients) < len(unique_recipients):
            invalid_count = len(unique_recipients) - len(valid_recipients)
            logger.warning(f"Filtered out {invalid_count} invalid email addresses")
            results['errors'].append(f"Filtered out {invalid_count} invalid email addresses")
        
        results['total'] = len(valid_recipients)
        
        # Process in batches
        logger.info(f"Starting bulk email send to {len(valid_recipients)} recipients in batches of {batch_size}")
        
        for i in range(0, len(valid_recipients), batch_size):
            batch = valid_recipients[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            
            for recipient in batch:
                success, error = cls.send_single_email(
                    subject=subject,
                    recipient_email=recipient,
                    html_template=html_template,
                    context=context_data,
                    plain_message=plain_message,
                    fail_silently=fail_silently
                )
                
                if success:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                    if error:
                        results['errors'].append(f"{recipient}: {error}")
        
        logger.info(
            f"Bulk email send complete - Total: {results['total']}, "
            f"Successful: {results['successful']}, Failed: {results['failed']}"
        )
        
        return results
    
    @classmethod
    def send_registration_email(cls, user, department: Optional[object] = None) -> Tuple[bool, Optional[str]]:
        """
        Send registration confirmation email to new user and notify all staff members
        
        Args:
            user: User instance
            department: User's department
            
        Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
        """
        context = {
            'user': user,
            'department': department,
        }
        
        # Send confirmation email to user
        user_success, user_error = cls.send_single_email(
            subject='Welcome to ICT Club - Account Pending Approval',
            recipient_email=user.email,
            html_template='emails/registration_confirmation.html',
            context=context,
            plain_message='Your account has been created and is pending approval.',
            fail_silently=True
        )
        
        # Notify all staff members about the new registration
        staff_emails = get_staff_emails()
        if staff_emails:
            staff_context = {
                'user': user,
                'department': department,
                'registered_at': timezone.now(),
            }
            cls.send_admin_notification(
                admin_emails=staff_emails,
                subject=f'New Registration: {user.full_name}',
                html_template='emails/staff_new_registration.html',
                context=staff_context,
                plain_message=f'New member registration from {user.full_name}',
                fail_silently=True
            )
        
        return user_success, user_error
    
    @classmethod
    def send_approval_email(cls, user) -> Tuple[bool, Optional[str]]:
        """
        Send account approval email to user and notify staff
        
        Args:
            user: User instance that was approved
            
        Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
        """
        context = {'user': user}
        
        # Send approval email to user
        user_success, user_error = cls.send_single_email(
            subject='🎉 Your ICT Club Account Has Been Approved!',
            recipient_email=user.email,
            html_template='emails/member_approved.html',
            context=context,
            plain_message='Congratulations! Your account has been approved.',
            fail_silently=True
        )
        
        # Notify all staff members about the approval
        staff_emails = get_staff_emails()
        if staff_emails:
            approval_context = {
                'user': user,
                'approved_at': timezone.now(),
            }
            cls.send_admin_notification(
                admin_emails=staff_emails,
                subject=f'Member Approved: {user.full_name}',
                html_template='emails/staff_member_approved.html',
                context=approval_context,
                plain_message=f'Member {user.full_name} has been approved.',
                fail_silently=True
            )
        
        return user_success, user_error
    
    @classmethod
    def send_rejection_email(cls, user) -> Tuple[bool, Optional[str]]:
        """
        Send account rejection email to user and notify staff
        
        Args:
            user: User instance that was rejected
            
        Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
        """
        context = {'user': user}
        
        # Send rejection email to user
        user_success, user_error = cls.send_single_email(
            subject='ICT Club Registration - Status Update',
            recipient_email=user.email,
            html_template='emails/member_rejected.html',
            context=context,
            plain_message='Thank you for your interest in ICT Club.',
            fail_silently=True
        )
        
        # Notify all staff members about the rejection
        staff_emails = get_staff_emails()
        if staff_emails:
            rejection_context = {
                'user': user,
                'rejected_at': timezone.now(),
            }
            cls.send_admin_notification(
                admin_emails=staff_emails,
                subject=f'Member Rejected: {user.full_name}',
                html_template='emails/staff_member_rejected.html',
                context=rejection_context,
                plain_message=f'Member {user.full_name} has been rejected.',
                fail_silently=True
            )
        
        return user_success, user_error
    
    @classmethod
    def send_picture_reminder_email(cls, user) -> Tuple[bool, Optional[str]]:
        """
        Send picture upload reminder email
        
        Args:
            user: User instance
            
        Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
        """
        if not hasattr(user, 'picture_upload_deadline'):
            error_msg = "User object missing picture_upload_deadline method"
            logger.error(error_msg)
            return False, error_msg
        
        deadline = user.picture_upload_deadline()
        context = {
            'user': user,
            'deadline': deadline,
        }
        
        return cls.send_single_email(
            subject='Picture Upload Reminder - ICT Club',
            recipient_email=user.email,
            html_template='emails/picture_reminder.html',
            context=context,
            plain_message='Please upload your profile picture.',
            fail_silently=True
        )
    
    @classmethod
    def send_announcement_email(cls, announcement, recipients: List) -> Dict:
        """
        Send announcement to multiple members (bulk email)
        
        Args:
            announcement: Announcement object with title and content
            recipients: List of email addresses or user objects
            
        Returns:
            Dict: Bulk send results
        """
        # Convert user objects to email addresses if necessary
        recipient_emails = []
        for recipient in recipients:
            if isinstance(recipient, str):
                recipient_emails.append(recipient)
            elif hasattr(recipient, 'email'):
                recipient_emails.append(recipient.email)
        
        context = {'announcement': announcement}
        
        return cls.send_bulk_emails(
            subject=f'Announcement: {announcement.title}',
            recipients=recipient_emails,
            html_template='emails/announcement.html',
            context_data=context,
            plain_message=announcement.content,
            fail_silently=True,
            batch_size=100
        )
    
    @classmethod
    def send_contact_message_notification(cls, message_obj) -> Tuple[bool, Optional[str]]:
        """
        Send contact form submission notification to all staff members
        
        Args:
            message_obj: ContactMessage instance with name, email, subject, message
            
        Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
        """
        context = {'message': message_obj}
        
        # Send to all staff members
        staff_emails = get_staff_emails()
        if not staff_emails:
            # Fallback to default email if no staff members
            staff_emails = [settings.DEFAULT_FROM_EMAIL]
        
        results = cls.send_admin_notification(
            admin_emails=staff_emails,
            subject=f'New Contact Message: {message_obj.subject}',
            html_template='emails/contact_message.html',
            context=context,
            plain_message=f"New contact message from {message_obj.name}",
            fail_silently=True
        )
        
        success = results['failed'] == 0
        error = None if success else f"Failed to send to {results['failed']} staff members"
        return success, error
    
    @classmethod
    def send_admin_notification(
        cls,
        admin_emails: List[str],
        subject: str,
        html_template: str,
        context: Dict = None,
        plain_message: str = None
    ) -> Dict:
        """
        Send notification to all admin/staff members
        
        Args:
            admin_emails: List of admin email addresses
            subject: Email subject
            html_template: HTML template path
            context: Template context
            plain_message: Plain text message
            
        Returns:
            Dict: Bulk send results
        """
        return cls.send_bulk_emails(
            subject=subject,
            recipients=admin_emails,
            html_template=html_template,
            context_data=context,
            plain_message=plain_message,
            fail_silently=True,
            batch_size=50
        )


# Backward compatibility - standalone functions
def send_registration_email(user, department=None) -> bool:
    """Backward compatible wrapper for send_registration_email"""
    success, _ = EmailService.send_registration_email(user, department)
    return success


def send_approval_email(user) -> bool:
    """Backward compatible wrapper for send_approval_email"""
    success, _ = EmailService.send_approval_email(user)
    return success


def send_rejection_email(user) -> bool:
    """Backward compatible wrapper for send_rejection_email"""
    success, _ = EmailService.send_rejection_email(user)
    return success


def send_picture_reminder_email(user) -> bool:
    """Backward compatible wrapper for send_picture_reminder_email"""
    success, _ = EmailService.send_picture_reminder_email(user)
    return success


def send_announcement_email(announcement, recipients) -> bool:
    """Backward compatible wrapper for send_announcement_email"""
    results = EmailService.send_announcement_email(announcement, recipients)
    return results['failed'] == 0
