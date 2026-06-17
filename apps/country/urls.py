from django.urls import path
from .views import CountryViewSet

urlpatterns = [
    path('', CountryViewSet.as_view({'get': 'list', 'post': 'create'}), name='country-list-create'),
    path('<int:pk>/', CountryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}), name='country-detail'),
]
