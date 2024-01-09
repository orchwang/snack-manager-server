from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from snack.core.permissions import IsAdmin
from snack.core.serializers.user_serializers import CreateUserSerializer


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
