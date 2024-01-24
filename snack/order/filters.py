import django_filters

from snack.order.constants import OrderStatus
from snack.order.models import Order


class OrderFilter(django_filters.FilterSet):
    uid = django_filters.CharFilter()
    status = django_filters.ChoiceFilter(choices=OrderStatus.choices)
    created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['uid', 'status', 'created_at']
