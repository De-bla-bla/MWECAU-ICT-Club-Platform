"""
Utilities for pagination, filtering, and sorting
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


class SimplePaginator:
    """Helper class for paginating querysets"""
    
    @staticmethod
    def paginate(queryset, page, per_page=12):
        """
        Paginate a queryset
        
        Args:
            queryset: Django QuerySet to paginate
            page: Current page number (from request.GET)
            per_page: Number of items per page (default: 12)
        
        Returns:
            Dictionary with paginated results and page info
        """
        paginator = Paginator(queryset, per_page)
        
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        
        return {
            'items': items,
            'paginator': paginator,
            'current_page': items.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_next': items.has_next(),
            'has_previous': items.has_previous(),
        }


class SearchFilter:
    """Helper class for searching across models"""
    
    @staticmethod
    def search_projects(queryset, query):
        """Search projects by title or description"""
        if not query:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    
    @staticmethod
    def search_events(queryset, query):
        """Search events by title, description, or location"""
        if not query:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    
    @staticmethod
    def search_announcements(queryset, query):
        """Search announcements by title or content"""
        if not query:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    
    @staticmethod
    def search_members(queryset, query):
        """Search members by name or registration number"""
        if not query:
            return queryset
        
        return queryset.filter(
            Q(full_name__icontains=query) |
            Q(reg_number__icontains=query) |
            Q(email__icontains=query)
        )


class FilterHelper:
    """Helper class for filtering querysets"""
    
    @staticmethod
    def filter_by_department(queryset, department_id):
        """Filter queryset by department"""
        if not department_id:
            return queryset
        
        return queryset.filter(department_id=department_id)
    
    @staticmethod
    def filter_by_status(queryset, status):
        """Filter queryset by status"""
        if not status:
            return queryset
        
        status_map = {
            'approved': {'is_approved': True},
            'pending': {'is_approved': False},
            'active': {'is_active': True},
            'inactive': {'is_active': False},
        }
        
        if status in status_map:
            return queryset.filter(**status_map[status])
        
        return queryset
    
    @staticmethod
    def filter_upcoming_events(queryset):
        """Filter to show only upcoming events"""
        from django.utils import timezone
        return queryset.filter(event_date__gte=timezone.now()).order_by('event_date')
    
    @staticmethod
    def filter_published_announcements(queryset):
        """Filter to show only published announcements"""
        return queryset.filter(is_published=True).order_by('-created_at')


class SortHelper:
    """Helper class for sorting querysets"""
    
    @staticmethod
    def sort_by_date(queryset, field='created_at', ascending=False):
        """Sort queryset by date field"""
        order = field if ascending else f'-{field}'
        return queryset.order_by(order)
    
    @staticmethod
    def sort_by_name(queryset, field='name', ascending=True):
        """Sort queryset by name field"""
        order = field if ascending else f'-{field}'
        return queryset.order_by(order)
    
    @staticmethod
    def sort_members_by_status(queryset, approved_first=True):
        """Sort members with approved first"""
        if approved_first:
            return queryset.order_by('-is_approved', '-registered_at')
        return queryset.order_by('is_approved', '-registered_at')
