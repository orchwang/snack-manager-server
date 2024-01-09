from django.db import models


class OrderStatus(models.TextChoices):
    CREATED = 'CREATED'
    ORDERED = 'ORDERED'
    CANCELLED = 'CANCELLED'
    APPROVED = 'APPROVED'
    SHIPPING = 'SHIPPING'
    COMPLETED = 'COMPLETED'


class Currency(models.TextChoices):
    KRW = 'KRW'
    USD = 'USD'
    JPY = 'JPY'
