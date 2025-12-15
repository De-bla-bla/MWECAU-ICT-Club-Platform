"""
Input sanitization utilities for security
"""
from django.utils.html import escape
from django.utils.text import slugify
import re
import logging

logger = logging.getLogger(__name__)


class InputSanitizer:
    """
    Utility class for sanitizing user input to prevent XSS and injection attacks
    """
    
    @staticmethod
    def sanitize_text(text: str, max_length: int = None) -> str:
        """
        Sanitize plain text input
        
        Args:
            text: Text to sanitize
            max_length: Maximum allowed length
            
        Returns:
            str: Sanitized text
        """
        if not text:
            return ""
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        # Escape HTML entities
        text = escape(text)
        
        # Limit length if specified
        if max_length:
            text = text[:max_length]
        
        return text
    
    @staticmethod
    def sanitize_html(html: str, allowed_tags: list = None) -> str:
        """
        Sanitize HTML input (basic implementation - use bleach library for production)
        
        Args:
            html: HTML to sanitize
            allowed_tags: List of allowed HTML tags
            
        Returns:
            str: Sanitized HTML
        """
        if not html:
            return ""
        
        # Basic sanitization - escape all HTML by default
        # For production, use django-bleach or bleach library for proper HTML parsing
        return escape(html)
    
    @staticmethod
    def sanitize_email(email: str) -> str:
        """
        Sanitize and validate email address
        
        Args:
            email: Email to sanitize
            
        Returns:
            str: Sanitized email (lowercased, whitespace removed)
        """
        if not email:
            return ""
        
        # Remove whitespace and convert to lowercase
        email = email.strip().lower()
        
        # Basic email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            logger.warning(f"Invalid email format attempted: {email}")
            return ""
        
        return email
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename for safe file operations
        
        Args:
            filename: Original filename
            
        Returns:
            str: Safe filename
        """
        if not filename:
            return ""
        
        # Remove path separators
        filename = filename.replace('/', '').replace('\\', '')
        
        # Remove null bytes and other dangerous characters
        filename = re.sub(r'[^\w\s.-]', '', filename)
        
        # Use Django slugify for safe filename
        base, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        safe_filename = slugify(base)
        
        return f"{safe_filename}.{ext}" if ext else safe_filename
    
    @staticmethod
    def sanitize_url(url: str) -> str:
        """
        Sanitize URL input
        
        Args:
            url: URL to sanitize
            
        Returns:
            str: Sanitized URL or empty string if invalid
        """
        if not url:
            return ""
        
        url = url.strip()
        
        # Only allow http/https protocols
        if not re.match(r'^https?://', url, re.IGNORECASE):
            logger.warning(f"Invalid protocol in URL: {url}")
            return ""
        
        # Remove control characters
        url = re.sub(r'[\x00-\x1f]', '', url)
        
        return url
    
    @staticmethod
    def sanitize_search_query(query: str) -> str:
        """
        Sanitize search query to prevent injection attacks
        
        Args:
            query: Search query
            
        Returns:
            str: Sanitized search query
        """
        if not query:
            return ""
        
        # Remove special regex characters that could cause ReDoS
        dangerous_chars = r'[.*+?^${}()|[\]\\]'
        query = re.sub(dangerous_chars, '', query)
        
        # Limit length to prevent resource exhaustion
        query = query[:100]
        
        return query.strip()
