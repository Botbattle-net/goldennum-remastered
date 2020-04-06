#!/bin/bash

python manage.py collectstatic --clear --no-input
cp ./favicon.ico /var/www/storage/goldennum/
gunicorn -b 0.0.0.0:8080 -w4 web.wsgi