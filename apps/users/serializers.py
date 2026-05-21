from django.contrib.auth import get_user_model,authenticate
from rest_framework import serializers

from .services import create_user

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True ,min_length=8)

    password_confirm = serializers.CharField(write_only = True , min_length=8)

    class Meta:
        model = User

        fields = (
            'id',
            'username',
            'email',
            'password',
            'password_confirm',
        )

    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError(
                'Email already exists.'
            )
        return value
        
    def validate_username(self , value ):
        if User.objects.filter(username = value).exists():
            raise serializers.ValidationError(
                'Username already exists.'
            )
        return value

    def validate(self ,data):

        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if data['password'] != data ['password_confirm']:

            raise serializers.ValidationError({
                'password_confirm':'passwords do not match.'
            }
            )
        return data
        
    def create (self , validated_data):
        validated_data.pop('password_confirm')
        return create_user(**validated_data)
        
class LoginSerializer(serializers.Serializer):

    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self , data):

        username_or_email = data.get("username_or_email")
        password = data.get("password")

        # Try login with email
        user = User.objects.filter(
            email = username_or_email
        ).first()

        if user:
            username = user.username
        else:
            username = username_or_email

        authenticated_user = authenticate(
            username = username,
            password = password
        )

        if not authenticated_user:
            raise serializers.ValidationError(
                'Invalid credentials.'
            )
        
        data['user'] = authenticated_user
        return data
        
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User 
        fields = (
            'id',
            'username',
            'email',
            'is_verified'
        )
        read_only_fields = fields

        
