from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError


from .services import authenticate_user
from .services import create_user 
User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True , min_length= 8 , required=True)
    password_confirm = serializers.CharField(write_only = True, required=True)

    class Meta:
        model = User
        fields = ('username','email','password','password_confirm')

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


        






# from django.contrib.auth import authenticate, get_user_model
# from rest_framework import serializers

# from .services import create_user, normalize_email

# User = get_user_model()


# class SignupSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=8)
#     password_confirm = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ("username", "email", "password", "password_confirm")

#     def validate_email(self, value):
#         normalized = normalize_email(value)
#         if User.objects.filter(email=normalized).exists():
#             raise serializers.ValidationError("Email already exists.")
#         return normalized

#     def validate_username(self, value):
#         if User.objects.filter(username=value).exists():
#             raise serializers.ValidationError("Username already exists.")
#         return value

#     def validate(self, attrs):
#         password = attrs.get("password")
#         password_confirm = attrs.get("password_confirm")
#         if password != password_confirm:
#             raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
#         return attrs

#     def create(self, validated_data):
#         validated_data.pop("password_confirm")
#         return create_user(
#             username=validated_data["username"],
#             email=validated_data["email"],
#             password=validated_data["password"],
#         )


# class LoginSerializer(serializers.Serializer):
#     username_or_email = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         username_or_email = attrs.get("username_or_email")
#         password = attrs.get("password")

#         normalized_email = normalize_email(username_or_email)
#         user = User.objects.filter(email=normalized_email).first()
#         username = user.username if user else username_or_email

#         authenticated_user = authenticate(username=username, password=password)

#         if not authenticated_user:
#             raise serializers.ValidationError("Invalid credentials.")

#         if not getattr(authenticated_user, "is_email_verified", False):
#             raise serializers.ValidationError("Email is not verified.")

#         attrs["user"] = authenticated_user
#         return attrs


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             "id",
#             "username",
#             "email",
#             "is_email_verified",
#         )
#            read_only_fields = fields