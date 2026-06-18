from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .serializers import CitySerializer

from .models import City 

# Create your views here.
class CityViewSet(ModelViewSet):
    
    serializer_class = CitySerializer

    def get_queryset(self):

        return City.objects.select_related("state" , "state__country")
    

    def get_serializer_context(self):

        context =  super().get_serializer_context()
        context["show_state_name"] = True
        context["show_country_name"] = True

        return context

    