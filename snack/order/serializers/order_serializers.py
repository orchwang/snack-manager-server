from typing import Optional, List

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
    estimated_arrival_time = serializers.DateTimeField()

    def get_user_email(self, obj):
        return obj.user.email


class SnackOrderSerializer(serializers.Serializer):
    uid = serializers.CharField()
    quantity = serializers.IntegerField()


class OrderWriteSerializer(serializers.Serializer):
    snacks = SnackOrderSerializer(many=True)

    def create(self, validated_data):
        snacks_list = validated_data.get('snacks')
        if not snacks_list:
            raise InvalidRequest('You cannot order without snacks.')

        # self._check_not_delivered_orders_exists()

        snack_instance_list = self._check_snack_list_valid(snacks_list)

        order = Order.objects.create(user=validated_data.get('user'))

        self._make_purchases(order, snack_instance_list)

        return order

    def _check_not_delivered_orders_exists(self):
        not_delivered_orders = Order.objects.not_delivered().count()
        if not_delivered_orders:
            raise InvalidRequest('You cannot order when not delivered orders are exists.')

    def _check_snack_list_valid(self, snacks_list: List):
        not_delivered_orders = Order.objects.not_delivered().values_list('id', flat=True)
        snack_ids_in_not_delivered_orders = Purchase.objects.filter(order_id__in=not_delivered_orders).values_list(
            'snack_id', flat=True
        )

        snack_instance_list = []
        for snack in snacks_list:
            try:
                created_snack = Snack.objects.get(uid=snack.get('uid'))

                # 배송 시작 전 주문에 이미 존재하는 간식 여부 검사
                if created_snack.id in snack_ids_in_not_delivered_orders:
                    raise InvalidRequest('You cannot order when not delivered snack is in your order.')

                # 좋아요 비율 검사
                if created_snack.like_ratio < 1:
                    raise InvalidRequest('Rated with hate reactions more than like cannot be ordered.')

                snack_instance_list.append({'snack': created_snack, 'quantity': snack.get('quantity')})
            except Snack.DoesNotExist:
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
        if (
            status_to_update in [OrderStatus.APPROVED.value, OrderStatus.ORDERED.value]
            and instance.check_has_hated_snacks()
        ):
            raise InvalidRequest('Your order has hated snacks')
        instance.update_status(status_to_update, estimated_arrival_time)

        return Order.objects.get(pk=instance.pk)
