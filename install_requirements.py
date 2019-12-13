import os
import subprocess

base_dir = os.path.abspath(os.path.curdir)
pip_path = subprocess.check_output(["which", "pip"]).decode().strip("\n")
apps = os.environ["WAM_APPS"].split(",")
for app in apps:
    req_file = os.path.join(base_dir, app, "requirements.txt")
    if os.path.isfile(req_file):
        subprocess.call([pip_path, "install", "-r", req_file])
