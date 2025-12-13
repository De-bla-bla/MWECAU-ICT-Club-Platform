"""
Management command to create test users with proper registration format
Usage: python manage.py create_test_user --email user@test.com --password Test1234! --dept Programming --reg-number T/DEG/2025/001 --full-name "John Doe Smith"
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from accounts.models import Department, Course
from django.utils.timezone import now

CustomUser = get_user_model()


class Command(BaseCommand):
    help = 'Create test users for development with proper registration format'

    def add_arguments(self, parser):
        parser.add_argument('--email', required=True, help='User email address')
        parser.add_argument('--password', required=True, help='User password (8+ chars, upper, lower, digit, special)')
        parser.add_argument('--dept', required=True, help='Department name')
        parser.add_argument('--regnumber', required=True, help='Registration number (Format: T/XXXX/YYYY/NNNN)')
        parser.add_argument('--fullname', required=True, help='Full name (FirstName LastName Surname)')
        parser.add_argument('--course', default=None, help='Course name (optional)')
        parser.add_argument('--isstaff', action='store_true', help='Make user admin/staff')
        parser.add_argument('--approved', action='store_true', help='Mark user as approved')

    def handle(self, *args, **options):
        email = options['email'].lower()
        password = options['password']
        dept_name = options['dept']
        reg_number = options['regnumber'].upper()
        full_name = options['fullname']
        course_name = options.get('course')
        is_staff = options['isstaff']
        is_approved = options['approved']

        # Check if user exists
        if CustomUser.objects.filter(email=email).exists():
            raise CommandError(f'User with email "{email}" already exists')

        # Check registration number
        if CustomUser.objects.filter(reg_number__iexact=reg_number).exists():
            raise CommandError(f'Registration number "{reg_number}" already in use')

        # Get department
        try:
            department = Department.objects.get(name=dept_name)
        except Department.DoesNotExist:
            raise CommandError(f'Department "{dept_name}" does not exist. Available departments: {", ".join(Department.objects.values_list("name", flat=True))}')

        # Get course if provided
        course = None
        if course_name:
            try:
                course = Course.objects.get(name=course_name)
            except Course.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Course "{course_name}" does not exist, skipping course assignment')
                )

        # Generate username from registration number
        username = reg_number.upper()
        
        # Create user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            reg_number=reg_number,
            full_name=full_name,
            department=department,
            course=course,
            is_staff=is_staff,
            is_superuser=is_staff,
            is_approved=is_approved,
        )

        self.stdout.write(self.style.SUCCESS(f'\n✓ Test user created successfully!'))
        self.stdout.write(f'  Email: {user.email}')
        self.stdout.write(f'  Registration Number: {user.reg_number}')
        self.stdout.write(f'  Full Name: {user.full_name}')
        self.stdout.write(f'  Department: {user.department.name}')
        if course:
            self.stdout.write(f'  Course: {course.name}')
        self.stdout.write(f'  Approved: {"Yes" if is_approved else "No (Pending)"}')
        if is_staff:
            self.stdout.write(self.style.WARNING('  → User is marked as staff/admin'))
