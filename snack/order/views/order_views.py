from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from snack.order.serializers.order_serializers import OrderSerializer, PurchaseSerializer
from snack.order.models import Order, Purchase


@extend_schema(description='간식 주문 목록을 불러옵니다.')
class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(description='주문-간식 데이터 목록을 불러옵니다.')
class PurchaseListView(generics.ListAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(description='특정 간식 주문의 상세 내역을 불러옵니다.')
class RetrieveOrderView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'
