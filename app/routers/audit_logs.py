from datetime import datetime
from math import ceil

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_permission,
)
from app.models.audit_logs import AuditLog
from app.models.users import User
from app.schemas.audit_logs import AuditLogListResponse


router = APIRouter(
    prefix="/api/v1/audit-logs",
    tags=["Audit Logs"]
)

@router.get(
    "/",
    response_model=AuditLogListResponse,
    dependencies=[
        Depends(require_permission("view_audit_logs"))
    ]
)
def list_audit_logs(
    user_id: int | None = Query(
        default=None,
        gt=0,
        description="Filter audit logs by user ID"
    ),
    action: str | None = Query(
        default=None,
        description="Filter by action"
    ),
    module: str | None = Query(
        default=None,
        description="Filter by module"
    ),
    from_date: datetime | None = Query(
        default=None,
        description="Filter logs from this date"
    ),
    to_date: datetime | None = Query(
        default=None,
        description="Filter logs until this date"
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
        description="Number of logs per page"
    ),
    sort_by: str = Query(
        default="created_at",
        description=(
            "Sort field: id, user_id, action, "
            "module, created_at"
        )
    ),
    sort_order: str = Query(
        default="desc",
        description="Sort order: asc or desc"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ========================================================
    # DATE VALIDATION
    # ========================================================

    if (
        from_date is not None
        and to_date is not None
        and from_date > to_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "from_date cannot be greater "
                "than to_date"
            )
        )

    # ========================================================
    # SORT VALIDATION
    # ========================================================

    allowed_sort_fields = {
        "id": AuditLog.id,
        "user_id": AuditLog.user_id,
        "action": AuditLog.action,
        "module": AuditLog.module,
        "created_at": AuditLog.created_at,
    }

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid sort_by value. "
                "Allowed values: id, user_id, action, "
                "module, created_at"
            )
        )

    sort_order = sort_order.lower()

    if sort_order not in {"asc", "desc"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "sort_order must be either "
                "'asc' or 'desc'"
            )
        )

    # ========================================================
    # BASE QUERY
    # ========================================================

    query = db.query(AuditLog)

    # ========================================================
    # FILTER BY USER
    # ========================================================

    if user_id is not None:
        query = query.filter(
            AuditLog.user_id == user_id
        )

    # ========================================================
    # FILTER BY ACTION
    # ========================================================

    if action:
        action_value = action.strip()

        if action_value:
            query = query.filter(
                AuditLog.action.ilike(
                    action_value
                )
            )

    # ========================================================
    # FILTER BY MODULE
    # ========================================================

    if module:
        module_value = module.strip()

        if module_value:
            query = query.filter(
                AuditLog.module.ilike(
                    module_value
                )
            )

    # ========================================================
    # FILTER BY START DATE
    # ========================================================

    if from_date is not None:
        query = query.filter(
            AuditLog.created_at >= from_date
        )

    # ========================================================
    # FILTER BY END DATE
    # ========================================================

    if to_date is not None:
        query = query.filter(
            AuditLog.created_at <= to_date
        )

    # ========================================================
    # COUNT TOTAL RECORDS
    # ========================================================

    total = query.with_entities(
        func.count(AuditLog.id)
    ).scalar()

    # ========================================================
    # APPLY SORTING
    # ========================================================

    sort_column = allowed_sort_fields[sort_by]

    if sort_order == "asc":
        query = query.order_by(
            sort_column.asc()
        )
    else:
        query = query.order_by(
            sort_column.desc()
        )

    # ========================================================
    # PAGINATION
    # ========================================================

    offset = (
        page - 1
    ) * limit

    audit_logs = (
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
        "items": audit_logs,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }