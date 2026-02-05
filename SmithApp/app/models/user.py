from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class User(Base):
    """
    Users table
    Stores user authentication information
    """
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    password = Column(String(20), nullable=False)

    # Relationship to UserDetails
    details = relationship("UserDetails", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(user_id={self.user_id})>"


class UserDetails(Base):
    """
    UserDetails table
    Stores user personal information
    """
    __tablename__ = "user_details"

    user_details_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    province = Column(String(20), nullable=False)
    gender = Column(String(6), nullable=False)
    facilitator = Column(Boolean, nullable=False, default=False)

    # Relationship to User
    user = relationship("User", back_populates="details")

    def __repr__(self):
        return f"<UserDetails(user_id={self.user_id}, name={self.first_name} {self.last_name})>"

    @property
    def full_name(self):
        """Get full name"""
        return f"{self.first_name} {self.last_name}"