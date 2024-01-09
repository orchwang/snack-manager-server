from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from snack.order.serializers.order_serializers import SnackSerializer
from snack.order.models import Snack


@extend_schema(description='등록된 간식 목록을 불러옵니다.')
class SnackListView(generics.ListAPIView):
    queryset = Snack.objects.all()
    serializer_class = SnackSerializer
    permission_classes = [IsAuthenticated]
