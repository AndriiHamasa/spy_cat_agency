from django.urls import include, path
from rest_framework.routers import DefaultRouter

from agency.views import CatViewSet, MissionViewSet, TargetViewSet

# from books.views import BookViewSet


app_name = "agency"

router = DefaultRouter()
router.register("cats", CatViewSet, basename="cats")
router.register("missions", MissionViewSet, basename="missions")
# router.register(r"missions/(?P<mission_id>\d+)/target", TargetViewSet, basename="mission-target")


urlpatterns = [
    path("", include(router.urls))
]

