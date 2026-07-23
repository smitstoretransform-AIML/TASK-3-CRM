from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str = Field(..., min_length=1)
    company: str | None = None

    @field_validator("name", "phone")
    @classmethod
    def validate_required_fields(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty")

        return value

    @field_validator("company")
    @classmethod
    def validate_company(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        return value if value else None


class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=1)
    company: str | None = None

    @field_validator("name", "phone")
    @classmethod
    def validate_optional_fields(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty")

        return value

    @field_validator("company")
    @classmethod
    def validate_company(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        return value if value else None


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    company: str | None
    created_by: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True
    )