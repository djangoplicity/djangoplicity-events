#!/bin/sh

# User: admin, Password: admin
python manage.py migrate
python manage.py loaddata dev
python manage.py runserver 0.0.0.0:8000
