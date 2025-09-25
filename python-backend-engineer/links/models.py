import random
import string

from django.db import models


def generate_short_code(length: int = 6) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


class Link(models.Model):
    original_url: models.URLField = models.URLField()
    short_code: models.CharField = models.CharField(
        max_length=10, unique=True, default=generate_short_code
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.short_code} -> {self.original_url}"


class LinkClick(models.Model):
    link: models.ForeignKey = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="clicks")
    clicked_at = models.DateTimeField(auto_now_add=True)
