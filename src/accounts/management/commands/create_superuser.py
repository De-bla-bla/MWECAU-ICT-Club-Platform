from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from accounts.models import CustomUser, Department, Course
import os
import sys


class Command(BaseCommand):
    help = 'Create a superuser with all required fields including department'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the superuser')
        parser.add_argument('--email', type=str, help='Email address for the superuser')
        parser.add_argument('--password', type=str, help='Password for the superuser')
        parser.add_argument('--reg-number', type=str, help='Registration number (e.g., T/DEG/2025/001)')
        parser.add_argument('--first-name', type=str, help='First name')
        parser.add_argument('--surname', type=str, help='Surname')
        parser.add_argument('--department', type=str, help='Department slug (e.g., programming)')
        parser.add_argument('--noinput', action='store_true', help='Run non-interactively')

    def handle(self, *args, **options):
        # Get existing departments
        departments = {dept.slug: dept for dept in Department.objects.all()}
        
        if not departments:
            self.stdout.write(
                self.style.ERROR('No departments found in database. Please create departments first.')
            )
            self.stdout.write(
                self.style.WARNING('Available departments: programming, cybersecurity, networking, maintenance, design, ai_ml')
            )
            sys.exit(1)

        # Non-interactive mode with command line arguments
        if options.get('noinput'):
            username = options.get('username')
            email = options.get('email')
            password = options.get('password')
            reg_number = options.get('reg_number')
            first_name = options.get('first_name')
            surname = options.get('surname')
            department_slug = options.get('department')

            # Validate all required fields
            missing_fields = []
            if not username:
                missing_fields.append('--username')
            if not email:
                missing_fields.append('--email')
            if not password:
                missing_fields.append('--password')
            if not reg_number:
                missing_fields.append('--reg-number')
            if not first_name:
                missing_fields.append('--first-name')
            if not surname:
                missing_fields.append('--surname')
            if not department_slug:
                missing_fields.append('--department')

            if missing_fields:
                raise CommandError(
                    f'Missing required arguments: {", ".join(missing_fields)}\n'
                    f'Available departments: {", ".join(departments.keys())}'
                )

            if department_slug not in departments:
                raise CommandError(
                    f'Department "{department_slug}" not found.\n'
                    f'Available departments: {", ".join(departments.keys())}'
                )

            self.create_superuser(
                username=username,
                email=email,
                password=password,
                reg_number=reg_number,
                first_name=first_name,
                surname=surname,
                department=departments[department_slug]
            )
        else:
            # Interactive mode
            self.stdout.write(self.style.SUCCESS('\n=== Superuser Creation ===\n'))
            
            # Get username
            while True:
                username = input('Username: ').strip()
                if not username:
                    self.stdout.write(self.style.WARNING('Username cannot be empty.'))
                    continue
                if CustomUser.objects.filter(username=username).exists():
                    self.stdout.write(self.style.WARNING('Username already exists.'))
                    continue
                break

            # Get email
            while True:
                email = input('Email address: ').strip()
                if not email:
                    self.stdout.write(self.style.WARNING('Email cannot be empty.'))
                    continue
                if CustomUser.objects.filter(email=email).exists():
                    self.stdout.write(self.style.WARNING('Email already exists.'))
                    continue
                break

            # Get first name
            while True:
                first_name = input('First name: ').strip()
                if not first_name:
                    self.stdout.write(self.style.WARNING('First name cannot be empty.'))
                    continue
                break

            # Get surname
            while True:
                surname = input('Surname: ').strip()
                if not surname:
                    self.stdout.write(self.style.WARNING('Surname cannot be empty.'))
                    continue
                break

            # Get registration number
            while True:
                reg_number = input('Registration number (e.g., T/DEG/2025/001): ').strip()
                if not reg_number:
                    self.stdout.write(self.style.WARNING('Registration number cannot be empty.'))
                    continue
                if CustomUser.objects.filter(reg_number=reg_number).exists():
                    self.stdout.write(self.style.WARNING('Registration number already exists.'))
                    continue
                # Validate format
                if not self.validate_reg_number(reg_number):
                    self.stdout.write(self.style.WARNING(
                        'Invalid format. Use T/XXXX/YYYY/NNNN (e.g., T/DEG/2025/001)'
                    ))
                    continue
                break

            # Get department
            self.stdout.write(f'\nAvailable departments:')
            for slug, dept in departments.items():
                self.stdout.write(f'  - {slug}: {dept.name}')
            
            while True:
                department_slug = input('\nDepartment (slug): ').strip()
                if not department_slug:
                    self.stdout.write(self.style.WARNING('Department cannot be empty.'))
                    continue
                if department_slug not in departments:
                    self.stdout.write(self.style.WARNING(
                        f'Department "{department_slug}" not found.'
                    ))
                    continue
                break

            # Get password
            while True:
                password = input('Password: ').strip()
                if not password:
                    self.stdout.write(self.style.WARNING('Password cannot be empty.'))
                    continue
                password_confirm = input('Password (again): ').strip()
                if password != password_confirm:
                    self.stdout.write(self.style.WARNING('Passwords do not match.'))
                    continue
                break

            self.create_superuser(
                username=username,
                email=email,
                password=password,
                reg_number=reg_number,
                first_name=first_name,
                surname=surname,
                department=departments[department_slug]
            )

    def validate_reg_number(self, reg_number):
        """Validate registration number format"""
        import re
        pattern = r'^T/(DEG|CERT|DIP|MASTER|PHD)/\d{4}/\d{3,4}$'
        return bool(re.match(pattern, reg_number))

    def create_superuser(self, username, email, password, reg_number, first_name, surname, department):
        """Create the superuser with all required fields"""
        try:
            with transaction.atomic():
                full_name = f"{first_name} {surname}".strip()
                
                user = CustomUser.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    reg_number=reg_number,
                    first_name=first_name,
                    surname=surname,
                    full_name=full_name,
                    department=department,
                    is_approved=True,  # Auto-approve admin
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\nSuperuser "{username}" created successfully!\n'
                        f'  Email: {email}\n'
                        f'  Reg Number: {reg_number}\n'
                        f'  Department: {department.name}\n'
                    )
                )
        except Exception as e:
            raise CommandError(f'Error creating superuser: {str(e)}')
