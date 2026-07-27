from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


ActivityType = Literal[
    "Call",
    "Email",
    "Meeting",
    "Note",
    "Follow-up",
]


class CustomerActivityCreate(BaseModel):
    type: ActivityType
    description: str = Field(..., min_length=1)

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Description cannot be empty"
            )

        return value

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


class CustomerTimelineResponse(BaseModel):
    type: ActivityType
    description: str
    date: datetime