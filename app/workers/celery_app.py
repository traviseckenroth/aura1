from celery import Celery
from celery.schedules import crontab

# Initialize the Celery instance
celery_instance = Celery(
    'twin_matchmaker',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['app.workers.match_tasks']
)

# Configuration for Celery Beat (The Scheduler)
celery_instance.conf.beat_schedule = {
    'run-matchmaking-every-night': {
        'task': 'app.workers.match_tasks.run_overnight_batch',
        'schedule': crontab(hour=2, minute=0), # Fires at 2:00 AM every morning
        'args': ('user_001',), # In prod, this would loop through all active users
    },
}

celery_instance.conf.timezone = 'UTC'