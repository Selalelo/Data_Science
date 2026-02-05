from pydantic import BaseModel, Field, validator
from datetime import date


# South African Provinces
SA_PROVINCES = [
    "Eastern Cape",
    "Free State",
    "Gauteng",
    "KwaZulu-Natal",
    "Limpopo",
    "Mpumalanga",
    "North West",
    "Northern Cape",
    "Western Cape"
]


class LoginRequest(BaseModel):
    """Login request schema"""
    surname: str = Field(..., min_length=1, description="User's surname")
    password: str = Field(..., min_length=1, description="User's password")


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    password: str = Field(..., max_length=20, min_length=1)
    first_name: str = Field(..., max_length=50, min_length=1)
    last_name: str = Field(..., max_length=50, min_length=1)
    date_of_birth: date
    province: str = Field(..., max_length=20)
    gender: str = Field(..., max_length=6)
    facilitator: bool

    @validator('province')
    def validate_province(cls, v: str) -> str:
        if v not in SA_PROVINCES:
            raise ValueError(f'Province must be one of: {", ".join(SA_PROVINCES)}')
        return v

    @validator('gender')
    def validate_gender(cls, v: str) -> str:
        valid_genders = ['Male', 'Female', 'Other']
        if v not in valid_genders:
            raise ValueError(f'Gender must be one of: {", ".join(valid_genders)}')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user details (FirstName and LastName only)"""
    first_name: str = Field(..., max_length=50, min_length=1)
    last_name: str = Field(..., max_length=50, min_length=1)


class UserResponse(BaseModel):
    """Schema for user response"""
    user_id: int
    first_name: str
    last_name: str
    date_of_birth: date
    province: str
    gender: str
    facilitator: bool

    class Config:
        from_attributes = True


class UserDetailResponse(BaseModel):
    """Detailed user response including all fields"""
    user_id: int
    password: str
    first_name: str
    last_name: str
    date_of_birth: date
    province: str
    gender: str
    facilitator: bool

    class Config:
        from_attributes = True