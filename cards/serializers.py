from rest_framework import serializers

from .models import Card
from decks.models import Deck


class CardSerializer(serializers.ModelSerializer):
    deck_title = serializers.CharField(
        source="deck.title",
        read_only=True,
    )

    is_due = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = [
            "id",
            "deck",
            "deck_title",
            "front",
            "back",
            "hint",
            "box",
            "next_review_at",
            "last_reviewed_at",
            "times_reviewed",
            "times_correct",
            "is_due",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "deck_title",
            "box",
            "next_review_at",
            "last_reviewed_at",
            "times_reviewed",
            "times_correct",
            "is_due",
            "created_at",
            "updated_at",
        ]

    def get_is_due(self, obj):
        from django.utils import timezone

        return obj.next_review_at <= timezone.now()

    def validate_deck(self, value):
        request = self.context["request"]

        if value.owner != request.user:
            raise serializers.ValidationError(
                "You cannot add a card to another user's deck."
            )

        return value