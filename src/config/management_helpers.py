"""
Django management command utilities and helpers
"""
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import logging

logger = logging.getLogger(__name__)


class BaseManagementCommand(BaseCommand):
    """Base class for custom management commands"""
    
    def add_arguments(self, parser):
        """Add common arguments"""
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Verbose output'
        )
    
    def success(self, message):
        """Print success message"""
        self.stdout.write(self.style.SUCCESS(message))
    
    def info(self, message):
        """Print info message"""
        self.stdout.write(self.style.NOTICE(message))
    
    def warning(self, message):
        """Print warning message"""
        self.stdout.write(self.style.WARNING(message))
    
    def error(self, message):
        """Print error message and exit"""
        self.stdout.write(self.style.ERROR(message))
        raise CommandError(message)


class CommandHelper:
    """Helper functions for management commands"""
    
    @staticmethod
    def get_model(app_label, model_name):
        """Get model by app and name"""
        try:
            return apps.get_model(app_label, model_name)
        except LookupError:
            raise CommandError(f'Model {app_label}.{model_name} not found')
    
    @staticmethod
    def confirm_action(message):
        """Confirm action with user"""
        response = input(f'{message} (yes/no): ').lower().strip()
        return response in ('yes', 'y')


class DataFixtures:
    """Create test/sample data"""
    
    @staticmethod
    def create_sample_departments():
        """Create sample departments"""
        from accounts.models import Department
        
        departments = [
            {'name': 'Programming', 'slug': 'programming'},
            {'name': 'Cybersecurity', 'slug': 'cybersecurity'},
            {'name': 'Web Development', 'slug': 'web-development'},
            {'name': 'Mobile Development', 'slug': 'mobile-development'},
        ]
        
        created = 0
        for dept_data in departments:
            dept, created_new = Department.objects.get_or_create(**dept_data)
            if created_new:
                created += 1
        
        return created
    
    @staticmethod
    def create_sample_courses():
        """Create sample courses"""
        from accounts.models import Course, Department
        
        courses = [
            {'name': 'Python Basics', 'code': 'PROG101', 'department': 'Programming'},
            {'name': 'JavaScript', 'code': 'PROG102', 'department': 'Programming'},
            {'name': 'Network Security', 'code': 'SEC101', 'department': 'Cybersecurity'},
            {'name': 'Web Security', 'code': 'SEC102', 'department': 'Cybersecurity'},
        ]
        
        created = 0
        for course_data in courses:
            dept = Department.objects.get(slug=course_data.pop('department'))
            course, created_new = Course.objects.get_or_create(
                **course_data,
                department=dept
            )
            if created_new:
                created += 1
        
        return created
