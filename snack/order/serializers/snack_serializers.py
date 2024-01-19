from django.contrib.auth import get_user_model
from rest_framework import serializers

from snack.order.constants import SnackReactionType
from snack.order.models import Snack, SnackReaction


User = get_user_model()


class SnackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = '__all__'


class SnackDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = '__all__'


class SnackWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = ['name', 'url', 'desc', 'image', 'currency', 'price']


class SnackReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnackReaction
        fields = '__all__'


class SnackReactionWriteSerializer(serializers.ModelSerializer):
    snack = serializers.SlugRelatedField(queryset=Snack.objects.all(), slug_field='uid')
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='id')
    type = serializers.ChoiceField(choices=SnackReactionType)

    class Meta:
        model = SnackReaction
        fields = ['snack', 'user', 'type']
