"""
API documentation and schema utilities
"""
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


class APIDocumentation:
    """API documentation helper"""
    
    @staticmethod
    def get_api_documentation():
        """Get comprehensive API documentation"""
        return {
            'name': 'MWECAU ICT Club API',
            'version': '1.0.0',
            'description': 'RESTful API for managing MWECAU ICT Club',
            'base_url': '/api/v1/',
            'authentication': {
                'type': 'Token Authentication',
                'header': 'Authorization: Token <token>',
                'description': 'Include token in Authorization header'
            },
            'endpoints': {
                'departments': {
                    'list': 'GET /api/departments/',
                    'detail': 'GET /api/departments/{id}/',
                    'create': 'POST /api/departments/',
                    'update': 'PUT /api/departments/{id}/',
                    'delete': 'DELETE /api/departments/{id}/',
                },
                'users': {
                    'list': 'GET /api/users/',
                    'detail': 'GET /api/users/{id}/',
                    'approve': 'POST /api/users/{id}/approve/',
                    'reject': 'POST /api/users/{id}/reject/',
                },
                'projects': {
                    'list': 'GET /api/projects/',
                    'detail': 'GET /api/projects/{id}/',
                    'create': 'POST /api/projects/',
                    'update': 'PUT /api/projects/{id}/',
                    'delete': 'DELETE /api/projects/{id}/',
                    'featured': 'GET /api/projects/featured/',
                },
                'events': {
                    'list': 'GET /api/events/',
                    'detail': 'GET /api/events/{id}/',
                    'create': 'POST /api/events/',
                    'update': 'PUT /api/events/{id}/',
                    'upcoming': 'GET /api/events/upcoming/',
                },
                'announcements': {
                    'list': 'GET /api/announcements/',
                    'detail': 'GET /api/announcements/{id}/',
                    'create': 'POST /api/announcements/',
                    'published': 'GET /api/announcements/published/',
                },
            },
            'error_responses': {
                '400': 'Bad Request',
                '401': 'Unauthorized',
                '403': 'Forbidden',
                '404': 'Not Found',
                '500': 'Server Error',
            }
        }


class SchemaGenerator:
    """Generate API schema"""
    
    @staticmethod
    def generate_field_schema(field):
        """Generate schema for serializer field"""
        schema = {
            'type': field.__class__.__name__,
            'required': field.required,
        }
        
        if hasattr(field, 'help_text') and field.help_text:
            schema['description'] = str(field.help_text)
        
        if isinstance(field, serializers.ChoiceField):
            schema['choices'] = list(field.choices.keys())
        
        return schema
    
    @staticmethod
    def generate_serializer_schema(serializer_class):
        """Generate schema for serializer"""
        serializer = serializer_class()
        schema = {}
        
        for field_name, field in serializer.fields.items():
            schema[field_name] = SchemaGenerator.generate_field_schema(field)
        
        return schema


class ResponseFormatter:
    """Format API responses consistently"""
    
    @staticmethod
    def format_success(data, message='Success'):
        """Format success response"""
        return {
            'success': True,
            'message': message,
            'data': data,
        }
    
    @staticmethod
    def format_error(error, status_code=400):
        """Format error response"""
        return {
            'success': False,
            'error': error,
            'status_code': status_code,
        }
    
    @staticmethod
    def format_paginated(results, count, next_page=None, previous_page=None):
        """Format paginated response"""
        return {
            'success': True,
            'count': count,
            'next': next_page,
            'previous': previous_page,
            'results': results,
        }
