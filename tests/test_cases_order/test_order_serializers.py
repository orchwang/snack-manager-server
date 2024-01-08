import pytest

from snack.order.serializers.order_serializers import CartSerializer
from snack.order.models import Cart


class TestCartSerializers:
    @pytest.mark.django_db
    def test_order_list_serializers_return_data(self, dummy_orders_set_1):
        cart = Cart.objects.filter(order=dummy_orders_set_1[0]).all()
        serializer = CartSerializer(cart, many=True)

        for item in serializer.data:
            assert item.get('quantity') == 1
            assert item.get('order').get('uid') == dummy_orders_set_1[0].uid
