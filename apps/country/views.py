
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


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
    
# API version 2 for returning details of country without nested serializer

    def get_queryset(self):
        if self.action == "get_country_v2":
            return Country.objects.prefetch_related("states__cities")
        return Country.objects.all()
    
    
    @action (detail = True , methods = ['get'] , url_path = "v2")

    def get_country_v2(self ,request , pk = None):
        country = self.get_object()

        states_data =[]
        

        for state in country.states.all():

            cities_data =[]

            for city in state.cities.all():

                cities_data.append(
                    {
                        "id":city.id,
                        "name":city.name,
                    }
                )


            states_data.append(
                {
                   "id": state.id,
                   "name":state.name,
                   "cities":cities_data,
                }
            )

            
            data = {
            "id":country.id,
            "name": country.name,
            "states": states_data
            }
        return Response(data)
