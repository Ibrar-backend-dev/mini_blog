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


