from rest_framework import serializers

from snack.core.exceptions import InvalidRequest
from snack.order.models import Purchase, Order, Snack
from snack.order.constants import OrderStatus
from snack.order.serializers.snack_serializers import SnackSerializer


class OrderSerializer(serializers.Serializer):
    uid = serializers.CharField()
    status = serializers.ChoiceField(choices=OrderStatus.choices)
    user_id = serializers.IntegerField()
    user_email = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_user_email(self, obj):
        return obj.user.email


class SnackOrderSerializer(serializers.Serializer):
    uid = serializers.CharField()
    quantity = serializers.IntegerField()


class CreateOrderSerializer(serializers.Serializer):
    snacks = SnackOrderSerializer(many=True)

    def create(self, validated_data):
        order = Order.objects.create(user=validated_data.get('user'))

        snacks_list = validated_data.get('snacks')
        if not snacks_list:
            order.delete()
            raise InvalidRequest('You cannot order without snacks.')

        for snack in snacks_list:
            try:
                created_snack = Snack.objects.get(uid=snack.get('uid'))
                purchase = Purchase(order=order, snack=created_snack, quantity=snack.get('quantity'))
                purchase.save()
            except Snack.DoesNotExist:
                order.delete()
                raise InvalidRequest('There are invalid snacks in your request.')

        return order


class PurchaseSerializer(serializers.ModelSerializer):
    snack = SnackSerializer()

    class Meta:
        model = Purchase
        fields = '__all__'


class OrderDetailSerializer(serializers.Serializer):
    uid = serializers.CharField()
    user_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=OrderStatus.choices)
    user_email = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    purchase_set = PurchaseSerializer(many=True, read_only=True)

    def get_user_email(self, obj):
        return obj.user.email
