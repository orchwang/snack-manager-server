#!/bin/bash

poetry run celery -A snack worker -l info
