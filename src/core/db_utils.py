"""
Database utility functions for backups, cleanup, and optimization
"""
import os
import subprocess
from datetime import datetime, timedelta
import logging
from django.db import connection
from django.conf import settings

logger = logging.getLogger(__name__)


class DatabaseBackup:
    """Database backup utilities"""
    
    @staticmethod
    def backup_sqlite():
        """Backup SQLite database"""
        db_path = settings.DATABASES['default']['NAME']
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        
        # Create backup directory if not exists
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'db_backup_{timestamp}.sqlite3')
        
        # Copy database file
        try:
            import shutil
            shutil.copy2(db_path, backup_file)
            logger.info(f'Database backup created: {backup_file}')
            return backup_file
        except Exception as e:
            logger.error(f'Database backup failed: {str(e)}')
            return None
    
    @staticmethod
    def backup_postgresql():
        """Backup PostgreSQL database"""
        db_config = settings.DATABASES['default']
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        
        # Create backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'db_backup_{timestamp}.sql')
        
        # pg_dump command
        cmd = [
            'pg_dump',
            f'--host={db_config.get("HOST", "localhost")}',
            f'--port={db_config.get("PORT", 5432)}',
            f'--username={db_config.get("USER")}',
            db_config['NAME']
        ]
        
        try:
            with open(backup_file, 'w') as f:
                env = os.environ.copy()
                env['PGPASSWORD'] = db_config.get('PASSWORD', '')
                
                subprocess.run(cmd, stdout=f, env=env, check=True)
                logger.info(f'PostgreSQL backup created: {backup_file}')
                return backup_file
        except Exception as e:
            logger.error(f'PostgreSQL backup failed: {str(e)}')
            return None
    
    @staticmethod
    def cleanup_old_backups(days=7):
        """Remove backups older than specified days"""
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        
        if not os.path.exists(backup_dir):
            return 0
        
        cutoff_time = datetime.now() - timedelta(days=days)
        removed_count = 0
        
        for filename in os.listdir(backup_dir):
            if not filename.startswith('db_backup_'):
                continue
            
            filepath = os.path.join(backup_dir, filename)
            file_time = datetime.fromtimestamp(os.path.getctime(filepath))
            
            if file_time < cutoff_time:
                try:
                    os.remove(filepath)
                    removed_count += 1
                    logger.info(f'Removed old backup: {filename}')
                except Exception as e:
                    logger.error(f'Failed to remove backup {filename}: {str(e)}')
        
        return removed_count


class DatabaseCleaner:
    """Database cleanup utilities"""
    
    @staticmethod
    def cleanup_old_logs(days=30):
        """Delete activity logs older than specified days"""
        from core.models import ActivityLog
        
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count, _ = ActivityLog.objects.filter(
            created_at__lt=cutoff_date
        ).delete()
        
        logger.info(f'Deleted {deleted_count} old activity logs')
        return deleted_count
    
    @staticmethod
    def cleanup_old_contact_messages(days=90):
        """Delete old contact messages"""
        from accounts.models import ContactMessage
        
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count, _ = ContactMessage.objects.filter(
            created_at__lt=cutoff_date
        ).delete()
        
        logger.info(f'Deleted {deleted_count} old contact messages')
        return deleted_count
    
    @staticmethod
    def cleanup_unapproved_users(days=30):
        """Delete users pending approval for more than specified days"""
        from accounts.models import CustomUser
        
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count, _ = CustomUser.objects.filter(
            is_approved=False,
            date_joined__lt=cutoff_date
        ).delete()
        
        logger.info(f'Deleted {deleted_count} unapproved users')
        return deleted_count
    
    @staticmethod
    def cleanup_orphaned_sessions(days=7):
        """Delete expired sessions"""
        from django.contrib.sessions.models import Session
        
        Session.objects.filter(
            expire_date__lt=datetime.now()
        ).delete()
        
        logger.info('Cleaned up expired sessions')
    
    @staticmethod
    def cleanup_failed_login_attempts(days=30):
        """Delete old login failure records"""
        from core.models import LoginAttempt
        
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count, _ = LoginAttempt.objects.filter(
            timestamp__lt=cutoff_date
        ).delete()
        
        logger.info(f'Deleted {deleted_count} old login attempts')
        return deleted_count


class DatabaseOptimization:
    """Database optimization utilities"""
    
    @staticmethod
    def analyze_database():
        """Analyze database for optimization opportunities"""
        with connection.cursor() as cursor:
            # Get table sizes
            if 'sqlite' in settings.DATABASES['default']['ENGINE']:
                cursor.execute("""
                    SELECT name, 
                           (page_count * page_size) as size
                    FROM pragma_page_count(), pragma_page_size()
                """)
            else:
                cursor.execute("""
                    SELECT schemaname, tablename,
                           pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
                    FROM pg_tables
                """)
            
            return cursor.fetchall()
    
    @staticmethod
    def create_indexes():
        """Create missing indexes for common query patterns"""
        from django.db import migrations
        from django.db.migrations.executor import MigrationExecutor
        
        logger.info('Running index creation...')
        
        # This is typically done through Django migrations
        # This is a placeholder for manual index creation
    
    @staticmethod
    def vacuum_database():
        """Vacuum/optimize database (PostgreSQL)"""
        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            with connection.cursor() as cursor:
                cursor.execute('VACUUM ANALYZE;')
                logger.info('Database vacuum completed')
    
    @staticmethod
    def check_database_health():
        """Check overall database health"""
        stats = {
            'timestamp': datetime.now(),
            'tables': 0,
            'indexes': 0,
            'connections': 0
        }
        
        with connection.cursor() as cursor:
            if 'postgresql' in settings.DATABASES['default']['ENGINE']:
                # Count tables
                cursor.execute("""
                    SELECT COUNT(*) FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)
                stats['tables'] = cursor.fetchone()[0]
                
                # Count indexes
                cursor.execute("""
                    SELECT COUNT(*) FROM pg_indexes
                    WHERE schemaname = 'public'
                """)
                stats['indexes'] = cursor.fetchone()[0]
                
                # Active connections
                cursor.execute("""
                    SELECT COUNT(*) FROM pg_stat_activity
                    WHERE state = 'active'
                """)
                stats['connections'] = cursor.fetchone()[0]
        
        return stats


class DatabaseMigration:
    """Database migration utilities"""
    
    @staticmethod
    def run_migrations():
        """Run pending migrations"""
        try:
            from django.core.management import call_command
            call_command('migrate', verbosity=1)
            logger.info('Migrations completed successfully')
            return True
        except Exception as e:
            logger.error(f'Migration failed: {str(e)}')
            return False
    
    @staticmethod
    def show_migration_status():
        """Show migration status"""
        try:
            from django.core.management import call_command
            call_command('showmigrations', verbosity=2)
        except Exception as e:
            logger.error(f'Failed to show migrations: {str(e)}')
    
    @staticmethod
    def create_migration(app_label, name):
        """Create new migration"""
        try:
            from django.core.management import call_command
            call_command('makemigrations', app_label, name=name)
            logger.info(f'Migration created: {name}')
            return True
        except Exception as e:
            logger.error(f'Failed to create migration: {str(e)}')
            return False
