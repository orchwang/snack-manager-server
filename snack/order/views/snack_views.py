from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from snack.order.serializers.order_serializers import SnackSerializer
from snack.order.models import Snack


class SnackListView(generics.ListAPIView):
    queryset = Snack.objects.all()
    serializer_class = SnackSerializer
    permission_classes = [IsAuthenticated]
