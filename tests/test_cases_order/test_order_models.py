import pytest
from django.utils import timezone

from snack.order.constants import OrderStatus
from snack.order.models import Order
from snack.order.exceptions import InvalidOrderStatusFlow


class TestOrderModelMixins:
    @pytest.mark.django_db
    def test_update_order_status_to_order_success(self, dummy_orders_set_1, member_user_1):
        order = dummy_orders_set_1[0]
        order.status = OrderStatus.APPROVED
        order.save()

        assert order.status == OrderStatus.APPROVED

        now = timezone.now()
        estimated_arrival_date = now + timezone.timedelta(weeks=1)

        order.order(estimated_arrival_date)

        updated_order = Order.objects.get(id=dummy_orders_set_1[0].id)
        assert updated_order.status == OrderStatus.ORDERED

    @pytest.mark.django_db
    def test_update_order_status_to_order_failed(self, dummy_orders_set_1, member_user_1):
        order = dummy_orders_set_1[0]
        order.status = OrderStatus.ORDERED
        order.save()

        now = timezone.now()
        estimated_arrival_date = now + timezone.timedelta(weeks=1)

        with pytest.raises(InvalidOrderStatusFlow) as e:
            order.order(estimated_arrival_date)

        assert str(e) == "<ExceptionInfo InvalidOrderStatusFlow('ORDERED order cannot change to ORDERED') tblen=2>"

    @pytest.mark.django_db
    def test_update_order_status_to_cancel_success_from_created_status(self, dummy_orders_set_1, member_user_1):
        order = dummy_orders_set_1[0]
        assert order.status == OrderStatus.CREATED

        order.cancel()

        updated_order = Order.objects.get(id=dummy_orders_set_1[0].id)
        assert updated_order.status == OrderStatus.CANCELLED

    @pytest.mark.django_db
    def test_update_order_status_to_cancel_success_from_approved_status(self, dummy_orders_set_1, member_user_1):
        order = dummy_orders_set_1[0]
        order.status = OrderStatus.APPROVED
        order.save()
        assert order.status == OrderStatus.APPROVED

        order.cancel()

        updated_order = Order.objects.get(id=dummy_orders_set_1[0].id)
        assert updated_order.status == OrderStatus.CANCELLED

    @pytest.mark.django_db
    def test_update_order_status_to_cancel_failed(self, dummy_orders_set_1, member_user_1):
        order = dummy_orders_set_1[0]
        order.status = OrderStatus.ORDERED
        order.save()

        with pytest.raises(InvalidOrderStatusFlow) as e:
            order.cancel()

        assert str(e) == "<ExceptionInfo InvalidOrderStatusFlow('ORDERED order cannot change to CANCELLED') tblen=2>"

    @pytest.mark.django_db
    def test_update_order_status_to_approve_success_from_created_status(self, dummy_orders_set_1, member_user_1):
        order = dummy_orders_set_1[0]
        order.status = OrderStatus.CREATED
        order.save()
        assert order.status == OrderStatus.CREATED

        order.approve()

        updated_order = Order.objects.get(id=dummy_orders_set_1[0].id)
        assert updated_order.status == OrderStatus.APPROVED

    @pytest.mark.django_db
    def test_update_order_status_to_approved_failed(self, dummy_orders_set_1, member_user_1):
        order = dummy_orders_set_1[0]
        order.status = OrderStatus.ORDERED
        order.save()

        with pytest.raises(InvalidOrderStatusFlow) as e:
            order.approve()

        assert str(e) == "<ExceptionInfo InvalidOrderStatusFlow('ORDERED order cannot change to APPROVED') tblen=2>"

    @pytest.mark.django_db
    def test_update_order_status_to_ship_success_from_ordered_status(self, dummy_orders_set_1, member_user_1):
        order = dummy_orders_set_1[0]
        order.status = OrderStatus.ORDERED
        order.save()
        assert order.status == OrderStatus.ORDERED

        now = timezone.now()
        estimated_arrival_date = now + timezone.timedelta(weeks=1)

        order.ship(estimated_arrival_date)

        updated_order = Order.objects.get(id=dummy_orders_set_1[0].id)
        assert updated_order.status == OrderStatus.SHIPPING

    @pytest.mark.django_db
    def test_update_order_status_to_shipping_failed(self, dummy_orders_set_1, member_user_1):
        order = dummy_orders_set_1[0]
        order.status = OrderStatus.CREATED
        order.save()

        now = timezone.now()
        estimated_arrival_date = now + timezone.timedelta(weeks=1)

        with pytest.raises(InvalidOrderStatusFlow) as e:
            order.ship(estimated_arrival_date)

        assert str(e) == "<ExceptionInfo InvalidOrderStatusFlow('CREATED order cannot change to SHIPPING') tblen=2>"

    @pytest.mark.django_db
    def test_update_order_status_to_completed_success_from_shipping_status(self, dummy_orders_set_1, member_user_1):
        order = dummy_orders_set_1[0]
        order.status = OrderStatus.SHIPPING
        order.save()
        assert order.status == OrderStatus.SHIPPING

        order.complete()

        updated_order = Order.objects.get(id=dummy_orders_set_1[0].id)
        assert updated_order.status == OrderStatus.COMPLETED

    @pytest.mark.django_db
    def test_update_order_status_to_completed_failed(self, dummy_orders_set_1, member_user_1):
        order = dummy_orders_set_1[0]
        order.status = OrderStatus.CREATED
        order.save()

        with pytest.raises(InvalidOrderStatusFlow) as e:
            order.complete()

        assert str(e) == "<ExceptionInfo InvalidOrderStatusFlow('CREATED order cannot change to COMPLETED') tblen=2>"

    @pytest.mark.django_db
    def test_update_order_to_ordered_with_update_order_success(self, dummy_orders_set_1, member_user_1):
        order = dummy_orders_set_1[0]
        order.status = OrderStatus.APPROVED
        order.save()
        assert order.status == OrderStatus.APPROVED

        now = timezone.now()
        estimated_arrival_date = now + timezone.timedelta(weeks=1)

        order.order(estimated_arrival_date)

        updated_order = Order.objects.get(id=dummy_orders_set_1[0].id)
        assert updated_order.status == OrderStatus.ORDERED


class TestOrderModelManager:
    @pytest.mark.django_db
    def test_order_not_delivered_queryset_response_valid_orders(self, dummy_orders_set_1, member_user_1):
        order_1 = dummy_orders_set_1[0]
        order_2 = dummy_orders_set_1[1]
        order_3 = dummy_orders_set_1[2]
        order_4 = dummy_orders_set_1[3]
        order_5 = dummy_orders_set_1[4]

        order_1.status = OrderStatus.CREATED
        order_2.status = OrderStatus.APPROVED
        order_3.status = OrderStatus.ORDERED
        order_4.status = OrderStatus.SHIPPING
        order_5.status = OrderStatus.COMPLETED

        order_1.save()
        order_2.save()
        order_3.save()
        order_4.save()
        order_5.save()

        not_delivered_orders = Order.objects.not_delivered().all()
        for order in not_delivered_orders:
            assert order.status not in [OrderStatus.CANCELLED, OrderStatus.COMPLETED]
