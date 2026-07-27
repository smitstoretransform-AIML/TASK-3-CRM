from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.notifications import Notification
from app.models.users import User
from app.schemas.notifications import (
    NotificationListResponse,
    NotificationReadUpdate,
    NotificationResponse,
)


router = APIRouter(
    prefix="/api/v1/notifications",
    tags=["Notifications"]
)


@router.get(
    "/",
    response_model=NotificationListResponse
)
def list_notifications(
    is_read: bool | None = Query(
        default=None,
        description="Filter notifications by read status"
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number"
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of notifications per page"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id
        )
    )

    # Filter by read status
    if is_read is not None:
        query = query.filter(
            Notification.is_read == is_read
        )

    # Count total notifications
    total = query.with_entities(
        func.count(Notification.id)
    ).scalar()

    # Latest notifications first
    query = query.order_by(
        Notification.created_at.desc()
    )

    # Pagination
    offset = (
        page - 1
    ) * limit

    notifications = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = (
        ceil(total / limit)
        if total > 0
        else 0
    )

    return {
        "items": notifications,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse
)
def mark_notification_as_read(
    notification_id: int,
    notification_data: NotificationReadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    notification.is_read = notification_data.is_read

    db.commit()
    db.refresh(notification)

    return notification