from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from snack.core.models import User
from snack.core.exceptions import InvalidEmail


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data.get('email', None)
        if User.objects.filter(email=email).exists():
            raise InvalidEmail(_(f'{email} is already registered. Please try with another email'))

        user = User.objects.create_user(
            username=validated_data['username'], email=validated_data['email'], password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'member_type')
