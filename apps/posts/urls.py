from .views import PostViewSet,PostViewSetV2
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("", PostViewSet, basename= "posts")
router.register("/v2", PostViewSetV2, basename= "posts")

urlpatterns = router.urls

