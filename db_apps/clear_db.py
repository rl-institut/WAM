
import os
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'kopy.settings'
application = get_wsgi_application()

from energysystem.models import Simulation


def clear_simulations():
    sims = Simulation.objects.all()
    for sim in sims:
        print(sim.id)
    sims.delete()


if __name__ == '__main__':
    clear_simulations()
