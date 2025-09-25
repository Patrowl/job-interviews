import json
from re import L
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from .models import Link, LinkClick
from .serializers import LinkClickSerializer, LinkCreateSerializer, LinkSerializer


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
            link_obj, _ = Link.objects.get_or_create(original_url=original_url)
            output_serializer = LinkSerializer(link_obj)
            return JsonResponse(output_serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class RedirectLinkAPIView(APIView):
    @extend_schema(exclude=True)
    def get(
        self, request: HttpRequest, short_code: str, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        link_obj = get_object_or_404(Link, short_code=short_code)
        LinkClick.objects.create(
            link=link_obj,
        )
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


class LinkStatsAPIView(APIView):
    @extend_schema(
        description="Retrieve statistics about a shortened URL",
        methods=["GET"],
        responses={200: LinkClickSerializer},
        tags=["Links"],
    )
    def get(self, request: HttpRequest) -> JsonResponse:
        links: list[Link] = Link.objects.all()
        stats_data = []
        for link in links:
            stats_data.append({
                'short_code': link.short_code,
                'click_count': link.clicks.count(),
                'last_click': link.clicks.first().clicked_at if link.clicks.exists() else None
            })

        serializer = LinkClickSerializer(stats_data, many=True)
        return JsonResponse(serializer.data, safe=False)
