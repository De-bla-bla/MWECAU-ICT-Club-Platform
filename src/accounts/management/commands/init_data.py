from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Department, Course


User = get_user_model()


class Command(BaseCommand):
    help = 'Create initial data including courses and departments'
    
    def handle(self, *args, **options):
        # Create courses
        courses = [
            'Computer Science',
            'Education With ICT',
            'Mathematics And Statistics'
        ]
        
        for course_name in courses:
            Course.objects.get_or_create(name=course_name)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {Course.objects.count()} courses'))
        
        # Create departments
        departments = [
            ('Programming', 'programming', 'Learn Python, JavaScript, PHP, and modern web development'),
            ('Cybersecurity', 'cybersecurity', 'Ethical hacking, digital forensics, and security practices'),
            ('Networking', 'networking', 'Network design, implementation, and infrastructure management'),
            ('Computer Maintenance', 'computer-maintenance', 'Hardware support, troubleshooting, and system administration'),
            ('Graphic Design', 'graphic-design', 'Creative design using Adobe tools and Canva'),
            ('AI & Machine Learning', 'ai-machine-learning', 'Automation, AI, prototyping, and data science'),
        ]
        
        for name, slug, desc in departments:
            Department.objects.get_or_create(
                name=name,
                defaults={'slug': slug, 'description': desc}
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {Department.objects.count()} departments'))
