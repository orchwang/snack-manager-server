from datetime import datetime
from typing import Optional

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache

from snack.order.constants import OrderStatus, SnackReactionType
from snack.order.exceptions import InvalidOrderStatusFlow, InvalidSnackReaction
from snack.order.tasks import update_snack_reaction_statistics

User = get_user_model()


class SnackMixin:
    def get_like_reaction_count(self) -> int:
        SnackReaction = apps.get_model('order', 'SnackReaction')
        return SnackReaction.objects.filter(snack=self, type=SnackReactionType.LIKE).count()

    def get_hate_reaction_count(self) -> int:
        SnackReaction = apps.get_model('order', 'SnackReaction')
        return SnackReaction.objects.filter(snack=self, type=SnackReactionType.HATE).count()

    def toggle_reaction(self, user: Optional[User], reaction_type: Optional[SnackReactionType]):
        SnackReaction = apps.get_model('order', 'SnackReaction')
        snack_reaction, is_created = SnackReaction.objects.get_or_create(snack_id=self.id, user=user)
        if not is_created and snack_reaction.type == reaction_type:
            raise InvalidSnackReaction('You cannot react same reaction.')

        snack_reaction.type = reaction_type
        snack_reaction.save()

        self._process_cache(reaction_type, self)

        if not settings.CELERY_DEBUG:
            update_snack_reaction_statistics.delay(self.uid)

    def _process_cache(self, reaction_type: Optional[SnackReactionType], snack):
        cache.get_or_set(f'{snack.uid}-{SnackReactionType.LIKE.value}', 0)
        cache.get_or_set(f'{snack.uid}-{SnackReactionType.HATE.value}', 0)
        if reaction_type == SnackReactionType.LIKE:
            cache.incr(f'{snack.uid}-{SnackReactionType.LIKE.value}', 1)
            cache.decr(f'{snack.uid}-{SnackReactionType.HATE.value}', 1)
        elif reaction_type == SnackReactionType.HATE:
            cache.incr(f'{snack.uid}-{SnackReactionType.HATE.value}', 1)
            cache.decr(f'{snack.uid}-{SnackReactionType.LIKE.value}', 1)

        snack.like_reaction_count = cache.get(f'{snack.uid}-{SnackReactionType.LIKE.value}')
        snack.hate_reaction_count = cache.get(f'{snack.uid}-{SnackReactionType.HATE.value}')
        snack.save()


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
        purchases = self.purchases.all()
        for snack in purchases:
            if snack.like_ratio < 1:
                return True
        return False
