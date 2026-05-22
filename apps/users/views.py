from django.contrib.auth import get_user_model
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    SignupSerializer,
    LoginSerializer,
    UserProfileSerializer,
)
from .permissions import IsOwnerOrReadOnly
from .services import normalize_email, send_email_verification
from .utils import verify_email_verification_token

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action in ["signup", "login", "verify_email"]:
            permission_classes = [permissions.AllowAny]
        elif self.action in ["logout", "me"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["create", "signup"]:
            return SignupSerializer
        if self.action == "login":
            return LoginSerializer
        return UserProfileSerializer

    def get_queryset(self):
        if self.action == "list":
            if self.request.user.is_staff:
                return User.objects.all()
            if self.request.user.is_authenticated:
                return User.objects.filter(pk=self.request.user.pk)
            return User.objects.none()
        return super().get_queryset()

    @action(detail=False, methods=["post"], url_path="signup", permission_classes=[permissions.AllowAny])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_email_verification(user)
        profile = UserProfileSerializer(user, context=self.get_serializer_context())
        headers = self.get_success_headers(profile.data)
        return Response(profile.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=["post"], url_path="login", permission_classes=[permissions.AllowAny])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        profile = UserProfileSerializer(user, context=self.get_serializer_context())
        return Response(
            {
                "user": profile.data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )

    @action(detail=False, methods=["post"], url_path="logout", permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"refresh": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            raise ValidationError({"refresh": "Invalid or expired token."})

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="me", permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = UserProfileSerializer(request.user, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"verify-email/(?P<token>[^/.]+)",
        permission_classes=[permissions.AllowAny],
    )
    def verify_email(self, request, token=None):
        if not token:
            raise ValidationError({"token": "This field is required."})

        payload = verify_email_verification_token(token)
        if not payload:
            raise ValidationError("Invalid or expired token.")

        user = User.objects.filter(
            pk=payload.get("user_id"),
            email=normalize_email(payload.get("email") or ""),
        ).first()
        if not user:
            raise NotFound("User not found.")

        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])
        return Response({"detail": "Email verified successfully."})
