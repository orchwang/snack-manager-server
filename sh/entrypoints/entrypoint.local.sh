#!/bin/bash

python manage.py migrate \
  --noinput \
  --settings=snack.settings.dev

python manage.py collectstatic \
  --noinput \
  --settings=snack.settings.dev

python manage.py runserver 0.0.0.0:3100 \
  --settings=snack.settings.dev

