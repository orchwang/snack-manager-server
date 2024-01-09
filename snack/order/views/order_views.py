from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from snack.order.serializers.order_serializers import OrderSerializer
from snack.order.models import Order


class CartListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class RetrieveOrderView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'
