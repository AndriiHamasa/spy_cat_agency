from django.urls import include, path
from rest_framework.routers import DefaultRouter

from agency.views import CatViewSet, MissionViewSet, TargetViewSet


app_name = "agency"

router = DefaultRouter()
router.register("cats", CatViewSet, basename="cats")
router.register("missions", MissionViewSet, basename="missions")


urlpatterns = [path("", include(router.urls))]
