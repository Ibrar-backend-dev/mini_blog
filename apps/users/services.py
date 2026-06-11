from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.conf import settings

from .utils import generate_verification_token , build_verification_url

User = get_user_model()

# E-mail normalization
def normalize_email(email):
    return email.strip().lower()

# User creation
def create_user(username, email, password):
    email = normalize_email(email)

    return User.objects.create_user(
        username = username,
        email = email,
        password = password
    )

# User authentication and  credential verification
def authenticate_user( *, email, password):
    email = normalize_email(email)

    try:
        user = User.objects.get(email = email)
        
    except User.DoesNotExist:
        raise ValidationError("Invalid email or password.")
    
    if not user.check_password(password):
        raise ValidationError("Invalid email or password.")
    
    if not user.is_email_verified:
        raise ValidationError("Verify your email first.")
    
    return user

#E-mail verification and sending verification e-mails
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



