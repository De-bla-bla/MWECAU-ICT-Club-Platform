"""
Production deployment utilities and helpers
"""
import os
import subprocess
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class DeploymentHelper:
    """Help with deployment tasks"""
    
    @staticmethod
    def collect_static_files():
        """Collect static files"""
        try:
            from django.core.management import call_command
            call_command('collectstatic', verbosity=1, interactive=False)
            logger.info('Static files collected successfully')
            return True
        except Exception as e:
            logger.error(f'Failed to collect static files: {str(e)}')
            return False
    
    @staticmethod
    def run_migrations():
        """Run database migrations"""
        try:
            from django.core.management import call_command
            call_command('migrate', verbosity=1)
            logger.info('Migrations completed successfully')
            return True
        except Exception as e:
            logger.error(f'Failed to run migrations: {str(e)}')
            return False
    
    @staticmethod
    def create_superuser(username, email, password):
        """Create superuser"""
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            if User.objects.filter(username=username).exists():
                logger.warning(f'User {username} already exists')
                return False
            
            User.objects.create_superuser(username, email, password)
            logger.info(f'Superuser {username} created')
            return True
        except Exception as e:
            logger.error(f'Failed to create superuser: {str(e)}')
            return False


class BackupHelper:
    """Help with backup operations"""
    
    @staticmethod
    def backup_database():
        """Backup database"""
        try:
            from django.core.management import call_command
            from datetime import datetime
            
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_dir, f'backup_{timestamp}.sql')
            
            db_config = settings.DATABASES['default']
            
            # For SQLite
            if 'sqlite' in db_config['ENGINE']:
                import shutil
                shutil.copy2(db_config['NAME'], backup_file)
            
            logger.info(f'Database backed up to {backup_file}')
            return backup_file
        except Exception as e:
            logger.error(f'Backup failed: {str(e)}')
            return None
    
    @staticmethod
    def backup_media():
        """Backup media directory"""
        try:
            import shutil
            from datetime import datetime
            
            media_root = settings.MEDIA_ROOT
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_dir, f'media_backup_{timestamp}.tar.gz')
            
            shutil.make_archive(backup_file.replace('.tar.gz', ''), 'gzip', media_root)
            
            logger.info(f'Media backed up to {backup_file}')
            return backup_file
        except Exception as e:
            logger.error(f'Media backup failed: {str(e)}')
            return None


class HealthCheckHelper:
    """Health check utilities"""
    
    @staticmethod
    def run_health_checks():
        """Run all health checks"""
        from core.monitoring import HealthCheck
        
        return HealthCheck.get_full_health_status()
    
    @staticmethod
    def check_critical_settings():
        """Check critical Django settings"""
        issues = []
        
        if settings.DEBUG:
            issues.append('DEBUG is enabled in production')
        
        if not settings.ALLOWED_HOSTS:
            issues.append('ALLOWED_HOSTS is not configured')
        
        if settings.SECRET_KEY == 'your-secret-key-here':
            issues.append('SECRET_KEY is using default value')
        
        return {
            'healthy': len(issues) == 0,
            'issues': issues,
        }
