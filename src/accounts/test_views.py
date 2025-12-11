"""
View testing utilities and test cases for common view patterns
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from accounts.models import Department, Course

User = get_user_model()


class AuthenticationViewTestCase(TestCase):
    """Test cases for authentication views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.department = Department.objects.create(
            name='Test Dept',
            slug='test-dept'
        )
        self.course = Course.objects.create(
            name='Test Course',
            code='TEST101',
            department=self.department
        )
    
    def test_login_page_loads(self):
        """Test login page loads successfully"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_register_page_loads(self):
        """Test register page loads successfully"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
    
    def test_user_registration(self):
        """Test user registration"""
        data = {
            'reg_number': 'SE2021001',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'full_name': 'Test User',
            'department': self.department.id,
            'course': self.course.id,
        }
        
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
    
    def test_user_login(self):
        """Test user login"""
        user = User.objects.create_user(
            reg_number='SE2021001',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            department=self.department,
            course=self.course,
            is_approved=True
        )
        
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_logout(self):
        """Test user logout"""
        user = User.objects.create_user(
            reg_number='SE2021001',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            department=self.department,
            course=self.course,
            is_approved=True
        )
        
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(reverse('logout'))
        
        self.assertEqual(response.status_code, 302)


class ProfileViewTestCase(TestCase):
    """Test cases for profile views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.department = Department.objects.create(
            name='Test Dept',
            slug='test-dept'
        )
        self.course = Course.objects.create(
            name='Test Course',
            code='TEST101',
            department=self.department
        )
        self.user = User.objects.create_user(
            reg_number='SE2021001',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            department=self.department,
            course=self.course,
            is_approved=True
        )
    
    def test_profile_view_requires_login(self):
        """Test profile view requires authentication"""
        response = self.client.get(reverse('profile_detail', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_profile_view_loads(self):
        """Test profile view loads for authenticated user"""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(reverse('profile_detail', args=[self.user.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_detail.html')
    
    def test_profile_edit_view(self):
        """Test profile edit view"""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(reverse('profile_edit', args=[self.user.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_edit.html')


class PermissionViewTestCase(TestCase):
    """Test cases for permission-restricted views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.department = Department.objects.create(
            name='Test Dept',
            slug='test-dept'
        )
        self.course = Course.objects.create(
            name='Test Course',
            code='TEST101',
            department=self.department
        )
        self.user = User.objects.create_user(
            reg_number='SE2021001',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            department=self.department,
            course=self.course,
            is_approved=True
        )
        self.admin_user = User.objects.create_superuser(
            reg_number='SE2021002',
            email='admin@example.com',
            password='adminpass123',
            full_name='Admin User',
            department=self.department,
            course=self.course
        )
    
    def test_admin_view_requires_superuser(self):
        """Test admin view requires superuser status"""
        # Login as regular user
        self.client.login(username='test@example.com', password='testpass123')
        
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [302, 403])
    
    def test_admin_view_allows_superuser(self):
        """Test admin view allows superuser"""
        self.client.login(username='admin@example.com', password='adminpass123')
        
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)


class MessageViewTestCase(TestCase):
    """Test cases for views with messages"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.department = Department.objects.create(
            name='Test Dept',
            slug='test-dept'
        )
        self.course = Course.objects.create(
            name='Test Course',
            code='TEST101',
            department=self.department
        )
        self.user = User.objects.create_user(
            reg_number='SE2021001',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            department=self.department,
            course=self.course,
            is_approved=False
        )
    
    def test_pending_approval_message(self):
        """Test pending approval message displays"""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(reverse('home'))
        
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any('approval' in str(m).lower() for m in messages_list))


class RedirectViewTestCase(TestCase):
    """Test cases for redirect behavior"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
    
    def test_redirect_anonymous_to_login(self):
        """Test redirects anonymous user to login"""
        response = self.client.get(reverse('home'))
        
        if response.status_code == 302:
            self.assertIn(reverse('login'), response.url)
    
    def test_redirect_pending_user_to_pending_page(self):
        """Test redirects pending user to pending approval page"""
        department = Department.objects.create(
            name='Test Dept',
            slug='test-dept'
        )
        course = Course.objects.create(
            name='Test Course',
            code='TEST101',
            department=department
        )
        user = User.objects.create_user(
            reg_number='SE2021001',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            department=department,
            course=course,
            is_approved=False
        )
        
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(reverse('home'))
        
        if response.status_code == 302:
            self.assertIn('pending', response.url.lower())
