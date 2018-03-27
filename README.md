# Zurb-Installation on Linux:
Download nodejs from: https://nodejs.org/en/

Follow instructions from: https://github.com/nodejs/help/wiki/Installation
Additionally, add npm and node to /usr/bin/:
sudo ln -s /usr/lib/nodejs/node-v8.9.4/bin/npm /usr/bin/npm
sudo ln -s /usr/lib/nodejs/node-v8.9.4/bin/node /usr/bin/node

Install foundation via:
sudo npm install --global foundation-cli
