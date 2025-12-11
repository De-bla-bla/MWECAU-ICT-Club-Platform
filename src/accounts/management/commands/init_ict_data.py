from django.core.management.base import BaseCommand
from django.utils.text import slugify
from accounts.models import Department, Course


class Command(BaseCommand):
    help = 'Initialize departments and courses for ICT Club'

    def handle(self, *args, **options):
        # Define departments
        departments_data = [
            {
                'name': 'Programming',
                'description': 'Python, JavaScript, PHP development and backend engineering'
            },
            {
                'name': 'Cybersecurity',
                'description': 'Ethical hacking, digital forensics, and security research'
            },
            {
                'name': 'Networking',
                'description': 'Network design, implementation, and infrastructure management'
            },
            {
                'name': 'Computer Maintenance',
                'description': 'Hardware support, software troubleshooting, and system maintenance'
            },
            {
                'name': 'Graphic Design',
                'description': 'Adobe Creative Suite, Canva, UI/UX design, and visual communication'
            },
            {
                'name': 'AI & Machine Learning',
                'description': 'Artificial intelligence, machine learning models, and automation'
            },
        ]

        # Define courses
        courses_data = [
            'Bachelor of Science in Computer Science',
            'Bachelor of Science in Information Technology',
            'Bachelor of Science in Software Engineering',
            'Bachelor of Science in Cybersecurity',
            'Diploma in Computer Applications',
            'Certificate in Computer Skills',
        ]

        # Create departments
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={
                    'slug': slugify(dept_data['name']),
                    'description': dept_data['description'],
                }
            )
            status = 'Created' if created else 'Already exists'
            self.stdout.write(self.style.SUCCESS(f"✓ {status}: {dept.name}"))

        # Create courses
        for course_name in courses_data:
            course, created = Course.objects.get_or_create(
                name=course_name,
                defaults={'code': None}
            )
            status = 'Created' if created else 'Already exists'
            self.stdout.write(self.style.SUCCESS(f"✓ {status}: {course.name}"))

        self.stdout.write(self.style.SUCCESS('\n✓ Initialization complete!'))
        self.stdout.write(self.style.WARNING(
            '\nNext steps:\n'
            '1. Create a superuser: python manage.py createsuperuser\n'
            '2. Assign department leaders in Django admin\n'
            '3. Configure email settings in .env\n'
            '4. Test registration workflow'
        ))
