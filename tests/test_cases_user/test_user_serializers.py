import pytest

from django.contrib.auth import get_user_model

from snack.core.serializers.user_serializers import UserWriteSerializer


class TestUserWriteSerializer:
    @pytest.mark.django_db
    def test_create_user_serializer(self):
        data = {
            'username': 'test_username',
            'password': 'test_password',
            'email': 'test_email@test.com',
        }

        serializer = UserWriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        User = get_user_model()
        user = User.objects.get(email=data['email'])

        assert user
        assert user.email == data['email']
        assert user.username == data['username']
