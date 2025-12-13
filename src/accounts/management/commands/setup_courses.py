"""
Management command to set up courses
Usage: python manage.py setup_courses
"""
from django.core.management.base import BaseCommand
from accounts.models import Course


class Command(BaseCommand):
    help = 'Set up courses for the club'

    def handle(self, *args, **options):
        courses_data = [
            'Bachelor of Science in Computer Science',
            'Bachelor of Science in Information Technology',
            'Bachelor of Engineering in Software Engineering',
            'Diploma in Information Technology',
            'Certificate in Information Technology',
        ]

        for course_name in courses_data:
            course, created = Course.objects.get_or_create(
                name=course_name
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created course: {course.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'→ Course already exists: {course.name}')
                )

        self.stdout.write(self.style.SUCCESS('\n✓ Courses setup complete!'))
