from celery.schedules import crontab

# Configuration du planning pour les tâches périodiques avec Celery Beat
CELERY_BEAT_SCHEDULE = {
    'check-reminders-every-5-minutes': {
        'task': 'gestion_taches.tasks.tasks.send_reminder',
        'schedule': crontab(minute='*/5'),
        'args': (),
    },
}