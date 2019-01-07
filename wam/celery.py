
from __future__ import absolute_import, unicode_literals
import os
import logging
from celery import Celery

from wam.settings import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wam.settings')

url = 'amqp://{user}:{password}@{host}:{port}'.format(
    user=config['CELERY']['USER'],
    password=config['CELERY']['PASSWORD'],
    host=config['CELERY']['HOST'],
    port=config['CELERY']['PORT'],
)
app = Celery(
    'wam',
    broker=url,
    backend=url,
)
app.autodiscover_tasks()
app.conf.task_default_queue = 'wam_queue'

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)


if __name__ == '__main__':
    app.start()
