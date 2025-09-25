from rest_framework import serializers

from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Link
        fields = ["original_url", "short_code", "created_at"]
        read_only_fields = ["short_code", "created_at"]


class LinkCreateSerializer(serializers.Serializer):
    url = serializers.URLField()
