import sys
import os
import subprocess

base_dir = os.path.abspath(os.path.curdir)
apps = os.environ['WAM_APPS'].split(',')
for app in apps:
    req_file = os.path.join(base_dir, app, 'requirements.txt')
    if os.path.isfile(req_file):
        subprocess.call(['/opt/conda/envs/django/bin/pip', 'install', '-r', req_file])

