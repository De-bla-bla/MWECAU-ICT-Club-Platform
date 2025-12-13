"""
Management command to create a test user
Usage: python manage.py create_test_user --email user@test.com --password test123 --dept "Programming"
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from accounts.models import Department

CustomUser = get_user_model()


class Command(BaseCommand):
    help = 'Create a test user for development'

    def add_arguments(self, parser):
        parser.add_argument('--email', required=True, help='User email address')
        parser.add_argument('--password', required=True, help='User password')
        parser.add_argument('--dept', required=True, help='Department name')
        parser.add_argument('--reg-number', default='TEST/2025/001', help='Registration number')
        parser.add_argument('--full-name', default='Test User', help='Full name')
        parser.add_argument('--is-staff', action='store_true', help='Make user admin/staff')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        dept_name = options['dept']
        reg_number = options['reg_number']
        full_name = options['full_name']
        is_staff = options['is_staff']

        # Check if user exists
        if CustomUser.objects.filter(email=email).exists():
            raise CommandError(f'User with email "{email}" already exists')

        # Get department
        try:
            department = Department.objects.get(name=dept_name)
        except Department.DoesNotExist:
            raise CommandError(f'Department "{dept_name}" does not exist')

        # Create user
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            reg_number=reg_number,
            full_name=full_name,
            department=department,
            is_staff=is_staff,
            is_superuser=is_staff,
            is_approved=True,
        )

        self.stdout.write(
            self.style.SUCCESS(f'✓ Created user: {user.email} (ID: {user.id})')
        )
        if is_staff:
            self.stdout.write(self.style.SUCCESS('  → User is marked as staff/admin'))
