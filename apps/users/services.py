from django.contrib.auth import get_user_model

User = get_user_model()


def normalize_email(email: str) -> str:
    return email.strip().lower()


def create_user(
    username: str,
    email: str,
    password: str,
):
    email = normalize_email(email)
    user = User(
        username=username,
        email=email,
    )
    user.set_password(password)
    user.is_verified = False
    user.save()
    
    return user
