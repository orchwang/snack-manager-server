from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from snack.core.permissions import IsAdmin


class IsAdminCheckView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, format=None):
        return Response({'detail': 'Success'}, status=status.HTTP_200_OK)
