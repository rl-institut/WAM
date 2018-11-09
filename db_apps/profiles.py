
import os
import pandas
import numpy as np
from scipy import io
from random import randrange

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'wam.settings'
application = get_wsgi_application()

from stemp.models import HeatProfile


def create_test_heat_profile():
    kwargs = {
        'name': 'Heat_8760_random',
        'profile': [randrange(0, 100) for i in range(8760)]
    }
    heat = HeatProfile(**kwargs)
    heat.save()


if __name__ == '__main__':
    create_test_heat_profile()
    # load_profile_upload()
