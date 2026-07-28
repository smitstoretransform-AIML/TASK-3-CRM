from math import ceil

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.responses import success_response
from app.models.notifications import Notification
from app.models.users import User
from app.schemas.notifications import (
    NotificationApiResponse,
    NotificationListApiResponse,
    NotificationListResponse,
    NotificationReadUpdate,
    NotificationResponse,
)


router = APIRouter(
    prefix="/api/v1/notifications",
    tags=["Notifications"],
)


# ============================================================
# LIST MY NOTIFICATIONS
# ============================================================

@router.get(
    "/",
    response_model=NotificationListApiResponse,
    status_code=status.HTTP_200_OK,
)
def list_notifications(
    is_read: bool | None = Query(
        default=None,
        description="Filter notifications by read status",
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of notifications per page",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    # ========================================================
    # BASE QUERY
    # ========================================================

    query = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id
        )
    )

    # ========================================================
    # FILTER BY READ STATUS
    # ========================================================

    if is_read is not None:
        query = query.filter(
            Notification.is_read == is_read
        )

    # ========================================================
    # COUNT TOTAL RECORDS
    # ========================================================

    total = query.with_entities(
        func.count(Notification.id)
    ).scalar()

    # ========================================================
    # SORTING
    # ========================================================

    query = query.order_by(
        Notification.created_at.desc()
    )

    # ========================================================
    # PAGINATION
    # ========================================================

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

    # ========================================================
    # BUILD PAGINATED RESPONSE DATA
    # ========================================================

    notification_list = NotificationListResponse(
        items=notifications,
        page=page,
        limit=limit,
        total=total,
        total_pages=total_pages,
    )

    # ========================================================
    # STANDARD SUCCESS RESPONSE
    # ========================================================

    return success_response(
        data=notification_list,
        message="Notifications fetched successfully",
        code=200,
    )


# ============================================================
# MARK NOTIFICATION AS READ / UNREAD
# ============================================================

@router.patch(
    "/{notification_id}/read",
    response_model=NotificationApiResponse,
    status_code=status.HTTP_200_OK,
)
def mark_notification_as_read(
    notification_id: int,
    notification_data: NotificationReadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    # ========================================================
    # FIND USER'S NOTIFICATION
    # ========================================================

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    # ========================================================
    # UPDATE READ STATUS
    # ========================================================

    notification.is_read = (
        notification_data.is_read
    )

    db.commit()
    db.refresh(notification)

    # ========================================================
    # STANDARD SUCCESS RESPONSE
    # ========================================================

    message = (
        "Notification marked as read"
        if notification.is_read
        else "Notification marked as unread"
    )

    return success_response(
        data=NotificationResponse.model_validate(
            notification
        ),
        message=message,
        code=200,
    )


# ============================================================
# GET SINGLE NOTIFICATION
# ============================================================

@router.get(
    "/{notification_id}",
    response_model=NotificationApiResponse,
    status_code=status.HTTP_200_OK,
)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    # ========================================================
    # FIND USER'S NOTIFICATION
    # ========================================================

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    # ========================================================
    # STANDARD SUCCESS RESPONSE
    # ========================================================

    return success_response(
        data=NotificationResponse.model_validate(
            notification
        ),
        message="Notification fetched successfully",
        code=200,
    )