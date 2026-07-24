from datetime import datetime
import re

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class LeadCreate(BaseModel):
    name: str = Field(...)
    email: EmailStr
    phone: str = Field(...)
    company: str | None = None
    source: str = Field(...)
    status: str = Field(...)
    assigned_to: int | None = Field(
        default=None,
        gt=0
    )

    @field_validator("name", "source", "status")
    @classmethod
    def validate_required_strings(
        cls,
        value: str
    ) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "This field cannot be empty"
            )

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(
        cls,
        value: str
    ) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Phone number cannot be empty"
            )

        if not re.fullmatch(
            r"\d{10}",
            value
        ):
            raise ValueError(
                "Phone number must contain exactly 10 digits"
            )

        return value

    @field_validator("company")
    @classmethod
    def validate_company(
        cls,
        value: str | None
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError(
                "Company cannot be empty if provided"
            )

        return value


class LeadUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    company: str | None = None
    source: str | None = None
    status: str | None = None
    assigned_to: int | None = Field(
        default=None,
        gt=0
    )

    @field_validator(
        "name",
        "source",
        "status"
    )
    @classmethod
    def validate_optional_strings(
        cls,
        value: str | None
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError(
                "This field cannot be empty"
            )

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(
        cls,
        value: str | None
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError(
                "Phone number cannot be empty"
            )

        if not re.fullmatch(
            r"\d{10}",
            value
        ):
            raise ValueError(
                "Phone number must contain exactly 10 digits"
            )

        return value

    @field_validator("company")
    @classmethod
    def validate_company(
        cls,
        value: str | None
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError(
                "Company cannot be empty if provided"
            )

        return value


class LeadResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    company: str | None
    source: str
    status: str
    assigned_to: int | None
    created_by: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True
    )


class LeadListResponse(BaseModel):
    items: list[LeadResponse]
    page: int
    limit: int
    total: int
    total_pages: int