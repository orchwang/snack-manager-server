from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema

from snack.core.permissions import IsAdmin
from snack.core.serializers.user_serializers import CreateUserSerializer, UserProfileSerializer

User = get_user_model()


class IsAdminCheckView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, format=None):
        return Response({'detail': 'Success'}, status=status.HTTP_200_OK)


class AuthenticationCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({'detail': 'Success'}, status=status.HTTP_200_OK)


class UserSignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer


@extend_schema(
    description='특정 사용자의 상세 정보를 가져옵니다.',
    responses={200: UserProfileSerializer},
)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
