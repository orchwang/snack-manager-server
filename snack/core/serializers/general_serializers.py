from rest_framework import serializers


class ResponseDetailSerializer(serializers.Serializer):
    detail = serializers.CharField()
