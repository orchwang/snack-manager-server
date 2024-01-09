#!/bin/bash

poetry run python manage.py migrate \
  --noinput \
  --settings=snack.settings.dev

poetry run python manage.py collectstatic \
  --noinput \
  --settings=snack.settings.dev

poetry run python manage.py runserver 0.0.0.0:3100 \
  --settings=snack.settings.dev

