from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from django.conf import settings

from .utils import generate_verification_token , build_verification_url

User = get_user_model()

def normalize_email(email:str)->str:
    return email.strip().lower()

def create_user(* , username:str, email:str, password:str):
    email = normalize_email(email)

    return User.objects.create_user(
        username = username,
        email = email,
        password = password
    )

def send_verification_email(user):
    token = generate_verification_token(user)
    verification_url = build_verification_url(token)

    send_mail(
        subject = 'Verify your account.',
        message = (f'Hi {user.username},\n'
                    f"Click the link below:\n\n"
                    f"{verification_url}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )








# from django.conf import settings
# from django.core.mail import send_mail
# from django.contrib.auth import get_user_model

# from .utils import build_email_verification_link, generate_email_verification_token

# User = get_user_model()


# def normalize_email(email):
#     """Normalize an email address for storage and comparison."""
#     return email.strip().lower()


# def create_user(username,email,password):
#     """Create and return a new user with an unverified email state."""
#     email = normalize_email(email)

#     user = User(username=username, email=email)
#     user.set_password(password)
#     if hasattr(user, "is_email_verified"):
#         user.is_email_verified = False
#     user.save()

#     return user


# def send_email_verification(user):
#     """Send an email verification message to the newly created user."""
#     token = generate_email_verification_token(user)
#     verification_link = build_email_verification_link(token)

#     subject = "Verify your Mini Blog account"
#     message = (
#         f"Hi {user.username},\n\n"
#         f"Please verify your email address by visiting the link below:\n\n"
#         f"{verification_link}\n\n"
#         "If you did not register for this account, please ignore this message.\n"
#     )

#     send_mail(
#         subject,
#         message,
#         getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
#         [user.email],
#         fail_silently=False,
#     )