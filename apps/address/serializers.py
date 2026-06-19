from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)


    class Meta:
        model = Address
        fields = [
            'id',
            'permanent_address',
            'residential_address',
            'country',
            'country_name',
            'state',
            'state_name',
            'city',
            'city_name',
            'postal_code'
        ]
    
    def validate(self, attrs):

        permanent = attrs.get('permanent_address')
        residential = attrs.get('residential_address')

        # At least one address is required
        
        if not permanent and not residential:
            raise serializers.ValidationError(
                "At least one of permanent_address or residential_address must be provided."
            )

        country = attrs.get('country')
        state = attrs.get('state')
        city = attrs.get('city')

        #country validation
        if state and country and state.country != country:
            raise serializers.ValidationError({
                'state': 'State does not belong to the specified country.'
            })

        if city and state and city.state != state:
            raise serializers.ValidationError({
                'city': 'City does not belong to the specified state.'
            })
        
        return attrs