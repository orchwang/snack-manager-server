from datetime import datetime
from typing import Optional

from django.apps import apps
from django.contrib.auth import get_user_model

from snack.order.constants import OrderStatus, SnackReactionType

from snack.order.exceptions import InvalidOrderStatusFlow

User = get_user_model()


class SnackMixin:
    def get_like_reaction_count(self) -> int:
        SnackReaction = apps.get_model('order', 'SnackReaction')
        return SnackReaction.objects.filter(snack=self, type=SnackReactionType.LIKE).count()

    def get_hate_reaction_count(self) -> int:
        SnackReaction = apps.get_model('order', 'SnackReaction')
        return SnackReaction.objects.filter(snack=self, type=SnackReactionType.HATE).count()


class OrderMixin:
    def update_status(self, status: Optional[OrderStatus], estimated_arrival_time: datetime):
        if status == OrderStatus.CANCELLED:
            self.cancel()
        if status == OrderStatus.APPROVED:
            self.approve()
        if status == OrderStatus.ORDERED:
            self.order(estimated_arrival_time)
        if status == OrderStatus.SHIPPING:
            self.ship(estimated_arrival_time)
        if status == OrderStatus.COMPLETED:
            self.complete()

    def cancel(self):
        if self.status not in [OrderStatus.CREATED, OrderStatus.APPROVED]:
            raise InvalidOrderStatusFlow(f'{self.status} order cannot change to {OrderStatus.CANCELLED}')
        self.status = OrderStatus.CANCELLED
        self.save()

    def approve(self):
        if self.status not in [OrderStatus.CREATED]:
            raise InvalidOrderStatusFlow(f'{self.status} order cannot change to {OrderStatus.APPROVED}')
        self.status = OrderStatus.APPROVED
        self.save()

    def order(self, estimated_arrival_time: datetime):
        if not estimated_arrival_time:
            raise InvalidOrderStatusFlow('Estimated arrival time is needed.')
        if self.status not in [OrderStatus.APPROVED]:
            raise InvalidOrderStatusFlow(f'{self.status} order cannot change to {OrderStatus.ORDERED}')
        self.status = OrderStatus.ORDERED
        self.estimated_arrival_time = estimated_arrival_time
        self.save()

    def ship(self, estimated_arrival_time: datetime):
        if not estimated_arrival_time:
            raise InvalidOrderStatusFlow('Estimated arrival time is needed.')
        if self.status not in [OrderStatus.ORDERED]:
            raise InvalidOrderStatusFlow(f'{self.status} order cannot change to {OrderStatus.SHIPPING}')
        self.status = OrderStatus.SHIPPING
        self.estimated_arrival_time = estimated_arrival_time
        self.save()

    def complete(self):
        if self.status not in [OrderStatus.SHIPPING]:
            raise InvalidOrderStatusFlow(f'{self.status} order cannot change to {OrderStatus.COMPLETED}')
        self.status = OrderStatus.COMPLETED
        self.save()
