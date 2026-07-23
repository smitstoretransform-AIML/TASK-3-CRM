from pydantic import BaseModel, ConfigDict, Field


class RolePermissionCreate(BaseModel):
    role_id: int = Field(..., gt=0)
    permission_id: int = Field(..., gt=0)


class RolePermissionResponse(BaseModel):
    id: int
    role_id: int
    permission_id: int

    model_config = ConfigDict(
        from_attributes=True
    )