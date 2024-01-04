from django.conf import settings
from django.db import models
from shortuuid.django_fields import ShortUUIDField


class Snack(models.Model):
    uid = ShortUUIDField(unique=True, editable=False, db_index=True)
    name = models.CharField(max_length=128, help_text="Snack name.")
    url = models.CharField(help_text="A url for buy the snack.")
    image = models.ImageField(upload_to="")
    price = models.FloatField()


class Order(models.Model):
    uid = ShortUUIDField(unique=True, editable=False, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    snacks_cart = models.ManyToManyField(
        Snack,
        through="Cart",
        through_fields=("order", "snack"),
    )


class Cart(models.Model):
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    snack = models.ForeignKey(Snack, on_delete=models.CASCADE)
