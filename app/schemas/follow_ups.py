from datetime import date, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class FollowUpCreate(BaseModel):

    lead_id: int | None = Field(
        default=None,
        gt=0
    )

    customer_id: int | None = Field(
        default=None,
        gt=0
    )

    followup_date: date

    type: str = Field(
        ...,
        min_length=1
    )

    notes: str | None = None

    @model_validator(mode="after")
    def validate_relation(self):

        if (
            self.lead_id is None
            and self.customer_id is None
        ):
            raise ValueError(
                "Either lead_id or customer_id is required"
            )

        if (
            self.lead_id is not None
            and self.customer_id is not None
        ):
            raise ValueError(
                "Only one of lead_id or customer_id is allowed"
            )

        return self

    @field_validator("type")
    @classmethod
    def validate_type(
        cls,
        value: str
    ) -> str:

        value = value.strip()

        allowed_types = {
            "Call",
            "Email",
            "Meeting",
            "Note",
            "Follow-up",
        }

        if value not in allowed_types:

            raise ValueError(
                "Invalid follow-up type"
            )

        return value

    @field_validator("notes")
    @classmethod
    def validate_notes(
        cls,
        value: str | None
    ) -> str | None:

        if value is None:
            return None

        value = value.strip()

        if not value:

            raise ValueError(
                "Notes cannot be empty"
            )

        return value


class FollowUpResponse(BaseModel):

    id: int

    lead_id: int | None

    customer_id: int | None

    date: date

    type: str

    status: str

    notes: str | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class FollowUpListResponse(BaseModel):

    items: list[FollowUpResponse]

    page: int

    limit: int

    total: int

    total_pages: int


class FollowUpStatusUpdate(BaseModel):

    status: str

    @field_validator("status")
    @classmethod
    def validate_status(
        cls,
        value: str
    ) -> str:

        value = value.strip().lower()

        allowed_statuses = {
            "pending",
            "completed",
            "cancelled",
        }

        if value not in allowed_statuses:

            raise ValueError(
                "Invalid status"
            )

        return value