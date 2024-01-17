from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

from snack.order.serializers.order_serializers import (
    OrderSerializer,
    OrderDetailSerializer,
    CreateOrderSerializer,
)
from snack.order.serializers.snack_serializers import SnackDetailSerializer
from snack.order.models import Order, Snack


@extend_schema(description='등록된 간식 주문 목록을 불러옵니다.', responses={200: OrderSerializer}, methods=['GET'])
@extend_schema(
    description='새로운 주문을 등록합니다.',
    request=CreateOrderSerializer,
    responses={201: OrderDetailSerializer},
    methods=['POST'],
)
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        response_serializer = OrderDetailSerializer(obj)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


@extend_schema(description='특정 간식 주문의 상세 내역을 불러옵니다. 주문 데이터 개요와 선택한 간식 목록이 포함됩니다.')
class RetrieveOrderView(generics.RetrieveAPIView):
    queryset = Order.objects.prefetch_related('purchase_set__snack')
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'


@extend_schema(description='특정 간식의 상세 내역을 불러옵니다.')
class RetrieveSnackView(generics.RetrieveAPIView):
    queryset = Snack.objects
    serializer_class = SnackDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'
