from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from django.utils import timezone

from decks.models import Deck


class Card(models.Model):
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
        related_name="cards",
    )

    front = models.TextField()

    back = models.TextField()

    hint = models.CharField(
        max_length=200,
        blank=True,
    )

    box = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    next_review_at = models.DateTimeField(
        default=timezone.now,
    )

    last_reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    times_reviewed = models.PositiveIntegerField(
        default=0,
    )

    times_correct = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["box", "next_review_at"]

    def __str__(self):
        return self.front[:40]