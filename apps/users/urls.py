from django.urls import path,include

from .views import SignupView, VerifyEmailView , LoginView,ProfileView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name= "profile"),

]
    
