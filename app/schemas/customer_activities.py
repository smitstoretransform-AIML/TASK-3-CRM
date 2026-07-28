from datetime import datetime
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


ActivityType = Literal[
    "Call",
    "Email",
    "Meeting",
    "Note",
    "Follow-up",
]


# ============================================================
# CREATE CUSTOMER ACTIVITY REQUEST
# ============================================================

class CustomerActivityCreate(BaseModel):
    type: ActivityType

    description: str = Field(
        ...,
        min_length=1
    )

    @field_validator("description")
    @classmethod
    def validate_description(
        cls,
        value: str
    ) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Description cannot be empty"
            )

        return value


# ============================================================
# CUSTOMER ACTIVITY DATA RESPONSE
# ============================================================

class CustomerActivityResponse(BaseModel):
    id: int
    customer_id: int
    type: ActivityType
    description: str
    created_by: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# CUSTOMER TIMELINE ITEM RESPONSE
# ============================================================

class CustomerTimelineResponse(BaseModel):
    type: ActivityType
    description: str
    date: datetime


# ============================================================
# STANDARD API RESPONSE - CREATE ACTIVITY
# ============================================================

class CustomerActivityCreateApiResponse(BaseModel):
    code: int
    status: str
    message: str
    data: CustomerActivityResponse


# ============================================================
# STANDARD API RESPONSE - CUSTOMER TIMELINE
# ============================================================

class CustomerTimelineApiResponse(BaseModel):
    code: int
    status: str
    message: str
    data: list[CustomerTimelineResponse]
