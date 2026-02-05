from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.user import User, UserDetails
from schemas.user import UserCreate, UserUpdate
from typing import List, Optional, TypedDict
from datetime import date


class AuthenticatedUserResponse(TypedDict):
    """Type definition for authenticated user response"""
    user_id: int
    surname: str
    first_name: str
    full_name: str


class UserService:
    """Service class for user operations"""

    @staticmethod
    def authenticate_user(db: Session, surname: str, password: str) -> Optional[AuthenticatedUserResponse]:
        """
        Authenticate user by surname and password
        
        Args:
            db: Database session
            surname: User's surname (last_name)
            password: User's password
            
        Returns:
            User data if authenticated, None otherwise
        """
        # Find user by surname
        user_details = db.query(UserDetails).filter(
            UserDetails.last_name == surname
        ).first()

        if not user_details:
            return None

        # Get user and verify password
        user = db.query(User).filter(User.user_id == user_details.user_id).first()
        
        if user and user.password == password:
            return {
                "user_id": user.user_id,
                "surname": user_details.last_name,
                "first_name": user_details.first_name,
                "full_name": f"{user_details.first_name} {user_details.last_name}"
            }
        
        return None

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> dict:
        """
        Create a new user with details
        
        Args:
            db: Database session
            user_data: User creation data
            
        Returns:
            Created user data
        """
        # Create user
        new_user = User(password=user_data.password)
        db.add(new_user)
        db.flush()  # Get user_id

        # Create user details
        new_details = UserDetails(
            user_id=new_user.user_id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            date_of_birth=user_data.date_of_birth,
            province=user_data.province,
            gender=user_data.gender,
            facilitator=user_data.facilitator
        )
        db.add(new_details)
        db.commit()
        db.refresh(new_user)
        db.refresh(new_details)

        return {
            "user_id": new_user.user_id,
            "first_name": new_details.first_name,
            "last_name": new_details.last_name,
            "date_of_birth": new_details.date_of_birth,
            "province": new_details.province,
            "gender": new_details.gender,
            "facilitator": new_details.facilitator
        }

    @staticmethod
    def get_all_users(db: Session) -> List[dict]:
        """
        Get all users with their details
        
        Args:
            db: Database session
            
        Returns:
            List of user data
        """
        users = db.query(UserDetails).all()
        return [
            {
                "user_id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.full_name,
                "date_of_birth": user.date_of_birth,
                "province": user.province,
                "gender": user.gender,
                "facilitator": user.facilitator
            }
            for user in users
        ]

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[dict]:
        """
        Get user by ID
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User data or None
        """
        user_details = db.query(UserDetails).filter(
            UserDetails.user_id == user_id
        ).first()

        if not user_details:
            return None

        return {
            "user_id": user_details.user_id,
            "first_name": user_details.first_name,
            "last_name": user_details.last_name,
            "full_name": user_details.full_name,
            "date_of_birth": user_details.date_of_birth,
            "province": user_details.province,
            "gender": user_details.gender,
            "facilitator": user_details.facilitator
        }

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[dict]:
        """
        Update user details (FirstName and LastName only)
        
        Args:
            db: Database session
            user_id: User ID
            user_data: Update data
            
        Returns:
            Updated user data or None
        """
        user_details = db.query(UserDetails).filter(
            UserDetails.user_id == user_id
        ).first()

        if not user_details:
            return None

        user_details.first_name = user_data.first_name
        user_details.last_name = user_data.last_name
        
        db.commit()
        db.refresh(user_details)

        return {
            "user_id": user_details.user_id,
            "first_name": user_details.first_name,
            "last_name": user_details.last_name,
            "full_name": user_details.full_name,
            "date_of_birth": user_details.date_of_birth,
            "province": user_details.province,
            "gender": user_details.gender,
            "facilitator": user_details.facilitator
        }

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        Delete user and their details
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            True if deleted, False otherwise
        """
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            return False

        db.delete(user)  
        db.commit()
        return True