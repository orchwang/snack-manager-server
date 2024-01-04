from django.db import models


class Currency(models.TextChoices):
    KRW = "KRW"
    USD = "USD"
    JPY = "JPY"
