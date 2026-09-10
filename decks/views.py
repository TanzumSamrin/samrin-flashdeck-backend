from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cards.models import Card

from .models import Deck
from .serializers import DeckSerializer, StudyDeckSerializer


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
                card_count=Count(
                    "cards",
                    distinct=True,
                ),
                due_count=Count(
                    "cards",
                    filter=Q(
                        cards__next_review_at__lte=now
                    ),
                    distinct=True,
                ),
            )
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(
        detail=True,
        methods=["get"],
        url_path="study",
    )
    def study(self, request, pk=None):
        deck = self.get_object()

        now = timezone.now()

        cards = (
            Card.objects
            .filter(
                deck=deck,
                next_review_at__lte=now,
            )
            .select_related("deck")
            .order_by("next_review_at")[:20]
        )

        return Response(
            {
                "deck": StudyDeckSerializer(deck).data,
                "due_count": Card.objects.filter(
                    deck=deck,
                    next_review_at__lte=now,
                ).count(),
                "cards": [
                    {
                        "id": card.id,
                        "deck": card.deck_id,
                        "deck_title": card.deck.title,
                        "front": card.front,
                        "back": card.back,
                        "hint": card.hint,
                        "box": card.box,
                        "next_review_at": card.next_review_at,
                        "last_reviewed_at": card.last_reviewed_at,
                        "times_reviewed": card.times_reviewed,
                        "times_correct": card.times_correct,
                        "is_due": True,
                        "created_at": card.created_at,
                        "updated_at": card.updated_at,
                    }
                    for card in cards
                ],
            },
            status=status.HTTP_200_OK,
        )

    
class StatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        today = now.date()

        cards = Card.objects.filter(
            deck__owner=request.user
        )

        decks_count = Deck.objects.filter(
            owner=request.user
        ).count()

        cards_count = cards.count()

        due_now = cards.filter(
            next_review_at__lte=now
        ).count()

        mastered = cards.filter(
            box=5
        ).count()

        reviewed_today = cards.filter(
            last_reviewed_at__date=today
        ).count()

        total_reviews = sum(
            cards.values_list(
                "times_reviewed",
                flat=True
            )
        )

        total_correct = sum(
            cards.values_list(
                "times_correct",
                flat=True
            )
        )

        if total_reviews == 0:
            accuracy = 0
        else:
            accuracy = round(
                100 * total_correct / total_reviews
            )

        box_data = cards.values("box").annotate(
            count=Count("id")
        )

        boxes = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
        }

        for item in box_data:
            boxes[item["box"]] = item["count"]

        return Response({
            "decks": decks_count,
            "cards": cards_count,
            "due_now": due_now,
            "mastered": mastered,
            "reviewed_today": reviewed_today,
            "accuracy": accuracy,
            "boxes": boxes,
        })