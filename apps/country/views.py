
from rest_framework.viewsets import ModelViewSet

from .serializers import CountrySerializer
from .models import Country

# Create your views here.
class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer