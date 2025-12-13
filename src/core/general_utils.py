"""
General purpose utility functions and helpers
"""
from django.utils import timezone
from datetime import timedelta


class StringUtils:
    """String manipulation utilities"""
    
    @staticmethod
    def truncate(text, length=100, suffix='...'):
        """Truncate text to specified length"""
        if len(text) > length:
            return text[:length - len(suffix)] + suffix
        return text
    
    @staticmethod
    def slugify(text):
        """Convert text to URL-safe slug"""
        import re
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')
    
    @staticmethod
    def camel_to_snake(name):
        """Convert camelCase to snake_case"""
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    
    @staticmethod
    def get_initials(full_name):
        """Get initials from full name"""
        parts = full_name.split()
        if len(parts) >= 2:
            return f'{parts[0][0]}{parts[-1][0]}'.upper()
        elif len(parts) == 1:
            return parts[0][0].upper()
        return ''


class DateUtils:
    """Date and time utilities"""
    
    @staticmethod
    def days_until(target_date):
        """Get number of days until target date"""
        delta = target_date - timezone.now()
        return delta.days
    
    @staticmethod
    def hours_until(target_date):
        """Get number of hours until target date"""
        delta = target_date - timezone.now()
        return int(delta.total_seconds() / 3600)
    
    @staticmethod
    def is_today(date):
        """Check if date is today"""
        return date.date() == timezone.now().date()
    
    @staticmethod
    def is_this_month(date):
        """Check if date is this month"""
        now = timezone.now()
        return date.year == now.year and date.month == now.month
    
    @staticmethod
    def is_this_year(date):
        """Check if date is this year"""
        return date.year == timezone.now().year
    
    @staticmethod
    def format_relative(date):
        """Format date relative to now"""
        now = timezone.now()
        delta = now - date
        
        if delta.days == 0:
            return 'Today'
        elif delta.days == 1:
            return 'Yesterday'
        elif delta.days < 7:
            return f'{delta.days} days ago'
        elif delta.days < 30:
            weeks = delta.days // 7
            return f'{weeks} week{"s" if weeks > 1 else ""} ago'
        elif delta.days < 365:
            months = delta.days // 30
            return f'{months} month{"s" if months > 1 else ""} ago'
        else:
            years = delta.days // 365
            return f'{years} year{"s" if years > 1 else ""} ago'


class NumberUtils:
    """Number formatting utilities"""
    
    @staticmethod
    def format_currency(amount, currency='USD'):
        """Format number as currency"""
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'TZS': 'TSh',
        }
        
        symbol = currency_symbols.get(currency, currency)
        return f'{symbol}{amount:,.2f}'
    
    @staticmethod
    def format_percentage(value, decimals=2):
        """Format number as percentage"""
        return f'{value:.{decimals}f}%'
    
    @staticmethod
    def format_file_size(size_bytes):
        """Format bytes as human-readable file size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f'{size_bytes:.2f} {unit}'
            size_bytes /= 1024.0
        return f'{size_bytes:.2f} PB'


class ListUtils:
    """List utilities"""
    
    @staticmethod
    def chunk(items, chunk_size):
        """Split list into chunks"""
        for i in range(0, len(items), chunk_size):
            yield items[i:i + chunk_size]
    
    @staticmethod
    def flatten(nested_list):
        """Flatten nested list"""
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(ListUtils.flatten(item))
            else:
                result.append(item)
        return result
    
    @staticmethod
    def deduplicate(items):
        """Remove duplicates from list while preserving order"""
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
