from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from .models import Card
from .serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "deck",
        "box",
    ]

    search_fields = [
        "front",
        "back",
    ]

    ordering_fields = [
        "created_at",
        "box",
        "next_review_at",
    ]

    ordering = [
        "box",
        "next_review_at",
    ]

    def get_queryset(self):
        return (
            Card.objects
            .filter(
                deck__owner=self.request.user
            )
            .select_related("deck")
        )