import os
import subprocess
from configobj import ConfigObj

base_dir = os.path.abspath(os.path.curdir)
pip_path = subprocess.check_output(['which', 'pip']).decode().strip('\n')
config = ConfigObj(os.environ['CONFIG_PATH'])
apps = config['WAM'].get_list('APPS')
for app in apps:
    req_file = os.path.join(base_dir, app, 'requirements.txt')
    if os.path.isfile(req_file):
        subprocess.call(
            [pip_path, 'install', '-r', req_file]
        )
