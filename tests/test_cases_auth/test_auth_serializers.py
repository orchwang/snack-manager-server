import pytest

from django.contrib.auth import get_user_model

from snack.core.serializers.user_serializers import UserProfileSerializer

User = get_user_model()


class TestCartSerializers:
    @pytest.mark.django_db
    def test_cart_serializers_return_data(self, member_user_1):
        serializer = UserProfileSerializer(member_user_1)
        user_data = serializer.data

        assert user_data['username'] == member_user_1.username
        assert user_data['email'] == member_user_1.email
