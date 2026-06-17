from rest_framework import serializers
from .models import State

class StateSerializer(serializers.ModelSerializer):
    
    country_name = serializers.SerializerMethodField() 

    class Meta:
        model = State
        fields = ['id', 'country_id','country_name', 'name', 'description']

    def get_country_name(self, obj):
        show_country_name = self.context.get('show_country_name', True)

        if show_country_name:
            return obj.country_id.name
        
        return None 
    
    def validate_name(self, value):
        name = value.strip().capitalize()

        if not name:
            raise serializers.ValidationError("State name cannot be empty.")
        return name
    
    def validate(self, data):
        country_id = data.get('country_id')
        name = data.get('name')

        if State.objects.filter(country_id=country_id, name=name).exists():
            raise serializers.ValidationError("State with this name already exists in the specified country.")
        
        return data