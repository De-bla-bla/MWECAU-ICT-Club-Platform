"""
Middleware for enforcing 72-hour picture upload requirement and security headers
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class PictureUploadMiddleware:
    """
    Middleware to enforce picture upload within 72 hours for authenticated users.
    Redirects to upload_picture page if deadline has passed.
    """
    
    # URLs that should not trigger the picture upload redirect
    EXEMPT_URLS = [
        '/upload-picture/',
        '/logout/',
        '/api/',
        '/admin/',
        '/static/',
        '/media/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            # Skip if URL is exempt
            if any(request.path.startswith(url) for url in self.EXEMPT_URLS):
                return self.get_response(request)
            
            # Skip if user is superuser/staff
            if request.user.is_staff:
                return self.get_response(request)
            
            # Check if picture is overdue
            if request.user.is_picture_overdue():
                return redirect('upload_picture')
        
        response = self.get_response(request)
        return response


class SecurityHeadersMiddleware:
    """
    Middleware to add security headers to all responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Only add HSTS in production (requires HTTPS)
        if not request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        return response
