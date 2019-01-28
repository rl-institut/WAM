#!/bin/bash

cd /code
source activate django
python manage.py migrate
python manage.py collectstatic --no-input

exec "$@"

