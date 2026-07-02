from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core import signing

from utils.print_utils import debug_print
from .utils import decode_verification_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser

from apps.address.models import Address
from apps.address.serializers import AddressSerializer


from .services import send_verification_email
from .serializers import (
    ProfilePhotoSerializer,
    SignupSerializer,
    LoginSerializer,
    UserProfileSerializer,
)

User = get_user_model()


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        send_verification_email(user)

        return Response(
            {
                "message": ("Registration successful. " "Please check your email. " "to verify your account."),
                "user_id": user.id,
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):

        try:
            payload = decode_verification_token(token)

        except signing.SignatureExpired:

            return Response(
                {"error": "Verification link has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except signing.BadSignature:
            return Response(
                {"error": "Invalid verification token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = payload.get("user_id")
        email = payload.get("email").lower().strip()

        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_email_verified:
            return Response(
                {"message": "Email already verified."},
                status=status.HTTP_200_OK,
            )

        user.is_email_verified = True

        user.save(update_fields=["is_email_verified"])

        return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """Update user address"""
        request_data = request.data
        logged_in_user = request.user
        logged_in_user_email = logged_in_user.email

        if not request_data:
            return Response({"error": "Request data is required."}, status=status.HTTP_400_BAD_REQUEST)

        signup_email = request_data.get("signup_email")

        if signup_email != logged_in_user_email:
            return Response({"error": "You are not authorized to update this address."}, status=status.HTTP_403_FORBIDDEN)

        # try:
        #     address_instance = Address.objects.get(user=logged_in_user)

        # except Address.DoesNotExist:
        #     return Response({"error": "Address does not exist."}, status=status.HTTP_404_NOT_FOUND)

        address_data = request_data.get("address")

        # Address.objects.create(
        #     user=logged_in_user,
        #     permanent_address=address_data.get("permanent_address"),
        #     residential_address=address_data.get("residential_address"),
        #     country_id=address_data.get("country"),
        #     state_id=address_data.get("state"),
        #     city_id=address_data.get("city"),
        #     postal_code=address_data.get("postal_code"),
        # )

        instance, created = Address.objects.update_or_create(
            user=logged_in_user,
            defaults={
                "permanent_address": address_data.get("permanent_address"),
                "residential_address": address_data.get("residential_address"),
                "country_id": address_data.get("country"),
                "state_id": address_data.get("state"),
                "city_id": address_data.get("city"),
                "postal_code": address_data.get("postal_code"),
            },
        )
        debug_print(instance)
        debug_print(created)

        return Response(
            {
                "signup_email": signup_email,
                "address": {
                    "id": instance.id,
                    "permanent_address": instance.permanent_address,
                    "residential_address": instance.residential_address,
                    "country": instance.country.name,
                    "state": instance.state.name,
                    "city": instance.city.name,
                    "postal_code": instance.postal_code,
                },
                "message": "Address updated successfully.",
            },
            status=status.HTTP_200_OK,
        )

        # if not address_data:
        #     return Response(
        #         {"error": "Address data is required."},
        #         status= status.HTTP_400_BAD_REQUEST
        #     )

        # try:
        #     address = user.address
        #     serializer = AddressSerializer(address, data=address_data, partial=True)
        # except Address.DoesNotExist:
        #     serializer = AddressSerializer(data=address_data)

        # if serializer.is_valid():
        #     serializer.save(user=user)
        #     return Response(
        #         UserProfileSerializer(user).data, status=status.HTTP_200_OK
        #     )

    def delete(self, request):
        """Delete user address"""
        user = request.user

        try:
            address = user.address
        except Address.DoesNotExist:
            return Response(
                {"error": "User has no address to delete."},
                status=status.HTTP_404_NOT_FOUND,
            )
        address.delete()
        return Response({"message": "Address deleted successfully."}, status=status.HTTP_200_OK)

    def patch(self, request):

        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfilePhotoView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request):

        serializer = ProfilePhotoSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if request.user.profile_photo:
            request.user.profile_photo.delete(save=False)

        serializer.save()
        return Response(UserProfileSerializer(request.user).data, status=status.HTTP_200_OK)

    def delete(self, request):
        if not request.user.profile_photo:
            return Response(
                {"error": "Profile photo does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        request.user.profile_photo.delete(save=False)
        request.user.profile_photo = None
        request.user.save(update_fields=["profile_photo"])

        return Response(
            {"message": "Profile photo deleted successfully."},
            status=status.HTTP_200_OK,
        )
