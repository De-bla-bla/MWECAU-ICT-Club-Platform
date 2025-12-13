"""
Comprehensive middleware for request/response tracking
"""
from django.utils.deprecation import MiddlewareMixin
import uuid
import time
import logging

logger = logging.getLogger(__name__)


class RequestTrackingMiddleware(MiddlewareMixin):
    """Track all requests with unique IDs"""
    
    def process_request(self, request):
        """Add request ID to request"""
        request.id = str(uuid.uuid4())
        request._start_time = time.time()
        
        logger.info(f'[{request.id}] {request.method} {request.path}')
    
    def process_response(self, request, response):
        """Add request ID to response headers"""
        if hasattr(request, 'id'):
            response['X-Request-ID'] = request.id
            
            if hasattr(request, '_start_time'):
                duration = time.time() - request._start_time
                response['X-Response-Time'] = f'{duration:.3f}s'
                logger.info(f'[{request.id}] {response.status_code} ({duration:.3f}s)')
        
        return response


class CORSMiddleware(MiddlewareMixin):
    """Handle CORS headers"""
    
    def process_response(self, request, response):
        """Add CORS headers"""
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return response


class CompressionMiddleware(MiddlewareMixin):
    """Enable gzip compression for responses"""
    
    def process_response(self, request, response):
        """Add compression headers"""
        if 'gzip' in request.META.get('HTTP_ACCEPT_ENCODING', ''):
            response['Content-Encoding'] = 'gzip'
        
        return response
