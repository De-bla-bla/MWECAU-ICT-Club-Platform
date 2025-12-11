"""
Unit tests for core models
"""
from django.test import TestCase
from django.utils import timezone
from accounts.models import CustomUser, Department, Course
from core.models import Project, Event, Announcement, ContactMessage


class ProjectModelTest(TestCase):
    """Test cases for Project model"""
    
    def setUp(self):
        self.department = Department.objects.create(
            name='Programming',
            slug='programming'
        )
        self.user = CustomUser.objects.create_user(
            reg_number='SE2021001',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            department=self.department
        )
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            slug='test-project',
            department=self.department,
            created_by=self.user
        )
    
    def test_project_creation(self):
        """Test project is created correctly"""
        self.assertEqual(self.project.title, 'Test Project')
        self.assertEqual(self.project.slug, 'test-project')
    
    def test_project_str(self):
        """Test project string representation"""
        self.assertEqual(str(self.project), 'Test Project')
    
    def test_project_featured_default(self):
        """Test project is not featured by default"""
        self.assertFalse(self.project.featured)


class EventModelTest(TestCase):
    """Test cases for Event model"""
    
    def setUp(self):
        self.department = Department.objects.create(
            name='Programming',
            slug='programming'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            event_date=timezone.now() + timezone.timedelta(days=1),
            location='Test Location',
            department=self.department
        )
    
    def test_event_creation(self):
        """Test event is created correctly"""
        self.assertEqual(self.event.title, 'Test Event')
        self.assertEqual(self.event.location, 'Test Location')
    
    def test_event_str(self):
        """Test event string representation"""
        self.assertEqual(str(self.event), 'Test Event')


class AnnouncementModelTest(TestCase):
    """Test cases for Announcement model"""
    
    def setUp(self):
        self.department = Department.objects.create(
            name='Programming',
            slug='programming'
        )
        self.announcement = Announcement.objects.create(
            title='Test Announcement',
            content='Test Content',
            announcement_type='general',
            department=self.department,
            is_published=True
        )
    
    def test_announcement_creation(self):
        """Test announcement is created correctly"""
        self.assertEqual(self.announcement.title, 'Test Announcement')
        self.assertEqual(self.announcement.announcement_type, 'general')
    
    def test_announcement_published_by_default_false(self):
        """Test announcement is not published by default"""
        announcement = Announcement.objects.create(
            title='Test',
            content='Test',
            department=self.department
        )
        self.assertFalse(announcement.is_published)
    
    def test_announcement_str(self):
        """Test announcement string representation"""
        self.assertEqual(str(self.announcement), 'Test Announcement')


class ContactMessageModelTest(TestCase):
    """Test cases for ContactMessage model"""
    
    def setUp(self):
        self.message = ContactMessage.objects.create(
            name='Test User',
            email='test@example.com',
            phone='1234567890',
            subject='Test Subject',
            message='Test Message'
        )
    
    def test_contact_message_creation(self):
        """Test contact message is created correctly"""
        self.assertEqual(self.message.name, 'Test User')
        self.assertEqual(self.message.email, 'test@example.com')
    
    def test_contact_message_responded_false_by_default(self):
        """Test contact message is not responded by default"""
        self.assertFalse(self.message.is_responded)
    
    def test_contact_message_str(self):
        """Test contact message string representation"""
        self.assertEqual(str(self.message), 'Test Subject - Test User')
