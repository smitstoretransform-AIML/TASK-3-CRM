from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FollowUpCreate(BaseModel):
    customer_id: int = Field(..., gt=0)
    followup_date: date
    type: str = Field(..., min_length=1)
    notes: str | None = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Follow-up type cannot be empty"
            )

        allowed_types = {
            "Call",
            "Email",
            "Meeting",
            "Note",
            "Follow-up",
        }

        if value not in allowed_types:
            raise ValueError(
                "Invalid follow-up type. "
                "Allowed values: Call, Email, Meeting, "
                "Note, Follow-up"
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
                "Notes cannot be empty if provided"
            )

        return value


class FollowUpUpdate(BaseModel):
    followup_date: date | None = None
    type: str | None = None
    status: str | None = None
    notes: str | None = None

    @field_validator("type")
    @classmethod
    def validate_type(
        cls,
        value: str | None
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError(
                "Follow-up type cannot be empty"
            )

        allowed_types = {
            "Call",
            "Email",
            "Meeting",
            "Note",
            "Follow-up",
        }

        if value not in allowed_types:
            raise ValueError(
                "Invalid follow-up type. "
                "Allowed values: Call, Email, Meeting, "
                "Note, Follow-up"
            )

        return value

    @field_validator("status")
    @classmethod
    def validate_status(
        cls,
        value: str | None
    ) -> str | None:
        if value is None:
            return None

        value = value.strip().lower()

        allowed_statuses = {
            "pending",
            "completed",
            "cancelled",
        }

        if value not in allowed_statuses:
            raise ValueError(
                "Invalid status. "
                "Allowed values: pending, completed, cancelled"
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
                "Notes cannot be empty if provided"
            )

        return value


class FollowUpResponse(BaseModel):
    id: int
    customer_id: int
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
                "Invalid status. "
                "Allowed values: pending, completed, cancelled"
            )

        return value