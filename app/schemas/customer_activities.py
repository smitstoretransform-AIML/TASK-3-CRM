from datetime import datetime
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
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

    # Activity can belong to a Lead OR Customer
    lead_id: int | None = Field(
        default=None,
        gt=0
    )

    customer_id: int | None = Field(
        default=None,
        gt=0
    )

    type: ActivityType

    description: str = Field(
        ...,
        min_length=1
    )

    # --------------------------------------------------------
    # VALIDATE LEAD / CUSTOMER OWNERSHIP
    # --------------------------------------------------------

    @model_validator(mode="after")
    def validate_activity_owner(self):

        # Neither Lead nor Customer provided
        if (
            self.lead_id is None
            and self.customer_id is None
        ):
            raise ValueError(
                "Either lead_id or customer_id must be provided"
            )

        # Both Lead and Customer provided
        if (
            self.lead_id is not None
            and self.customer_id is not None
        ):
            raise ValueError(
                "Only one of lead_id or customer_id can be provided"
            )

        return self

    # --------------------------------------------------------
    # VALIDATE DESCRIPTION
    # --------------------------------------------------------

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
# ACTIVITY DATA RESPONSE
# ============================================================

class CustomerActivityResponse(BaseModel):

    id: int

    lead_id: int | None

    customer_id: int | None

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

    id: int

    lead_id: int | None

    customer_id: int | None

    type: ActivityType

    description: str

    created_by: int

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