
import os
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'kopy.settings'
application = get_wsgi_application()

from stemp.models import OEPScenario


def clear_scenario():
    OEPScenario.delete_table()
    OEPScenario.create_table()


if __name__ == '__main__':
    clear_scenario()
