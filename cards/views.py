from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Card
from .serializers import CardSerializer


INTERVALS = {
    1: 0,
    2: 1,
    3: 3,
    4: 7,
    5: 16,
}


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = ["deck", "box"]
    search_fields = ["front", "back"]
    ordering_fields = [
        "created_at",
        "box",
        "next_review_at",
    ]
    ordering = ["box", "next_review_at"]

    def get_queryset(self):
        return (
            Card.objects
            .filter(deck__owner=self.request.user)
            .select_related("deck")
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="review",
    )
    @transaction.atomic
    def review(self, request, pk=None):
        card = self.get_object()

        # Strict boolean validation
        if "correct" not in request.data:
            return Response(
                {"correct": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        correct = request.data["correct"]

        if not isinstance(correct, bool):
            return Response(
                {"correct": ["Must be a boolean."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        now = timezone.now()

        if correct:
            # Move one box up, maximum box 5
            new_box = min(card.box + 1, 5)

            card.box = new_box
            card.next_review_at = (
                now + timedelta(days=INTERVALS[new_box])
            )

            card.times_correct += 1

        else:
            # Wrong answer -> reset to box 1
            card.box = 1
            card.next_review_at = now

        card.last_reviewed_at = now
        card.times_reviewed += 1

        card.save(
            update_fields=[
                "box",
                "next_review_at",
                "last_reviewed_at",
                "times_reviewed",
                "times_correct",
                "updated_at",
            ]
        )

        return Response(
            CardSerializer(
                card,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK,
        )