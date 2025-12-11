"""
Custom model managers and querysets
"""
from django.db import models
from django.utils import timezone


class UserQuerySet(models.QuerySet):
    """Custom QuerySet for User model"""
    
    def approved(self):
        """Get approved users"""
        return self.filter(is_approved=True)
    
    def pending(self):
        """Get users pending approval"""
        return self.filter(is_approved=False)
    
    def active(self):
        """Get active users"""
        return self.filter(is_active=True)
    
    def with_pictures(self):
        """Get users who have uploaded pictures"""
        return self.exclude(picture='')
    
    def without_pictures(self):
        """Get users without pictures"""
        return self.filter(picture='')
    
    def overdue_pictures(self):
        """Get users with overdue picture uploads"""
        users = []
        for user in self:
            if user.is_picture_overdue():
                users.append(user.id)
        return self.filter(id__in=users)
    
    def by_department(self, department):
        """Filter users by department"""
        return self.filter(department=department)
    
    def leaders(self):
        """Get department leaders"""
        return self.filter(is_department_leader=True)
    
    def staff(self):
        """Get staff members"""
        return self.filter(is_staff=True)
    
    def recent(self, days=30):
        """Get users registered in last N days"""
        since = timezone.now() - timezone.timedelta(days=days)
        return self.filter(registered_at__gte=since)


class UserManager(models.Manager):
    """Custom manager for User model"""
    
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)
    
    def approved(self):
        return self.get_queryset().approved()
    
    def pending(self):
        return self.get_queryset().pending()
    
    def active(self):
        return self.get_queryset().active()
    
    def with_pictures(self):
        return self.get_queryset().with_pictures()
    
    def without_pictures(self):
        return self.get_queryset().without_pictures()
    
    def overdue_pictures(self):
        return self.get_queryset().overdue_pictures()
    
    def leaders(self):
        return self.get_queryset().leaders()
    
    def staff(self):
        return self.get_queryset().staff()
    
    def recent(self, days=30):
        return self.get_queryset().recent(days)


class ProjectQuerySet(models.QuerySet):
    """Custom QuerySet for Project model"""
    
    def featured(self):
        """Get featured projects"""
        return self.filter(featured=True)
    
    def by_department(self, department):
        """Filter projects by department"""
        return self.filter(department=department)
    
    def recent(self, count=5):
        """Get recent projects"""
        return self.order_by('-created_at')[:count]
    
    def with_live_url(self):
        """Get projects with live URLs"""
        return self.exclude(live_url='')
    
    def with_github_url(self):
        """Get projects with GitHub URLs"""
        return self.exclude(github_url='')


class ProjectManager(models.Manager):
    """Custom manager for Project model"""
    
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)
    
    def featured(self):
        return self.get_queryset().featured()
    
    def by_department(self, department):
        return self.get_queryset().by_department(department)
    
    def recent(self, count=5):
        return self.get_queryset().recent(count)


class EventQuerySet(models.QuerySet):
    """Custom QuerySet for Event model"""
    
    def upcoming(self):
        """Get upcoming events"""
        return self.filter(event_date__gte=timezone.now()).order_by('event_date')
    
    def past(self):
        """Get past events"""
        return self.filter(event_date__lt=timezone.now()).order_by('-event_date')
    
    def by_department(self, department):
        """Filter events by department"""
        return self.filter(department=department)
    
    def this_month(self):
        """Get events this month"""
        now = timezone.now()
        return self.filter(
            event_date__year=now.year,
            event_date__month=now.month
        ).order_by('event_date')
    
    def this_week(self):
        """Get events this week"""
        today = timezone.now().date()
        start_week = today - timezone.timedelta(days=today.weekday())
        end_week = start_week + timezone.timedelta(days=6)
        return self.filter(
            event_date__date__gte=start_week,
            event_date__date__lte=end_week
        ).order_by('event_date')


class EventManager(models.Manager):
    """Custom manager for Event model"""
    
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)
    
    def upcoming(self):
        return self.get_queryset().upcoming()
    
    def past(self):
        return self.get_queryset().past()
    
    def this_month(self):
        return self.get_queryset().this_month()
    
    def this_week(self):
        return self.get_queryset().this_week()


class AnnouncementQuerySet(models.QuerySet):
    """Custom QuerySet for Announcement model"""
    
    def published(self):
        """Get published announcements"""
        return self.filter(is_published=True)
    
    def unpublished(self):
        """Get unpublished announcements"""
        return self.filter(is_published=False)
    
    def by_type(self, announcement_type):
        """Filter announcements by type"""
        return self.filter(announcement_type=announcement_type)
    
    def by_department(self, department):
        """Filter announcements by department"""
        return self.filter(department=department)
    
    def recent(self, count=10):
        """Get recent announcements"""
        return self.published().order_by('-created_at')[:count]
    
    def urgent(self):
        """Get urgent announcements"""
        return self.by_type('urgent')
    
    def general(self):
        """Get general announcements"""
        return self.by_type('general')


class AnnouncementManager(models.Manager):
    """Custom manager for Announcement model"""
    
    def get_queryset(self):
        return AnnouncementQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def unpublished(self):
        return self.get_queryset().unpublished()
    
    def by_type(self, announcement_type):
        return self.get_queryset().by_type(announcement_type)
    
    def recent(self, count=10):
        return self.get_queryset().recent(count)
    
    def urgent(self):
        return self.get_queryset().urgent()
