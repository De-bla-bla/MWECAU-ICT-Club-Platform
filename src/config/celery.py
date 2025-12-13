"""
Celery async task configuration
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create Celery app
app = Celery('mwecau_ict')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Celery Beat Schedule - Periodic Tasks
app.conf.beat_schedule = {
    'cleanup-old-logs': {
        'task': 'core.tasks.cleanup_old_logs',
        'schedule': crontab(hour=2, minute=0),  # Run at 2 AM daily
    },
    'cleanup-old-messages': {
        'task': 'core.tasks.cleanup_old_contact_messages',
        'schedule': crontab(hour=3, minute=0),  # Run at 3 AM daily
    },
    'send-picture-reminders': {
        'task': 'core.tasks.send_picture_reminders',
        'schedule': crontab(hour=10, minute=0),  # Run at 10 AM daily
    },
    'generate-statistics': {
        'task': 'core.tasks.generate_statistics',
        'schedule': crontab(hour=23, minute=59),  # Run before midnight daily
    },
}

# Celery Configuration
app.conf.update(
    # Timezone
    timezone='Africa/Dar_es_Salaam',
    
    # Task settings
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Task timeouts
    task_soft_time_limit=300,  # 5 minutes soft timeout
    task_time_limit=600,       # 10 minutes hard timeout
    
    # Result backend settings
    result_expires=3600,  # Results expire after 1 hour
    
    # Task retry settings
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)


@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')
