from django.contrib import admin

from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        "deck",
        "box",
        "next_review_at",
        "last_reviewed_at",
        "times_reviewed",
        "times_correct",
        "created_at",
    )

    list_filter = (
        "box",
        "deck",
    )

    search_fields = (
        "front",
        "back",
        "hint",
        "deck__title",
    )

    ordering = (
        "box",
        "next_review_at",
    )