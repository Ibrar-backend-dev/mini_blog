from django.core import signing
from django.conf import settings


def generate_verification_token(user):

    return signing.dumps(
        {'user_id': user.id,
         "email": user.email,
         }
    )

def decode_verification_token(token):

    return signing.loads(
        token, max_age=60*60*24                 # Token valid for 24 hours

    )  

def build_verification_url(token):

    return(
        f"{settings.BACKEND_URL}"
        f"/auth/verify-email/{token}/"
    )





# from django.conf import settings
# from django.core import signing
# from django.core.signing import BadSignature, SignatureExpired

# TOKEN_EXPIRY_SECONDS = 60 * 60 * 24  # 24 hours


# def generate_email_verification_token(user):
#     """Create a signed verification token for email confirmation."""
#     data = {
#         "user_id": user.id,
#         "email": user.email,
#     }
#     return signing.dumps(data)


# def verify_email_verification_token(token):
#     """Validate a verification token and return the payload if valid."""
#     try:
#         return signing.loads(token, max_age=TOKEN_EXPIRY_SECONDS)
#     except (BadSignature, SignatureExpired):
#         return None


# def build_email_verification_link(token):
#     """Build a backend verification URL for the email verification token."""
#     base_url = getattr(settings, "BACKEND_URL", "http://localhost:8000")
#     return f"{base_url.rstrip('/')}/auth/verify-email/{token}"
