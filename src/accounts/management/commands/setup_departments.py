"""
Management command to set up departments
Usage: python manage.py setup_departments
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from accounts.models import Department


class Command(BaseCommand):
    help = 'Set up MWECAU ICT Club departments'

    def handle(self, *args, **options):
        departments_data = [
            {
                'name': 'Programming',
                'description': 'Software development in Python, JavaScript, PHP, and other languages.'
            },
            {
                'name': 'Cybersecurity',
                'description': 'Ethical hacking, digital forensics, information security, and secure computing.'
            },
            {
                'name': 'Networking',
                'description': 'Network design, implementation, and management for robust connectivity.'
            },
            {
                'name': 'Computer Maintenance',
                'description': 'Hardware and software troubleshooting, repair, and system optimization.'
            },
            {
                'name': 'Graphic Design',
                'description': 'Visual design and digital art using Adobe Creative Suite and Canva.'
            },
            {
                'name': 'AI & Machine Learning',
                'description': 'Artificial intelligence, machine learning, and intelligent data automation.'
            },
        ]

        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={
                    'slug': slugify(dept_data['name']),
                    'description': dept_data['description'],
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created department: {dept.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'→ Department already exists: {dept.name}')
                )

        self.stdout.write(self.style.SUCCESS('\n✓ Departments setup complete!'))
