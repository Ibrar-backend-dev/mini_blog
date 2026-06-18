from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .serializers import StateSerializer

from .models import  State
# Create your views here.
class StateViewSet(ModelViewSet):
    
    serializer_class = StateSerializer
    
    def get_queryset(self):
        return State.objects.select_related("country")

    def get_serializer_context(self):

        context = super().get_serializer_context()
        context['show_country_name'] = True

        return context

    