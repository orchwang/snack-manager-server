import pytest

from django.contrib.auth import get_user_model

from snack.core.serializers.user_serializers import UserProfileSerializer, UserListSerializer

User = get_user_model()


class TestUserProfileSerializer:
    @pytest.mark.django_db
    def test_user_profile_serializers_return_data(self, member_user_1):
        serializer = UserProfileSerializer(member_user_1)
        user_data = serializer.data

        assert user_data['username'] == member_user_1.username
        assert user_data['email'] == member_user_1.email


class TestUserListSerializer:
    @pytest.mark.django_db
    def test_user_list_serializers_return_valid_data(self, member_user_1, member_user_2, member_user_3, member_user_4):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        serialized_data = serializer.data

        users_list = [member_user_1, member_user_2, member_user_3, member_user_4]
        assert len(serialized_data) == len(users_list)
        for i in range(len(serialized_data)):
            serialized_data[i]['username'] == users_list[i].username
            serialized_data[i]['email'] == users_list[i].email
            serialized_data[i]['member_type'] == users_list[i].member_type
            serialized_data[i]['date_joined'] == users_list[i].date_joined
            serialized_data[i]['last_login'] == users_list[i].last_login
