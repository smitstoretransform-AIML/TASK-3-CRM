from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: int
    user_id: int | None
    action: str
    module: str
    old_data: dict | None
    new_data: dict | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]
    page: int
    limit: int
    total: int
    total_pages: int