from django.db.models import Count, Q
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .models import Deck
from .serializers import DeckSerializer


class DeckViewSet(viewsets.ModelViewSet):
    serializer_class = DeckSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "subject",
        "is_archived",
    ]

    search_fields = [
        "title",
    ]

    def get_queryset(self):
        now = timezone.now()

        return (
            Deck.objects
            .filter(owner=self.request.user)
            .annotate(
                card_count=Count("cards", distinct=True),
                due_count=Count(
                    "cards",
                    filter=Q(cards__next_review_at__lte=now),
                    distinct=True,
                ),
            )
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)