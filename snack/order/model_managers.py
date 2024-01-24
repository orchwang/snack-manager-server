from django.db import models

from snack.order.constants import OrderStatus


class SnackManager(models.Manager):
    pass


class OrderManager(models.Manager):
    def not_delivered(self):
        """
        배송 시작 전 모든 주문 필터링
        - 아직 배송 전인 주문 내 간식을 중복 재주문 방지하기 위함
        - CANCELED, COMPLETED 는 체크 프로세스에서 제외
        """
        not_delivered_statuses = [OrderStatus.CREATED, OrderStatus.APPROVED, OrderStatus.ORDERED, OrderStatus.SHIPPING]
        return self.filter(status__in=not_delivered_statuses)
