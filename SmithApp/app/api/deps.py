from fastapi import Cookie, HTTPException, status, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import verify_session_token
from typing import Optional, TypedDict, cast


class UserData(TypedDict):
    """Type definition for user data dictionary"""
    id: str
    email: str


def get_current_user(
    session_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
) -> UserData:
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user_data = cast(UserData, verify_session_token(session_token))
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    return user_data


def get_optional_current_user(
    session_token: Optional[str] = Cookie(None)
) -> Optional[UserData]:
    if not session_token:
        return None
    
    return cast(Optional[UserData], verify_session_token(session_token))