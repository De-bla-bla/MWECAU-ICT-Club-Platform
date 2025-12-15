"""
Management command to set up Mwenge University IT-related courses
Usage: python manage.py setup_courses
Source: Mwenge Catholic University official programs
"""
from django.core.management.base import BaseCommand
from accounts.models import Course


class Command(BaseCommand):
    help = 'Set up Mwenge University IT-related courses'

    def handle(self, *args, **options):
        # Mwenge University IT-related and Education courses from official programs
        # Only including Computer Science, IT and Education-related fields
        courses_data = [
            # DEGREE Level Courses (Undergraduate - 3 years)
            # From Undergraduate Programs
            ('Bachelor of Science in Computer Science', 'DEG', 'MW009'),
            ('Bachelor of Science with Education', 'DEG', 'MW002'),
            ('Bachelor of Arts with Education', 'DEG', 'MW001'),
            
            # MASTER Level Courses (Postgraduate - 2 years)
            # Master of Science with Education could be IT Education focus
            ('Master of Science with Education', 'MASTER', 'MWM07'),
            ('Master of Business Administration', 'MASTER', 'MWM06'),
            ('Master of Education in Assessment and Evaluation', 'MASTER', 'MWM02'),
            ('Master of Education in Assessment and Evaluation -Weekend', 'MASTER', 'MWM02W'),
            ('Master of Education in Curriculum and Instruction', 'MASTER', 'MWM03'),
            ('Master of Education in Curriculum and Instruction -Weekend', 'MASTER', 'MWM03W'),
            ('Master of Education in Educational Planning and Administration', 'MASTER', 'MWM04'),
            ('Master of Education in Educational Planning and Administration- Weekend', 'MASTER', 'MWM04W'),
            
            # PHD Level Courses (3 years)
            ('Doctor of Philosophy in Education', 'PHD', 'MWPH01'),
        ]

        created_count = 0
        existing_count = 0

        self.stdout.write(self.style.WARNING(
            '\n⚠ Note: Setting up Mwenge University IT and Education programs.'
        ))
        self.stdout.write(self.style.WARNING(
            '  - Primary IT program: Bachelor of Science in Computer Science (MW009)'
        ))
        self.stdout.write(self.style.WARNING(
            '  - Education programs: Bachelor of Education, Master of Education, PhD Education'
        ))
        self.stdout.write(self.style.WARNING(
            '  - MBA: Master of Business Administration\n'
        ))

        for course_name, level, code in courses_data:
            course, created = Course.objects.get_or_create(
                name=course_name,
                defaults={'level': level, 'code': code}
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {course_name} ({level}) - {code}')
                )
                created_count += 1
            else:
                if course.level != level or course.code != code:
                    course.level = level
                    course.code = code
                    course.save()
                    self.stdout.write(
                        self.style.WARNING(f'→ Updated: {course_name} ({level}) - {code}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'→ Exists: {course_name}')
                    )
                existing_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ IT and Education courses setup complete! Created: {created_count}, Existing: {existing_count}'
        ))
        self.stdout.write(self.style.WARNING(
            '\nℹ Students from other programs can also join the ICT Club!'
        ))
