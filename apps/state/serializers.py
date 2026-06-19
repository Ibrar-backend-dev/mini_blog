from rest_framework import serializers
from .models import State

from apps.city.serializers import CountryCitySerializer

class StateSerializer(serializers.ModelSerializer):
    
    country_name = serializers.SerializerMethodField() 

    class Meta:
        model = State
        fields = ['id', 'country','country_name', 'name', 'description']

    def get_country_name(self, obj):
        show_country_name = self.context.get('show_country_name', True)

        if show_country_name:
            return obj.country.name
        
        return None 
    
    def validate_name(self, value):
        name = value.strip().capitalize()

        if not name:
            raise serializers.ValidationError("State name cannot be empty.")
        return name
    
    def validate(self, data):
        country = data.get('country')
        name = data.get('name')

        if State.objects.filter(country = country, name=name).exists():
            raise serializers.ValidationError("State with this name already exists in the specified country.")
        
        return data
    
# Nested serializer for  countries to get its related states
class CountryStateSerializer(serializers.ModelSerializer):
    cities = CountryCitySerializer(many = True , read_only = True)

    class Meta:
        fields = ["id" , "name" ,"cities"]