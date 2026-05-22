
from django.conf import settings
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired

TOKEN_EXPIRY_SECONDS = 60 * 60 * 24  # 24 hours


def generate_email_verification_token(user) -> str:
    """Create a signed verification token for email confirmation."""
    data = {
        "user_id": user.id,
        "email": user.email,
    }
    return signing.dumps(data)


def verify_email_verification_token(token: str):
    """Validate a verification token and return the payload if valid."""
    try:
        return signing.loads(token, max_age=TOKEN_EXPIRY_SECONDS)
    except (BadSignature, SignatureExpired):
        return None


def build_email_verification_link(token: str) -> str:
    """Build a backend verification URL for the email verification token."""
    base_url = getattr(settings, "BACKEND_URL", "http://localhost:8000")
    return f"{base_url.rstrip('/')}/auth/verify-email/{token}"
