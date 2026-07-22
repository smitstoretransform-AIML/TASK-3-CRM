from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: int


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)