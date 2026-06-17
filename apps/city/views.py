from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .serializers import CitySerializer

from .models import City 

# Create your views here.
class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    