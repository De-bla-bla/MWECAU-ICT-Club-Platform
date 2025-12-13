"""
Comprehensive test utilities and fixtures
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

User = get_user_model()


class APITestHelper:
    """Helper for API testing"""
    
    @staticmethod
    def get_auth_token(user):
        """Get authentication token for user"""
        token, _ = Token.objects.get_or_create(user=user)
        return token.key
    
    @staticmethod
    def get_auth_headers(user):
        """Get authorization headers for user"""
        token = APITestHelper.get_auth_token(user)
        return {'HTTP_AUTHORIZATION': f'Token {token}'}
    
    @staticmethod
    def create_authenticated_client(user):
        """Create API client with user authentication"""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {APITestHelper.get_auth_token(user)}')
        return client


class ModelTestHelper:
    """Helper for model testing"""
    
    @staticmethod
    def assert_model_exists(model_class, **filters):
        """Assert model instance exists with filters"""
        return model_class.objects.filter(**filters).exists()
    
    @staticmethod
    def assert_model_count(model_class, count, **filters):
        """Assert model count matches"""
        actual = model_class.objects.filter(**filters).count()
        return actual == count
    
    @staticmethod
    def assert_field_value(instance, field_name, expected_value):
        """Assert field has expected value"""
        actual = getattr(instance, field_name)
        return actual == expected_value


class FormTestHelper:
    """Helper for form testing"""
    
    @staticmethod
    def assert_form_valid(form_class, data):
        """Assert form is valid with data"""
        form = form_class(data=data)
        return form.is_valid()
    
    @staticmethod
    def assert_form_invalid(form_class, data):
        """Assert form is invalid with data"""
        form = form_class(data=data)
        return not form.is_valid()
    
    @staticmethod
    def get_form_errors(form_class, data):
        """Get form errors for data"""
        form = form_class(data=data)
        form.is_valid()
        return form.errors


class ViewTestHelper:
    """Helper for view testing"""
    
    @staticmethod
    def assert_view_requires_login(client, url):
        """Assert view requires login"""
        response = client.get(url)
        return response.status_code in [301, 302]
    
    @staticmethod
    def assert_view_accessible_after_login(client, url, user):
        """Assert view is accessible after login"""
        client.login(username=user.email, password='testpass123')
        response = client.get(url)
        return response.status_code == 200
    
    @staticmethod
    def post_to_view(client, url, data, user=None):
        """Post data to view"""
        if user:
            client.login(username=user.email, password='testpass123')
        return client.post(url, data)
