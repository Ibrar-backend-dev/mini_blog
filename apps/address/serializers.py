from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):



    class Meta:
        model = Address
        fields = [
            'id',
            'permanent_address',
            'residential_address',
            'country',
            'state',
            'city',
            'postal_code'
        ]
    
    def validate_permanent_address(self, value):
        if not value:
            raise serializers.ValidationError("Permanent address cannot be empty.")
        return value
    
    def validate_residential_address(self, value):
        if not value:
            raise serializers.ValidationError("Residential address cannot be empty.")
        return value
    
    def validate(self, attrs):

        permanent = attrs.get('permanent_address')
        residential = attrs.get('residential_address')

        # At least one address is required
        if not permanent and not residential:
            raise serializers.ValidationError(
                "At least one of permanent_address or residential_address must be provided."
            )
        
    def validate(self, attrs):
        country = attrs.get('country')
        state = attrs.get('state')
        city = attrs.get('city')


        #country validation
        if state.country != country:
            raise serializers.ValidationError({
                "state": "State does not belong to the specified country."
                })

    
        #state validation

        if city.state != state:
            raise serializers.ValidationError({
                "city": "City does not belong to the specified state."
                })
        return attrs
    

    