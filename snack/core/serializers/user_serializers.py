from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from snack.core.models import User
from snack.core.constants import MemberType
from snack.core.exceptions import InvalidEmail, InvalidUsername


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data.get('email', None)
        self._check_email_exists(email)

        username = validated_data.get('username', None)
        self._check_username_exists(username)

        user = User.objects.create_user(
            username=validated_data['username'], email=validated_data['email'], password=validated_data['password']
        )

        return user

    def _check_email_exists(self, email: str):
        if User.objects.filter(email=email).exists():
            raise InvalidEmail(_(f'{email} is already registered. Please try with another email'))

    def _check_username_exists(self, username: str):
        if User.objects.filter(username=username).exists():
            raise InvalidUsername(_(f'{username} is already registered. Please try with another username'))


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'member_type')


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'member_type', 'date_joined', 'last_login')


class UserUpdateSerializer(serializers.Serializer):
    member_type = serializers.ChoiceField(choices=MemberType.choices)

    def update(self, instance, validated_data):
        instance.member_type = validated_data.get('member_type')
        instance.save()
        return instance
