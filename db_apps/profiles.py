
import os
import pandas
import numpy as np
from scipy import io
from random import randrange

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'wam.settings'
application = get_wsgi_application()

from stemp.models import LoadProfile, HeatProfile


def load_profile_upload():
    file = (
        '/home/hendrik/rl-institut/04_Projekte/109_EOS/04-Projektinhalte/'
        '05_Daten/Lastgaenge/Haushalte/80_Lastprofile_von_HTW/HTW-Lastprofile/'
        'Lastprofile/Sytheseprofile_80_P_Q_15min.mat'
    )
    data = io.loadmat(file)
    p = pandas.DataFrame(data['P_sum'])
    q = pandas.DataFrame(data['Q_sum'])

    # Calculate "Scheinleistung":
    s = (p.pow(2) + q.pow(2)).pow(0.5)

    s_hourly = s.groupby(np.arange(len(s)) // 4).sum()
    for column in s_hourly:
        kwargs = {
            'name': 'HH-' + str(column),
            'profile': s_hourly[column].tolist()
        }
        load = LoadProfile(**kwargs)
        load.save()


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
