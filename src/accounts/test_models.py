"""
Unit tests for accounts app models
"""
from django.test import TestCase
from django.utils import timezone
from accounts.models import CustomUser, Department, Course


class DepartmentModelTest(TestCase):
    """Test cases for Department model"""
    
    def setUp(self):
        self.department = Department.objects.create(
            name='Programming',
            slug='programming',
            description='Programming department'
        )
    
    def test_department_creation(self):
        """Test department is created correctly"""
        self.assertEqual(self.department.name, 'Programming')
        self.assertEqual(self.department.slug, 'programming')
    
    def test_department_str(self):
        """Test department string representation"""
        self.assertEqual(str(self.department), 'Programming')


class CourseModelTest(TestCase):
    """Test cases for Course model"""
    
    def setUp(self):
        self.department = Department.objects.create(
            name='Programming',
            slug='programming'
        )
        self.course = Course.objects.create(
            name='Python Programming',
            code='PROG101',
            department=self.department
        )
    
    def test_course_creation(self):
        """Test course is created correctly"""
        self.assertEqual(self.course.name, 'Python Programming')
        self.assertEqual(self.course.code, 'PROG101')
    
    def test_course_str(self):
        """Test course string representation"""
        self.assertEqual(str(self.course), 'PROG101 - Python Programming')


class CustomUserModelTest(TestCase):
    """Test cases for CustomUser model"""
    
    def setUp(self):
        self.department = Department.objects.create(
            name='Programming',
            slug='programming'
        )
        self.course = Course.objects.create(
            name='Python Programming',
            code='PROG101',
            department=self.department
        )
        self.user = CustomUser.objects.create_user(
            reg_number='SE2021001',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            department=self.department,
            course=self.course
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.reg_number, 'SE2021001')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.full_name, 'Test User')
    
    def test_user_is_not_approved_by_default(self):
        """Test user is not approved by default"""
        self.assertFalse(self.user.is_approved)
    
    def test_picture_upload_deadline(self):
        """Test picture upload deadline calculation"""
        deadline = self.user.picture_upload_deadline()
        time_diff = (deadline - self.user.registered_at).total_seconds()
        # Should be approximately 72 hours
        self.assertGreater(time_diff, 3600 * 71)  # > 71 hours
        self.assertLess(time_diff, 3600 * 73)  # < 73 hours
    
    def test_is_picture_overdue_false(self):
        """Test is_picture_overdue returns False for new users"""
        self.assertFalse(self.user.is_picture_overdue())
    
    def test_is_picture_overdue_true(self):
        """Test is_picture_overdue returns True when deadline passed"""
        # Manually set registered_at to 4 days ago
        self.user.registered_at = timezone.now() - timezone.timedelta(days=4)
        self.user.save()
        self.assertTrue(self.user.is_picture_overdue())
    
    def test_is_leadership_false(self):
        """Test is_leadership returns False for regular user"""
        self.assertFalse(self.user.is_leadership())
    
    def test_is_leadership_true_for_leader(self):
        """Test is_leadership returns True for department leader"""
        self.user.is_department_leader = True
        self.user.save()
        self.assertTrue(self.user.is_leadership())
    
    def test_is_leadership_true_for_katibu(self):
        """Test is_leadership returns True for Katibu"""
        self.user.is_katibu = True
        self.user.save()
        self.assertTrue(self.user.is_leadership())


class UserAuthenticationTest(TestCase):
    """Test cases for user authentication"""
    
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
    
    def test_user_can_login(self):
        """Test user can login with correct credentials"""
        self.assertTrue(
            self.user.check_password('testpass123')
        )
    
    def test_user_password_incorrect(self):
        """Test login fails with incorrect password"""
        self.assertFalse(
            self.user.check_password('wrongpass')
        )
    
    def test_user_by_email(self):
        """Test getting user by email"""
        user = CustomUser.objects.get(email='test@example.com')
        self.assertEqual(user.reg_number, 'SE2021001')
    
    def test_user_by_registration_number(self):
        """Test getting user by registration number"""
        user = CustomUser.objects.get(reg_number='SE2021001')
        self.assertEqual(user.email, 'test@example.com')
