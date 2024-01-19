from typing import Optional

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema

from snack.core.constants import MemberType
from snack.core.exceptions import ResignFailed
from snack.core.permissions import IsAdmin, IsActive
from snack.core.serializers.user_serializers import (
    UserWriteSerializer,
    UserProfileSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)
from snack.core.serializers.general_serializers import ResponseDetailSerializer

User = get_user_model()


class IsAdminCheckView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, format=None):
        return Response({'detail': 'Success'}, status=status.HTTP_200_OK)


class AuthenticationCheckView(APIView):
    permission_classes = [IsAuthenticated, IsActive]

    def get(self, request, format=None):
        return Response({'detail': 'Success'}, status=status.HTTP_200_OK)


class UserSignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserWriteSerializer


@extend_schema(
    description='특정 사용자의 상세 정보를 가져옵니다.',
    responses={
        200: UserProfileSerializer,
        400: ResponseDetailSerializer,
    },
)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated, IsActive]

    def get(self, request):
        serializer = UserProfileSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    queryset = User.objects
    permission_classes = [IsAuthenticated, IsActive]
    serializer_class = UserListSerializer


class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects
    permission_classes = [IsAuthenticated, IsActive, IsAdmin]
    serializer_class = UserUpdateSerializer
    lookup_field = 'id'


class UserResignView(APIView):
    """
    TODO: RESTful 을 유지하기 위해 /users/ endpoint 를 이용할 수도 있지만,
          별개의 API View 를 사용하기 위해 별도 endpoint 를 사용함.
          이후 리팩토링 여지 있음.
    """

    permission_classes = [IsAuthenticated, IsActive]

    def delete(self, request):
        member_type = request.user.member_type

        self._check_last_admin(member_type)

        self._set_user_inactive(request.user)

        return Response({'detail': f'User "{request.user.username}" resigned'}, status=status.HTTP_200_OK)

    def _check_last_admin(self, member_type):
        admin_count = 0
        if member_type == MemberType.ADMIN:
            admin_count = User.objects.filter(member_type=MemberType.ADMIN).count()
        if admin_count > 0:
            raise ResignFailed('You cannot resign because you are the last admin.')

    def _set_user_inactive(self, user: Optional[User]):
        user.is_deleted = True
        user.is_active = False
        user.save()
