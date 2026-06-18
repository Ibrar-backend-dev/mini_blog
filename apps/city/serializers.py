from rest_framework import serializers
from .models import City

class CitySerializer(serializers.ModelSerializer):

    state_name = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['id', 'state', 'state_name', 'country', 'country_name', 'name', 'description']


    def get_state_name(self, obj):
        show_state_name = self.context.get("show_state_name", False)

        if show_state_name:
            return obj.state.name

        return None

    def get_country(self, obj):
        return obj.state.country.id

    def get_country_name(self, obj):
        show_country_name = self.context.get("show_country_name", False)

        if show_country_name:
            return obj.state.country.name

        return None