from django.conf import settings
from django.db import models


class Deck(models.Model):
    class Subject(models.TextChoices):
        PROGRAMMING = "PROGRAMMING", "Programming"
        LANGUAGE = "LANGUAGE", "Language"
        ACADEMIC = "ACADEMIC", "Academic"
        INTERVIEW = "INTERVIEW", "Interview"
        OTHER = "OTHER", "Other"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="decks",
    )

    title = models.CharField(max_length=120)

    description = models.TextField(blank=True)

    subject = models.CharField(
        max_length=20,
        choices=Subject.choices,
        default=Subject.OTHER,
    )

    is_archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title