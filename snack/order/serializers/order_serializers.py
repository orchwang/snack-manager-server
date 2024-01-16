from rest_framework import serializers

from snack.order.models import Purchase
from snack.order.constants import OrderStatus
from snack.order.serializers.snack_serializers import SnackSerializer


class OrderSerializer(serializers.Serializer):
    uid = serializers.CharField()
    status = serializers.ChoiceField(choices=OrderStatus.choices)
    user_id = serializers.IntegerField()
    user_email = serializers.SerializerMethodField()

    def get_user_email(self, obj):
        return obj.user.email


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
