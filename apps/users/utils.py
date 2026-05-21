
from django.conf import settings
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired


TOKEN_EXPIRY_SECONDS = 60 * 60 * 24  # 24 hours


def generate_email_verification_token(user) -> str:
    """
    Create signed token for email verification.
    """

    data = {
        "user_id": user.id,
        "email": user.email,
    }

    token = signing.dumps(data)

    return token


def verify_email_verification_token(token: str):
    """
    Verify signed token and return payload.
    Returns None if token is invalid or expired.
    """

    try:
        data = signing.loads(
            token,
            max_age=TOKEN_EXPIRY_SECONDS
        )
        return data

    except (BadSignature, SignatureExpired):
        return None


def build_email_verification_link(token: str) -> str:
    """
    Build frontend/backend verification URL.
    """

    base_url = getattr(
        settings,
        "FRONTEND_URL",
        "http://localhost:3000"
    )

    return f"{base_url}/verify-email/?token={token}"