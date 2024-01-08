from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_deleted = models.BooleanField(default=False, help_text='Who leaved this project.')
