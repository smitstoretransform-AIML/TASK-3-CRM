from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.schemas.common import APIResponse

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=1)
    role_id: int = Field(..., gt=0)

    @field_validator("name", "password")
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty")

        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

    @field_validator("password")
    @classmethod
    def validate_password_not_empty(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Password cannot be empty")

        return value


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserRegisterResponse( APIResponse[UserResponse] ): pass 
class UserLoginResponse( APIResponse[TokenResponse] ): pass 
class UserProfileResponse( APIResponse[UserResponse] ): pass