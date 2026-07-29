from datetime import datetime
import re
from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


# ============================================================
# LEAD STATUS
# ============================================================

LeadStatus = Literal[
    "New",
    "Contacted",
    "Interested",
    "Qualified",
    "Converted",
    "Lost",
]


# ============================================================
# CREATE LEAD
# ============================================================

class LeadCreate(BaseModel):

    name: str = Field(...)

    email: EmailStr

    phone: str = Field(...)

    company: str | None = None

    source: str = Field(...)

    status: LeadStatus = Field(
        default="New"
    )

    assigned_to: int | None = Field(
        default=None,
        gt=0
    )

    # --------------------------------------------------------
    # Validate required string fields
    # --------------------------------------------------------

    @field_validator(
        "name",
        "source"
    )
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

    # --------------------------------------------------------
    # Validate phone
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Validate company
    # --------------------------------------------------------

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


# ============================================================
# UPDATE LEAD
# ============================================================

class LeadUpdate(BaseModel):

    name: str | None = None

    email: EmailStr | None = None

    phone: str | None = None

    company: str | None = None

    source: str | None = None

    status: LeadStatus | None = None

    assigned_to: int | None = Field(
        default=None,
        gt=0
    )

    # --------------------------------------------------------
    # Validate optional string fields
    # --------------------------------------------------------

    @field_validator(
        "name",
        "source"
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

    # --------------------------------------------------------
    # Validate phone
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Validate company
    # --------------------------------------------------------

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


# ============================================================
# LEAD RESPONSE
# ============================================================

class LeadResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    phone: str

    company: str | None

    source: str

    status: LeadStatus

    assigned_to: int | None

    created_by: int

    created_at: datetime

    updated_at: datetime

    deleted_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# LEAD LIST RESPONSE
# ============================================================

class LeadListResponse(BaseModel):

    items: list[LeadResponse]

    page: int

    limit: int

    total: int

    total_pages: int


# ============================================================
# SINGLE LEAD API RESPONSE
# ============================================================

class LeadSingleResponse(BaseModel):

    code: int

    status: str

    message: str

    data: LeadResponse


# ============================================================
# LEAD LIST API RESPONSE
# ============================================================

class LeadListWrapperResponse(BaseModel):

    code: int

    status: str

    message: str

    data: LeadListResponse


# ============================================================
# GENERIC LEAD API RESPONSE
# ============================================================

class LeadGenericResponse(BaseModel):

    code: int

    status: str

    message: str

    data: Any | None = None