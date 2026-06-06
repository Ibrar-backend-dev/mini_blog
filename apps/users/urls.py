from django.urls import path,include

from .views import SignupView, VerifyEmailView , LoginView,ProfileView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name= "profile"),

]
    

# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from .views import UserViewSet
# from django.urls import path

# router = DefaultRouter()
# router.register(r"", UserViewSet, basename="auth")

# urlpatterns = [
#     path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
# ]+router.urls

