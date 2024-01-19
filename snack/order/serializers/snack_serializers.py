from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from snack.order.constants import SnackReactionType
from snack.order.models import Snack, SnackReaction


User = get_user_model()


class SnackSerializer(serializers.ModelSerializer):
    like_reaction_count = serializers.SerializerMethodField()
    hate_reaction_count = serializers.SerializerMethodField()

    class Meta:
        model = Snack
        fields = '__all__'

    @extend_schema_field(OpenApiTypes.INT)
    def get_like_reaction_count(self, obj):
        return obj.snack_reactions.filter(type=SnackReactionType.LIKE).count()

    @extend_schema_field(OpenApiTypes.INT)
    def get_hate_reaction_count(self, obj):
        return obj.snack_reactions.filter(type=SnackReactionType.HATE).count()


class SnackDetailSerializer(serializers.ModelSerializer):
    like_reaction_count = serializers.SerializerMethodField()
    hate_reaction_count = serializers.SerializerMethodField()

    class Meta:
        model = Snack
        fields = '__all__'

    @extend_schema_field(OpenApiTypes.INT)
    def get_like_reaction_count(self, obj):
        return obj.snack_reactions.filter(type=SnackReactionType.LIKE).count()

    @extend_schema_field(OpenApiTypes.INT)
    def get_hate_reaction_count(self, obj):
        return obj.snack_reactions.filter(type=SnackReactionType.HATE).count()


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
