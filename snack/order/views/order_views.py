from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from snack.core.exceptions import InvalidRequest
from snack.core.permissions import IsActive, IsAdmin
from snack.order.filters import OrderFilter
from snack.order.serializers.order_serializers import (
    OrderSerializer,
    OrderDetailSerializer,
    OrderWriteSerializer,
    OrderUpdateSerializer,
    OrderStatusUpdateSerializer,
)
from snack.order.serializers.snack_serializers import SnackDetailSerializer
from snack.order.models import Order, Snack, Purchase


@extend_schema(description='등록된 간식 주문 목록을 불러옵니다.', responses={200: OrderSerializer}, methods=['GET'])
@extend_schema(
    description='새로운 주문을 등록합니다.',
    request=OrderWriteSerializer,
    responses={201: OrderDetailSerializer},
    methods=['POST'],
)
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsActive]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = OrderFilter
    ordering_fields = ['created_at', 'uid']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        response_serializer = OrderDetailSerializer(obj)

        created_instance = response_serializer.instance
        created_instance.year = created_instance.created_at.year
        created_instance.month = created_instance.created_at.month
        created_instance.day = created_instance.created_at.day
        created_instance.save()

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderWriteSerializer
        return OrderSerializer


@extend_schema(description='특정 간식 주문의 상세 내역을 불러옵니다. 주문 데이터 개요와 선택한 간식 목록이 포함됩니다.')
@extend_schema(
    description='특정 주문의 주문 내역을 업데이트 합니다.',
    request=OrderUpdateSerializer,
    responses={200: OrderDetailSerializer},
    methods=['PUT'],
)
class RetrieveUpdateOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.prefetch_related('purchase_set__snack')
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated, IsActive]
    lookup_field = 'uid'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        snacks_list = request.data.get('snacks')

        self._check_payload_is_valid(snacks_list)

        self._remove_existing_purchases(instance)

        self._create_new_purchases(instance, snacks_list)

        updated_order = Order.objects.get(uid=instance.uid)
        serializer = self.get_serializer(updated_order)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def _check_payload_is_valid(self, snacks_list):
        if not snacks_list:
            raise InvalidRequest('You cannot order without snacks.')
        for snack in snacks_list:
            try:
                Snack.objects.filter(uid=snack.get('uid')).get()
            except Snack.DoesNotExist:
                raise InvalidRequest('There are invalid snacks in your request.')

    def _remove_existing_purchases(self, order):
        existing_purchases = Purchase.objects.filter(order=order).all()
        existing_purchases.delete()

    def _create_new_purchases(self, order, snacks_list):
        for snack in snacks_list:
            created_snack = Snack.objects.get(uid=snack.get('uid'))
            purchase = Purchase(order=order, snack=created_snack, quantity=snack.get('quantity'))
            purchase.save()


@extend_schema(description='특정 간식의 상세 내역을 불러옵니다.')
class RetrieveSnackView(generics.RetrieveAPIView):
    queryset = Snack.objects
    serializer_class = SnackDetailSerializer
    permission_classes = [IsAuthenticated, IsActive]
    lookup_field = 'uid'


@extend_schema(description='특정 간식의 상세 내역을 불러옵니다.')
class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsActive, IsAdmin]
    lookup_field = 'uid'
