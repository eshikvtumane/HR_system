from datetime import timedelta

BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'amqp://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Vladivostok'

CELERYBEAT_SCHEDULE = {
    'add-every-10-seconds': {
        'task': 'tasks.add',
        'schedule': timedelta(seconds=10),
        'args': (10, 10)
    },
}