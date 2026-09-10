from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DeckViewSet, StatsView


router = DefaultRouter()

router.register(
    "decks",
    DeckViewSet,
    basename="deck",
)


urlpatterns = [
    path("", include(router.urls)),
    path("stats/", StatsView.as_view(), name="stats"),
]