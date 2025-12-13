"""
Management command for sending bulk emails to members
Usage: python manage.py send_bulk_email --type=announcement --target=all_members
       python manage.py send_bulk_email --type=announcement --target=department --department=Programming
       python manage.py send_bulk_email --type=manual --recipients=email1@example.com,email2@example.com
"""
import logging
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from accounts.models import CustomUser, Department
from accounts.email_service import EmailService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send bulk emails to members with error handling and logging'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            required=True,
            choices=['announcement', 'manual'],
            help='Type of email to send'
        )
        
        parser.add_argument(
            '--target',
            type=str,
            choices=['all_members', 'approved_members', 'pending_members', 'department'],
            help='Target recipients for announcement type'
        )
        
        parser.add_argument(
            '--department',
            type=str,
            help='Department slug/name for department-specific emails'
        )
        
        parser.add_argument(
            '--recipients',
            type=str,
            help='Comma-separated list of email addresses for manual type'
        )
        
        parser.add_argument(
            '--subject',
            type=str,
            help='Email subject line'
        )
        
        parser.add_argument(
            '--template',
            type=str,
            help='Path to email template (e.g., emails/announcement.html)'
        )
        
        parser.add_argument(
            '--message',
            type=str,
            help='Plain text message for the email'
        )
    
    def handle(self, *args, **options):
        email_type = options.get('type')
        
        try:
            if email_type == 'announcement':
                self.handle_announcement(options)
            elif email_type == 'manual':
                self.handle_manual(options)
                
        except CommandError as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            logger.error(f"Command error: {str(e)}")
            raise
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {str(e)}'))
            logger.error(f"Unexpected error in send_bulk_email command: {str(e)}", exc_info=True)
            raise
    
    def handle_announcement(self, options):
        """Handle announcement email sending"""
        target = options.get('target')
        if not target:
            raise CommandError('--target is required for announcement type')
        
        subject = options.get('subject')
        if not subject:
            raise CommandError('--subject is required for announcement type')
        
        # Ensure template has a default value
        template = options.get('template') or 'emails/announcement.html'
        message = options.get('message', '')
        
        # Determine recipients based on target
        recipients = []
        if target == 'all_members':
            recipients = list(CustomUser.objects.filter(is_active=True).values_list('email', flat=True))
            self.stdout.write(f'Targeting all active members ({len(recipients)} recipients)')
            
        elif target == 'approved_members':
            recipients = list(CustomUser.objects.filter(is_approved=True, is_active=True).values_list('email', flat=True))
            self.stdout.write(f'Targeting approved members ({len(recipients)} recipients)')
            
        elif target == 'pending_members':
            recipients = list(CustomUser.objects.filter(is_approved=False, is_active=True).values_list('email', flat=True))
            self.stdout.write(f'Targeting pending members ({len(recipients)} recipients)')
            
        elif target == 'department':
            department_name = options.get('department')
            if not department_name:
                raise CommandError('--department is required when target is department')
            
            try:
                department = Department.objects.get(name__icontains=department_name)
                recipients = list(department.members.filter(is_active=True).values_list('email', flat=True))
                self.stdout.write(f'Targeting {department.name} members ({len(recipients)} recipients)')
            except Department.DoesNotExist:
                raise CommandError(f'Department "{department_name}" not found')
        
        if not recipients:
            raise CommandError('No recipients found for the specified target')
        
        # Send bulk emails
        context = {}
        results = EmailService.send_bulk_emails(
            subject=subject,
            recipients=recipients,
            html_template=template,
            context_data=context,
            plain_message=message,
            fail_silently=True,
            batch_size=100
        )
        
        self._print_results(results)
    
    def handle_manual(self, options):
        """Handle manual email sending to specific recipients"""
        recipients_str = options.get('recipients')
        if not recipients_str:
            raise CommandError('--recipients is required for manual type')
        
        subject = options.get('subject')
        if not subject:
            raise CommandError('--subject is required for manual type')
        
        # Ensure template has a default value
        template = options.get('template') or 'emails/announcement.html'
        message = options.get('message', '')
        
        # Parse recipients
        recipients = [email.strip() for email in recipients_str.split(',') if email.strip()]
        
        if not recipients:
            raise CommandError('No valid email addresses provided')
        
        self.stdout.write(f'Sending to {len(recipients)} specified recipients')
        
        # Send bulk emails
        results = EmailService.send_bulk_emails(
            subject=subject,
            recipients=recipients,
            html_template=template,
            context_data={},
            plain_message=message,
            fail_silently=True,
            batch_size=100
        )
        
        self._print_results(results)
    
    def _print_results(self, results):
        """Print bulk email results"""
        total = results['total']
        successful = results['successful']
        failed = results['failed']
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Bulk Email Send Complete'))
        self.stdout.write(f'Total Recipients: {total}')
        self.stdout.write(self.style.SUCCESS(f'Successful: {successful}'))
        
        if failed > 0:
            self.stdout.write(self.style.WARNING(f'Failed: {failed}'))
            if results['errors']:
                self.stdout.write('\nErrors:')
                for error in results['errors'][:10]:  # Show first 10 errors
                    self.stdout.write(f'  - {error}')
                if len(results['errors']) > 10:
                    self.stdout.write(f'  ... and {len(results["errors"]) - 10} more errors')
        else:
            self.stdout.write(self.style.SUCCESS('No errors!'))
        
        logger.info(f"Bulk email send completed - Total: {total}, Successful: {successful}, Failed: {failed}")
