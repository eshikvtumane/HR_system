from datetime import timedelta

BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = 'redis://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Vladivostok'

CELERYBEAT_SCHEDULE = {
    'check-events-every-30-minutes': {
        'task': 'events.tasks.check_events',
        'schedule': timedelta(seconds=10)

    },
}