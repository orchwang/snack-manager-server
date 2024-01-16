from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from snack.order.serializers.snack_serializers import SnackSerializer, CreateSnackSerializer
from snack.order.models import Snack


@extend_schema(description='등록된 간식 목록을 불러옵니다.', responses={200: SnackSerializer}, methods=['GET'])
@extend_schema(
    description='새로운 간식을 등록합니다.',
    request=CreateSnackSerializer,
    responses={201: SnackSerializer},
    methods=['POST'],
)
class SnackListView(generics.ListCreateAPIView):
    queryset = Snack.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateSnackSerializer
        return SnackSerializer
