from celery import Celery

app = Celery(include=['events.tasks'])
app.config_from_object('events.celeryconfig')

@app.task
def add(x,y):
    return x+y

