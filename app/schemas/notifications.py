from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    page: int
    limit: int
    total: int
    total_pages: int


class NotificationReadUpdate(BaseModel):
    is_read: bool