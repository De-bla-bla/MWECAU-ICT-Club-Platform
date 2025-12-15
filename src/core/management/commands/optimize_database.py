"""
Django management command to clean up and optimize the database
"""
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Q
from accounts.models import CustomUser
from core.models import ContactMessage, Announcement
from datetime import timedelta
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Optimize database by cleaning up old data and cache'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
        
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Delete records older than this many days (default: 90)',
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        days = options['days']
        
        self.stdout.write(f"Starting database optimization (dry-run: {dry_run})")
        
        # Clean up old contact messages
        self._cleanup_old_contact_messages(days, dry_run)
        
        # Clean up draft announcements older than 6 months
        self._cleanup_draft_announcements(180, dry_run)
        
        # Clean cache
        self._clear_cache(dry_run)
        
        self.stdout.write(self.style.SUCCESS('Database optimization completed successfully'))
    
    def _cleanup_old_contact_messages(self, days: int, dry_run: bool):
        """Remove old contact messages that have been responded to"""
        cutoff_date = timezone.now() - timedelta(days=days)
        
        messages = ContactMessage.objects.filter(
            created_at__lt=cutoff_date,
            responded=True
        )
        
        count = messages.count()
        
        if count > 0:
            self.stdout.write(f"Found {count} old responded contact messages")
            if not dry_run:
                messages.delete()
                self.stdout.write(self.style.SUCCESS(f"Deleted {count} old contact messages"))
            else:
                self.stdout.write(f"[DRY RUN] Would delete {count} old contact messages")
        else:
            self.stdout.write("No old contact messages found")
    
    def _cleanup_draft_announcements(self, days: int, dry_run: bool):
        """Remove draft announcements older than specified days"""
        cutoff_date = timezone.now() - timedelta(days=days)
        
        announcements = Announcement.objects.filter(
            created_at__lt=cutoff_date,
            published=False
        )
        
        count = announcements.count()
        
        if count > 0:
            self.stdout.write(f"Found {count} old draft announcements")
            if not dry_run:
                announcements.delete()
                self.stdout.write(self.style.SUCCESS(f"Deleted {count} old draft announcements"))
            else:
                self.stdout.write(f"[DRY RUN] Would delete {count} old draft announcements")
        else:
            self.stdout.write("No old draft announcements found")
    
    def _clear_cache(self, dry_run: bool):
        """Clear all cache entries"""
        self.stdout.write("Clearing application cache...")
        if not dry_run:
            cache.clear()
            self.stdout.write(self.style.SUCCESS("Cache cleared successfully"))
        else:
            self.stdout.write("[DRY RUN] Would clear cache")
