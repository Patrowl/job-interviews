import json
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from .models import Link
from .serializers import LinkCreateSerializer, LinkSerializer


class ShortenLinkAPIView(APIView):
    @extend_schema(
        request=LinkCreateSerializer,
        responses={201: LinkSerializer},
        description="Create a shortened URL from an original URL",
        methods=["POST"],
        tags=["Links"],
    )
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        try:
            data: dict[str, Any] = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        serializer = LinkCreateSerializer(data=data)
        if serializer.is_valid():
            original_url: str = serializer.validated_data["url"]
            link_obj, created = Link.objects.get_or_create(original_url=original_url)
            output_serializer = LinkSerializer(link_obj)
            return JsonResponse(output_serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class RedirectLinkAPIView(APIView):
    @extend_schema(exclude=True)
    def get(
        self, request: HttpRequest, short_code: str, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        link_obj = get_object_or_404(Link, short_code=short_code)
        return redirect(link_obj.original_url)


class RetrieveLinkAPIView(APIView):
    @extend_schema(
        description="Retrieve details about a shortened URL",
        methods=["GET"],
        responses={200: LinkSerializer, 404: dict},
        tags=["Links"],
    )
    def get(
        self, request: HttpRequest, short_code: str, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        link_obj = get_object_or_404(Link, short_code=short_code)
        serializer = LinkSerializer(link_obj)
        return JsonResponse(serializer.data)
