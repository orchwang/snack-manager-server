import os
import uuid

from django.conf import settings
from django.db import models
from shortuuid.django_fields import ShortUUIDField

from snack.order.constants import Currency, OrderStatus, SnackReactionType


def snack_image_path(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    return f'images/snack/{str(uuid.uuid4())}{file_extension}'


class Snack(models.Model):
    uid = ShortUUIDField(unique=True, editable=False)
    name = models.CharField(unique=True, max_length=128, blank=True, help_text='Snack name.')
    url = models.CharField(max_length=500, blank=True, help_text='A url for buy the snack.')
    desc = models.TextField(blank=True, help_text='Snack description')
    image = models.ImageField(upload_to=snack_image_path)
    currency = models.CharField(max_length=4, choices=Currency.choices, default=Currency.KRW)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['uid']),
        ]

    def __str__(self):
        return self.name


class SnackReaction(models.Model):
    snack = models.ForeignKey(Snack, on_delete=models.CASCADE, to_field='uid', related_name='snack_reactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=SnackReactionType.choices, default=SnackReactionType.LIKE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['snack']),
        ]


class Order(models.Model):
    uid = ShortUUIDField(unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.CREATED)
    purchases = models.ManyToManyField(
        Snack,
        related_name='snacks',
        through='Purchase',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['uid']),
        ]

    def __str__(self):
        return f'{self.uid}'


class Purchase(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    snack = models.ForeignKey(Snack, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
