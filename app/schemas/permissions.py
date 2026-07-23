from pydantic import BaseModel, ConfigDict, Field, field_validator


class PermissionCreate(BaseModel):
    name: str = Field(..., min_length=1)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Permission name cannot be empty")

        return value


class PermissionResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )