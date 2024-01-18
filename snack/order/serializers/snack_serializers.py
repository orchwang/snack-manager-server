from rest_framework import serializers

from snack.order.constants import SnackReactionType
from snack.order.models import Snack, SnackReaction


class SnackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = '__all__'


class SnackDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = '__all__'


class CreateSnackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = ['name', 'url', 'desc', 'image', 'currency', 'price']


class SnackReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnackReaction
        fields = '__all__'


class CreateSnackReactionSerializer(serializers.Serializer):
    snack_uid = serializers.CharField()
    type = serializers.ChoiceField(choices=SnackReactionType)
