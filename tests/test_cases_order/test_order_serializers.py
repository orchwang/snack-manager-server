import pytest

from snack.order.serializers.order_serializers import PurchaseSerializer, OrderSerializer
from snack.order.models import Purchase, Order


class TestPurchaseSerializers:
    @pytest.mark.django_db
    def test_puchase_serializers_return_data(self, dummy_orders_set_1):
        purchases = Purchase.objects.filter(order=dummy_orders_set_1[0]).all()
        serializer = PurchaseSerializer(purchases, many=True)

        for item in serializer.data:
            assert item.get('quantity') == 1
            assert item.get('order').get('uid') == dummy_orders_set_1[0].uid
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
