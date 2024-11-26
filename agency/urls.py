from django.urls import include, path
from rest_framework.routers import DefaultRouter

from agency.views import CatViewSet

# from books.views import BookViewSet


app_name = "agency"

router = DefaultRouter()
router.register("cats", CatViewSet, basename="cats")

urlpatterns = [
    path("", include(router.urls))
]

