from django.contrib import admin

from .models import Deck


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "subject",
        "is_archived",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "subject",
        "is_archived",
    )

    search_fields = (
        "title",
        "description",
        "owner__username",
    )

    ordering = (
        "-created_at",
    )