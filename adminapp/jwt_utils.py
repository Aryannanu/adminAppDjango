import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings


def generate_jwt(app_user):
    payload = {
        'user_id': app_user.id,
        'username': app_user.username,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(
            seconds=settings.JWT_EXP_DELTA_SECONDS
        ),
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return token


def decode_jwt(token):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload

    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
