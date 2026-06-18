from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import StateViewSet

router = DefaultRouter()
router.register("", StateViewSet, basename="state")

urlpatterns = [
    path("", include(router.urls)),
]

