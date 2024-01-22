from typing import Optional, List

from rest_framework import serializers

from snack.core.exceptions import InvalidRequest
from snack.order.models import Purchase, Order, Snack, SnackReaction
from snack.order.constants import OrderStatus, SnackReactionType
from snack.order.serializers.snack_serializers import SnackSerializer


class OrderSerializer(serializers.Serializer):
    uid = serializers.CharField()
    status = serializers.ChoiceField(choices=OrderStatus.choices)
    user_id = serializers.IntegerField()
    user_email = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    estimated_arrival_time = serializers.DateTimeField()

    def get_user_email(self, obj):
        return obj.user.email


class SnackOrderSerializer(serializers.Serializer):
    uid = serializers.CharField()
    quantity = serializers.IntegerField()


class OrderWriteSerializer(serializers.Serializer):
    snacks = SnackOrderSerializer(many=True)

    def create(self, validated_data):
        order = Order.objects.create(user=validated_data.get('user'))

        snacks_list = validated_data.get('snacks')
        if not snacks_list:
            order.delete()
            raise InvalidRequest('You cannot order without snacks.')

        snack_instance_list = self._check_snack_list_valid(order, snacks_list)

        self._make_purchases(order, snack_instance_list)

        return order

    def _check_snack_list_valid(self, order: Optional[Order], snacks_list: List):
        snack_instance_list = []
        for snack in snacks_list:
            try:
                created_snack = Snack.objects.get(uid=snack.get('uid'))
                like_snack_reaction_count = SnackReaction.objects.filter(
                    snack=created_snack, type=SnackReactionType.LIKE
                ).count()
                hate_snack_reaction_count = SnackReaction.objects.filter(
                    snack=created_snack, type=SnackReactionType.HATE
                ).count()
                if hate_snack_reaction_count > like_snack_reaction_count:
                    raise InvalidRequest('Rated with hate reactions more than like cannot be ordered.')
                snack_instance_list.append({'snack': created_snack, 'quantity': snack.get('quantity')})
            except Snack.DoesNotExist:
                order.delete()
                raise InvalidRequest('There are invalid snacks in your request.')
        return snack_instance_list

    def _make_purchases(self, order: Optional[Order], snacks_list: List):
        for item in snacks_list:
            purchase = Purchase(order=order, snack=item.get('snack'), quantity=item.get('quantity'))
            purchase.save()


class OrderUpdateSerializer(serializers.Serializer):
    snacks = SnackOrderSerializer(many=True)


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
    estimated_arrival_time = serializers.DateTimeField()
    purchase_set = PurchaseSerializer(many=True, read_only=True)

    def get_user_email(self, obj):
        return obj.user.email


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)
    estimated_arrival_time = serializers.DateTimeField()

    def update(self, instance, validated_data):
        status_to_update = validated_data.get('status')
        estimated_arrival_time = validated_data.get('estimated_arrival_time')
        instance.update_status(status_to_update, estimated_arrival_time)

        return Order.objects.get(pk=instance.pk)
