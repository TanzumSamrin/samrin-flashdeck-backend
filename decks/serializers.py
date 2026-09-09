from django.db.models import Count, Q
from rest_framework import serializers

from .models import Deck


class DeckSerializer(serializers.ModelSerializer):
    card_count = serializers.IntegerField(read_only=True)
    due_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Deck
        fields = [
            "id",
            "title",
            "description",
            "subject",
            "is_archived",
            "card_count",
            "due_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "card_count",
            "due_count",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        user = self.context["request"].user

        queryset = Deck.objects.filter(
            owner=user,
            title__iexact=value,
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A deck with this title already exists."
            )

        return value