from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core import signing
from .utils import decode_verification_token
from rest_framework_simplejwt.tokens import RefreshToken


from .services import send_verification_email
from.serializers import SignupSerializer , LoginSerializer

User = get_user_model()

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        serializer = SignupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        user = serializer.save()

        send_verification_email(user)

        return Response({
        "message": (
            "Registration successful. "
            "Please check your email. "
            "to verify your account."
        ),
        "user_id": user.id,
    },
    status=201
    )

class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):

    
        try:
            payload = decode_verification_token(token)
        
        except signing.SignatureExpired:

            return Response ({"error": "Verification link has expired."}, status=400) 
    
        except signing.BadSignature:
            return Response ({"error": "Invalid verification token."}, status=400)
    
        user_id = payload.get("user_id")
        email = payload.get("email").lower().strip()

        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return Response ({"error":"User not found."}, status = 404)
    
        if user.is_email_verified:
            return Response(
                {
                    "message": "Email already verified."
                },
                status=200,
            )

        user.is_email_verified = True

        user.save(update_fields=["is_email_verified"])

        return Response({"message": "Email verified successfully."}, status=200)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access" : str(refresh.access_token), 
                "refresh" : str(refresh),      
            },
            status = 200,
        )
    

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {
                'id': request.user.id,
                'email': request.user.email,
                'is_email_verified': (request.user.is_email_verified),
            }
        )

