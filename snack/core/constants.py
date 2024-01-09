from django.db import models


class MemberType(models.TextChoices):
    MEMBER = 'MEMBER'
    ADMIN = 'ADMIN'
