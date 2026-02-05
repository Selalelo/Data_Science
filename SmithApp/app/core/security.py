from itsdangerous import URLSafeTimedSerializer
from core.config import settings 

def get_serializer():
    """Get serializer for session management"""
    return URLSafeTimedSerializer(settings.SECRET_KEY)

def create_session_token(user_id: int, surname: str) -> str:
    serializer = get_serializer()
    token = serializer.dumps({"user_id": user_id, "surname": surname})
    return token.decode() if isinstance(token, bytes) else token


def verify_session_token(token: str, max_age: int | None = None) -> dict[str, int] | None:
    serializer = get_serializer()
    try:
        if max_age is None:
            max_age = getattr(settings, "SESSION_MAX_AGE", 3600) 
        
        data = serializer.loads(token, max_age=max_age)
        return data
    except Exception:
        return None

def verify_password(plain_password: str, stored_password: str) -> bool:
    return plain_password == stored_password
