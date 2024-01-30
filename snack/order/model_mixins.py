from datetime import datetime
from typing import Optional

from django_redis import get_redis_connection

from django.apps import apps
from django.contrib.auth import get_user_model

from snack.order.constants import OrderStatus, SnackReactionType
from snack.order.exceptions import InvalidOrderStatusFlow, InvalidSnackReaction

User = get_user_model()


class SnackMixin:
    def get_like_reaction_count(self) -> int:
        SnackReaction = apps.get_model('order', 'SnackReaction')
        return SnackReaction.objects.filter(snack=self, type=SnackReactionType.LIKE).count()

    def get_hate_reaction_count(self) -> int:
        SnackReaction = apps.get_model('order', 'SnackReaction')
        return SnackReaction.objects.filter(snack=self, type=SnackReactionType.HATE).count()

    def toggle_reaction(self, user: Optional[User], reaction_type: Optional[SnackReactionType]):
        like_key = f'snack:like:{self.id}'
        hate_key = f'snack:hate:{self.id}'

        redis_con = get_redis_connection('default')

        if reaction_type == SnackReactionType.LIKE:
            if not redis_con.sismember(like_key, user.id):
                redis_con.sadd(like_key, user.id)
                redis_con.srem(hate_key, user.id)
            else:
                raise InvalidSnackReaction('Cannot add same reaction.')

        if reaction_type == SnackReactionType.HATE:
            if not redis_con.sismember(hate_key, user.id):
                redis_con.sadd(hate_key, user.id)
                redis_con.srem(like_key, user.id)
            else:
                raise InvalidSnackReaction('Cannot add same reaction.')

        like_count = redis_con.scard(like_key)
        hate_count = redis_con.scard(hate_key)
        like_ratio = (like_count or 1) / (hate_count or 1)

        self.like_reaction_count = like_count
        self.hate_reaction_count = hate_count
        self.like_ratio = like_ratio
        self.save()

        # if not settings.CELERY_DEBUG:
        #     update_snack_reaction_statistics.delay(self.uid)


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

    def check_has_hated_snacks(self) -> bool:
        Snack = apps.get_model('order', 'Snack')
        snack_ids_list = self.purchases.values_list('id', flat=True)
        hated_snacks_count = Snack.objects.filter(id__in=snack_ids_list).filter(like_ratio__lt=1).count()
        if not hated_snacks_count:
            return False
        return True
