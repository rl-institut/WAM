from __future__ import absolute_import, unicode_literals
from celery import Celery
from kopy.settings import config

url = 'amqp://{user}:{password}@{host}:{port}'.format(
    user=config['CELERY']['USER'],
    password=config['CELERY']['PASSWORD'],
    host=config['CELERY']['HOST'],
    port=config['CELERY']['PORT'],
)
app = Celery(
    'kopy',
    broker=url,
    backend=url,
    include=['stemp.tasks']
)

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
