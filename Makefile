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
	docker exec -it $(CONTAINER) poetry run python manage.py shell --settings=$(PROJECT_NAME).settings.dev

bash:
	docker exec -it $(CONTAINER) /bin/bash


# Django Commands

makemigrations:
	docker exec -it $(CONTAINER) poetry run python manage.py makemigrations --settings=$(PROJECT_NAME).settings.dev

migrate:
	docker exec -it $(CONTAINER) poetry run python manage.py migrate --settings=$(PROJECT_NAME).settings.dev

fake-migrate:
	docker exec -it $(CONTAINER) poetry run python manage.py migrate --fake --settings=$(PROJECT_NAME).settings.dev


# Test

test:
	docker exec -it $(CONTAINER) make test-workflow

test-workflow:
	poetry run coverage erase
	export DJANGO_SETTINGS_MODULES=$(PROJECT_NAME).settings.test; poetry run coverage run -m pytest -n 10 --no-migrations

coverage-report:
	docker exec -it $(CONTAINER) poetry run coverage report

test-tm:
	docker exec -it $(CONTAINER) pytest -ra -k $(METHOD) --pdb

remove-test-statics:
	rm -rf tests/images
	rm -rf tests/test_cases_auth/images