
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from wam.settings import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wam.settings')

rtd_mode = config['WAM'].get('RTD-MODE', 'False') == 'True'
if rtd_mode:
    url = None
else:
    url = 'amqp://{user}:{password}@{host}:{port}/{vhost}'.format(
        user=config['CELERY']['USER'],
        password=config['CELERY']['PASSWORD'],
        host=config['CELERY']['HOST'],
        port=config['CELERY']['PORT'],
        vhost=config['CELERY']['VHOST'],
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
