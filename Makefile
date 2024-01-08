TARGET ?= local
VERSION ?= latest
PROJECT_NAME ?= snack
CONTAINER ?= snack-server


# Docker Compose

build:
	docker compose -f docker-compose.$(TARGET).yml --env-file .env.docker-compose up -d --build

up:
	docker compose -f docker-compose.$(TARGET).yml --env-file .env.docker-compose up -d

down:
	docker compose -f docker-compose.$(TARGET).yml --env-file .env.docker-compose down

restart:
	docker compose -f docker-compose.$(TARGET).yml --env-file .env.docker-compose restart $(CONTAINER)

logs:
	docker compose -f docker-compose.$(TARGET).yml --env-file .env.docker-compose logs -f $(CONTAINER)

django-shell:
	docker exec -it $(CONTAINER) python manage.py shell --settings=$(PROJECT_NAME).settings.dev

bash:
	docker exec -it $(CONTAINER) /bin/bash

# PIP Commands

pip-compile:
	docker exec -it $(CONTAINER) pip-compile


# Django Commands

makemigrations:
	docker exec -it $(CONTAINER) python manage.py makemigrations --settings=$(PROJECT_NAME).settings.dev

migrate:
	docker exec -it $(CONTAINER) python manage.py migrate --settings=$(PROJECT_NAME).settings.dev

# Test

test:
	docker exec -it $(CONTAINER) make test-workflow
	rm -rf images

test-workflow:
	coverage erase
	export DJANGO_SETTINGS_MODULES=$(PROJECT_NAME).settings.test; coverage run -m pytest

test-tm:
	docker exec -it $(CONTAINER) pytest -ra -k $(METHOD) --pdb

# Poetry

requirements-dev-to-poetry:
    poetry add --dev --lock -D --allow-prereleases --from=requirements-dev.txt