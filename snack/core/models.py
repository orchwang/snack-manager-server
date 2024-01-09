from django.contrib.auth.models import AbstractUser
from django.db import models

from snack.core.constants import MemberType


class User(AbstractUser):
    is_deleted = models.BooleanField(default=False, help_text='Who leaved this project.')
    member_type = models.CharField(
        max_length=10, choices=MemberType.choices, default=MemberType.MEMBER, help_text='회원 등급'
    )
