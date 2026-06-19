
from rest_framework.viewsets import ModelViewSet

from .serializers import CountrySerializer ,CountryDetailSerializer
from .models import Country

# Create your views here.
class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

# return Country serializer when list is get and when get one country with id then get details about the country 
    def get_serializer_class(self):
        if self.action == "retrieve":
            return CountryDetailSerializer
        
        return CountrySerializer