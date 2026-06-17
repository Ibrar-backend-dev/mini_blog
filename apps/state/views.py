from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .serializers import StateSerializer

from .models import  State
# Create your views here.
class StateViewSet(ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


    def get_serializer_context(self):

        context = super().get_serializer_context()
        context['show_country_name'] = True

        return context

    