"""
Middleware for enforcing 72-hour picture upload requirement
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
