from rest_framework import serializers

from snack.order.models import Order, Cart
from snack.order.serializers.snack_serializers import SnackSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    snack = SnackSerializer()
    order = OrderSerializer()

    class Meta:
        model = Cart
        fields = '__all__'
