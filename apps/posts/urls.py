from .views import PostViewSet, PostViewSetv2, PostDetailViewSetv2
from rest_framework.routers import DefaultRouter 
from django.urls import path

router = DefaultRouter()

router.register("", PostViewSet, basename= "posts")
# router.register("/v2", PostViewSetv2, basename= "posts_v2")
# router.register("/v2", PostDetailViewSetv2, basename= "posts_deatil_v2")

urlpatterns = [
    path("v2/", PostViewSetv2.as_view(), name="posts_v2"),
    path("v2/<int:pk>/", PostDetailViewSetv2.as_view(), name="posts_detail_v2"),
] + router.urls


