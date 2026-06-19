from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.address.serializers import AddressSerializer
from apps.address.models import Address

from .services import authenticate_user
from .services import create_user 

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True , min_length= 8 , required=True)
    password_confirm = serializers.CharField(write_only = True, required=True)

    address = AddressSerializer(required = False, allow_null = True)

    class Meta:
        model = User
        fields = ['username','email','password','password_confirm','address']

# email validation
    def validate_email(self,value):
        email= value.strip().lower()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        return email

# password match validation
    def validate(self,attrs):

        if attrs['password']!= attrs['password_confirm']:
            raise serializers.ValidationError('Passwords do not match.')
        return attrs

# user creation with removal of password_confirm
    def create(self, validated_data):
        validated_data.pop('password_confirm')

        return create_user(
            username= validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

class UserProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only = True)

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'username','email','is_email_verified','address',]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        user = authenticate_user(
                email = attrs['email'],
                password = attrs['password'],
            )
        
        attrs["user"] = user

        return attrs
