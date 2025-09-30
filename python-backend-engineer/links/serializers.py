from rest_framework import serializers

from .models import Link, LinkClick


class LinkSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Link
        fields = ["original_url", "short_code", "created_at"]
        read_only_fields = ["short_code", "created_at"]



class LinkClickSerializer(serializers.Serializer):
    short_code = serializers.CharField()
    click_count = serializers.IntegerField()
    last_click = serializers.DateTimeField(allow_null=True)


class LinkCreateSerializer(serializers.Serializer):
    url = serializers.URLField()
