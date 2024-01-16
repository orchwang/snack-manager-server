from rest_framework import serializers

from snack.order.models import Snack
from snack.order.constants import Currency


class SnackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = '__all__'


class SnackDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = '__all__'


class CreateSnackSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.CharField()
    desc = serializers.CharField()
    image = serializers.ImageField()
    currency = serializers.ChoiceField(choices=Currency, default=Currency.KRW)
    price = serializers.FloatField()

    def create(self, validated_data):
        return Snack.objects.create(**validated_data)
