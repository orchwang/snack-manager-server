from rest_framework import serializers

from snack.order.models import Purchase
from snack.order.constants import OrderStatus
from snack.order.serializers.snack_serializers import SnackSerializer


class OrderSerializer(serializers.Serializer):
    """
    Order + Snack queryset
    """

    uid = serializers.CharField()
    status = serializers.ChoiceField(choices=OrderStatus.choices)
    user_id = serializers.IntegerField()
    user_email = serializers.SerializerMethodField()

    def get_user_email(self, obj):
        return obj.user.email


class PurchaseSerializer(serializers.ModelSerializer):
    snack = SnackSerializer()
    order = OrderSerializer()

    class Meta:
        model = Purchase
        fields = '__all__'


class OrderDetailSerializer(serializers.Serializer):
    uid = serializers.CharField()
    status = serializers.ChoiceField(choices=OrderStatus.choices)
    user_id = serializers.IntegerField()
    user_email = serializers.SerializerMethodField()
    snacks = SnackSerializer(many=True)

    def get_user_email(self, obj):
        return obj.user.email
