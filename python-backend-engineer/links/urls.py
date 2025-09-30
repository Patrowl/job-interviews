from django.urls import path

from .views import LinkStatsAPIView, RedirectLinkAPIView, RetrieveLinkAPIView, ShortenLinkAPIView

urlpatterns = [
    path("api/shorten/", ShortenLinkAPIView.as_view(), name="shorten_link"),
    path("<str:short_code>/", RedirectLinkAPIView.as_view(), name="redirect_link"),
    path(
        "api/links/<str:short_code>/",
        RetrieveLinkAPIView.as_view(),
        name="retrieve_link",
    ),
    path("api/stats/", LinkStatsAPIView.as_view(), name="link_stats"),
]
