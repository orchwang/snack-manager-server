from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from snack.order.serializers.order_serializers import CartSerializer
from snack.order.models import Cart


class CartListView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
