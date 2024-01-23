import pytest
from django.utils import timezone

from snack.order.serializers.order_serializers import (
    PurchaseSerializer,
    OrderSerializer,
    OrderDetailSerializer,
    OrderStatusUpdateSerializer,
)
from snack.order.models import Purchase, Order
from snack.order.serializers.snack_serializers import SnackReactionSerializer, SnackReactionWriteSerializer
from snack.order.constants import SnackReactionType, OrderStatus


class TestPurchaseSerializers:
    @pytest.mark.django_db
    def test_puchase_serializers_return_data(self, dummy_orders_set_1):
        purchases = Purchase.objects.filter(order=dummy_orders_set_1[0]).all()
        serializer = PurchaseSerializer(purchases, many=True)

        for item in serializer.data:
            assert item.get('quantity') == 1
            assert item.get('order') == dummy_orders_set_1[0].id
            assert item.get('snack').get('uid')
            assert item.get('snack').get('name')
            assert item.get('snack').get('url')
            assert item.get('snack').get('desc')
            assert item.get('snack').get('image')
            assert item.get('snack').get('currency')
            assert item.get('snack').get('price')


class TestOrderSerializers:
    @pytest.mark.django_db
    def test_order_serializers_return_data(self, dummy_orders_set_1):
        serializer = OrderSerializer(dummy_orders_set_1, many=True)

        for item in serializer.data:
            order = Order.objects.get(uid=item['uid'])
            assert item.get('uid') == order.uid


class TestOrderDetailSerializers:
    @pytest.mark.django_db
    def test_order_detail_serializers_return_order_data_with_related_snack_list(
        self, dummy_orders_set_1, dummy_snacks_set_1
    ):
        prefetched_queryset = Order.objects.prefetch_related('purchase_set__snack').get(id=dummy_snacks_set_1[0].id)
        serializer = OrderDetailSerializer(prefetched_queryset)

        data = serializer.data
        order = Order.objects.get(uid=dummy_orders_set_1[0].uid)
        assert data.get('uid') == order.uid
        assert data.get('status') == order.status
        purchases = data.get('purchase_set')
        ordered_purchases = Purchase.objects.filter(order__uid=dummy_orders_set_1[0].uid).values()
        assert len(purchases) == len(ordered_purchases)
        for i in range(len(purchases)):
            snack = purchases[i].get('snack')
            order = purchases[i].get('order')
            assert order == dummy_orders_set_1[0].id
            assert snack.get('id') == ordered_purchases[i]['snack_id']

    @pytest.mark.django_db
    def test_order_detail_serializers_return_many_order_data_with_related_snack_list(
        self, dummy_orders_set_1, dummy_snacks_set_1
    ):
        prefetched_queryset = Order.objects.prefetch_related('purchase_set__snack').all()
        serializer = OrderDetailSerializer(prefetched_queryset, many=True)

        data = serializer.data
        for i in range(len(data)):
            order = Order.objects.get(uid=dummy_orders_set_1[i].uid)
            assert data[i].get('uid') == order.uid
            assert data[i].get('status') == order.status
            purchases = data[i].get('purchase_set')
            ordered_purchases = Purchase.objects.filter(order__uid=dummy_orders_set_1[i].uid).values()

            # test purhcase_set data are valid
            assert len(purchases) == len(ordered_purchases)
            for j in range(len(purchases)):
                snack = purchases[j].get('snack')
                order = purchases[j].get('order')
                assert order == dummy_orders_set_1[i].id
                assert snack.get('id') == ordered_purchases[j]['snack_id']


class TestSnackReactionSerializer:
    @pytest.mark.django_db
    def test_snack_reaction_serializer_with_single_snack_reaction_return_valid_data(self, dummy_snacks_reaction_set_1):
        serializer = SnackReactionSerializer(dummy_snacks_reaction_set_1[0])
        data = serializer.data
        assert data['id'] == dummy_snacks_reaction_set_1[0].id
        assert data['snack'] == dummy_snacks_reaction_set_1[0].snack.id
        assert data['type'] == dummy_snacks_reaction_set_1[0].type


class TestCreateSnackReactionSerializer:
    @pytest.mark.django_db
    def test_create_snack_reaction_serializer_create_valid_data(self, dummy_snacks_set_1, member_user_1):
        serializer = SnackReactionWriteSerializer(
            data={
                'snack': dummy_snacks_set_1[0].uid,
                'user': member_user_1.id,
                'type': SnackReactionType.HATE,
            }
        )
        serializer.is_valid()
        result = serializer.save()
        assert result.snack.uid == dummy_snacks_set_1[0].uid
        assert result.user.id == member_user_1.id
        assert result.type == SnackReactionType.HATE


class TestOrderStatusUpdateSerializer:
    @pytest.mark.django_db
    def test_order_status_update_serializer_update_success(self, dummy_orders_set_1):
        order = dummy_orders_set_1[0]
        order.status = OrderStatus.SHIPPING
        order.save()

        now = timezone.now()
        serializer = OrderStatusUpdateSerializer(
            dummy_orders_set_1[0],
            data={'status': OrderStatus.COMPLETED, 'estimated_arrival_time': now},
        )
        serializer.is_valid()
        result = serializer.save()
        assert result.status == OrderStatus.COMPLETED
