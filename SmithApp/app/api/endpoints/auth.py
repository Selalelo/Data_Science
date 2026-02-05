from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Dict, Any
from core.database import get_db
from schemas.user import LoginRequest
from services.user_service import UserService
from core.security import create_session_token
from core.config import settings


router = APIRouter()


@router.post("/login")
def login(
    credentials: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
   
    # Validate empty fields
    if not credentials.surname or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Surname and password are required"
        )
    
    # Authenticate user
    user = UserService.authenticate_user(db, credentials.surname, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid surname or password"
        )
    
    # Create session token
    token = create_session_token(user["user_id"], user["surname"])
    
    # Set session cookie
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        max_age=settings.SESSION_MAX_AGE,
        samesite="lax"
    )
    
    return {
        "message": "Login successful",
        "user": user
    }


@router.post("/logout")
def logout(response: Response):
    """
    Logout user by clearing session cookie
    
    Args:
        response: FastAPI response object
        
    Returns:
        Success message
    """
    response.delete_cookie(key="session_token")
    return {"message": "Logout successful"}