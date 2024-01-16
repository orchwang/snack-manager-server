from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from snack.order.serializers.order_serializers import OrderSerializer, PurchaseSerializer, OrderDetailSerializer
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


@extend_schema(description='특정 간식 주문의 상세 내역을 불러옵니다. 주문 데이터 개요와 선택한 간식 목록이 포함됩니다.')
class RetrieveOrderView(generics.RetrieveAPIView):
    queryset = Order.objects.prefetch_related('purchase_set__snack').all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'
