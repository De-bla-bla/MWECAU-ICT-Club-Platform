"""
Management command to set up departments
Usage: python manage.py setup_departments
"""
from django.core.management.base import BaseCommand
from accounts.models import Department


class Command(BaseCommand):
    help = 'Set up default departments for ICT Club'

    def handle(self, *args, **options):
        departments_data = [
            {
                'name': 'Programming',
                'description': 'Software development in Python, JavaScript, PHP, etc.',
                'color': '#0066cc'
            },
            {
                'name': 'Cybersecurity',
                'description': 'Ethical hacking, digital forensics, and secure computing.',
                'color': '#cc0000'
            },
            {
                'name': 'Networking',
                'description': 'Design and implementation of robust networks.',
                'color': '#00cc00'
            },
            {
                'name': 'Computer Maintenance',
                'description': 'Hardware/software troubleshooting and repair.',
                'color': '#ffcc00'
            },
            {
                'name': 'Graphic Design',
                'description': 'Visual design using Adobe tools & Canva.',
                'color': '#00ccff'
            },
            {
                'name': 'AI & Machine Learning',
                'description': 'AI-driven automation and intelligent prototyping.',
                'color': '#9900cc'
            },
        ]

        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={
                    'description': dept_data['description'],
                    'color': dept_data['color']
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

        self.stdout.write(self.style.SUCCESS('\n✓ Department setup complete!'))
