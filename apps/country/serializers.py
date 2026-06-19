from rest_framework import serializers
from .models import Country

from apps.state.serializers import CountryStateSerializer


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ['id',  'name', 'description']

class CountryDetailSerializer(serializers.ModelSerializer):

    states = CountryStateSerializer( many = True , read_only = True)

    class Meta:
        model = Country
        fields = ["id" , "name" , "states"]