from datetime import date
from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.audit import create_audit_log
from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_permission,
)
from app.core.responses import (
    APIResponse,
    success_response,
)
from app.models.customers import Customer
from app.models.follow_ups import FollowUp
from app.models.users import User
from app.models.leads import Lead

from app.schemas.follow_ups import (
    FollowUpCreate,
    FollowUpResponse,
    FollowUpStatusUpdate,
)


router = APIRouter(
    prefix="/api/v1/followups",
    tags=["Follow-ups"]
)

# ============================================================
# CREATE FOLLOW-UP
# ============================================================

@router.post(
    "/",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED
)
def create_follow_up(
    follow_up_data: FollowUpCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("create_followup")
    )
):

    # ========================================================
    # VALIDATE LEAD
    # ========================================================

    if follow_up_data.lead_id is not None:

        lead = (
            db.query(Lead)
            .filter(
                Lead.id == follow_up_data.lead_id,
                Lead.deleted_at.is_(None)
            )
            .first()
        )

        if not lead:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead not found"
            )

    # ========================================================
    # VALIDATE CUSTOMER
    # ========================================================

    if follow_up_data.customer_id is not None:

        customer = (
            db.query(Customer)
            .filter(
                Customer.id == follow_up_data.customer_id,
                Customer.deleted_at.is_(None)
            )
            .first()
        )

        if not customer:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

    # ========================================================
    # CREATE FOLLOW-UP
    # ========================================================

    new_follow_up = FollowUp(
        lead_id=follow_up_data.lead_id,
        customer_id=follow_up_data.customer_id,
        date=follow_up_data.followup_date,
        type=follow_up_data.type,
        status="pending",
        notes=follow_up_data.notes
    )

    db.add(new_follow_up)

    db.flush()

    # ========================================================
    # CREATE AUDIT LOG
    # ========================================================

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="CREATE",
        module="followups",
        old_data=None,
        new_data={
            "id": new_follow_up.id,
            "lead_id": new_follow_up.lead_id,
            "customer_id": new_follow_up.customer_id,
            "date": str(new_follow_up.date),
            "type": new_follow_up.type,
            "status": new_follow_up.status,
            "notes": new_follow_up.notes,
        }
    )

    db.commit()

    db.refresh(new_follow_up)

    return success_response(
        data=FollowUpResponse.model_validate(
            new_follow_up
        ).model_dump(
            mode="json"
        ),
        message="Follow-up created successfully",
        code=201
    )

# ============================================================
# LIST FOLLOW-UPS
# ============================================================

@router.get(
    "/",
    response_model=APIResponse
)
def list_follow_ups(
    status_filter: str | None = Query(
        default=None,
        alias="status",
        description=(
            "Filter by status: pending, completed, cancelled"
        )
    ),
    date_filter: str | None = Query(
        default=None,
        alias="date",
        description=(
            "Filter by date: today, upcoming, overdue"
        )
    ),
    lead_id: int | None = Query(
        default=None,
        gt=0,
        description="Filter follow-ups by lead ID"
    ),

    customer_id: int | None = Query(
        default=None,
        gt=0,
        description="Filter follow-ups by customer ID"
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
        description="Number of follow-ups per page"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("view_customers")
    )
):
    query = db.query(FollowUp)

    # ========================================================
    # STATUS FILTER
    # ========================================================

    if status_filter:
        status_value = status_filter.strip().lower()

        allowed_statuses = {
            "pending",
            "completed",
            "cancelled",
        }

        if status_value not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid status. "
                    "Allowed values: pending, completed, cancelled"
                )
            )

        query = query.filter(
            FollowUp.status == status_value
        )

    # ========================================================
    # CUSTOMER FILTER
    # ========================================================

    if customer_id is not None:
        query = query.filter(
            FollowUp.customer_id == customer_id
        )

    # ========================================================
    # LEAD FILTER
    # ========================================================

        if lead_id is not None:

            query = query.filter(
                FollowUp.lead_id == lead_id
            )

    # ========================================================
    # DATE CATEGORY FILTER
    # ========================================================

    if date_filter:
        date_value = date_filter.strip().lower()

        today = date.today()

        if date_value == "today":

            query = query.filter(
                FollowUp.date == today
            )

        elif date_value == "upcoming":

            query = query.filter(
                FollowUp.date > today
            )

        elif date_value == "overdue":

            query = query.filter(
                FollowUp.date < today,
                FollowUp.status == "pending"
            )

        else:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid date filter. "
                    "Allowed values: today, upcoming, overdue"
                )
            )

    # ========================================================
    # COUNT TOTAL RECORDS
    # ========================================================

    total = query.with_entities(
        func.count(FollowUp.id)
    ).scalar()

    # ========================================================
    # SORTING
    # ========================================================

    query = query.order_by(
        FollowUp.date.asc()
    )

    # ========================================================
    # PAGINATION
    # ========================================================

    offset = (
        page - 1
    ) * limit

    follow_ups = (
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
    # SERIALIZE FOLLOW-UPS
    # ========================================================

    response_data = {
        "items": [
            FollowUpResponse.model_validate(
                follow_up
            ).model_dump(mode="json")
            for follow_up in follow_ups
        ],
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }

    # ========================================================
    # STANDARD SUCCESS RESPONSE
    # ========================================================

    return success_response(
        data=response_data,
        message="Follow-ups retrieved successfully",
        code=200
    )


# ============================================================
# UPDATE FOLLOW-UP STATUS
# ============================================================

@router.patch(
    "/{followup_id}/status",
    response_model=APIResponse
)
def update_follow_up_status(
    followup_id: int,
    status_data: FollowUpStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("update_followup")
    )
):
    # Find follow-up
    follow_up = (
        db.query(FollowUp)
        .filter(
            FollowUp.id == followup_id
        )
        .first()
    )

    if not follow_up:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow-up not found"
        )

    # Capture old and new status
    old_status = follow_up.status
    new_status = status_data.status

    # ========================================================
    # SAME STATUS
    # ========================================================

    if old_status == new_status:

        return success_response(
            data=FollowUpResponse.model_validate(
                follow_up
            ).model_dump(mode="json"),
            message="Follow-up status is already up to date",
            code=200
        )

    # ========================================================
    # UPDATE STATUS
    # ========================================================

    follow_up.status = new_status

    # ========================================================
    # CREATE AUDIT LOG
    # ========================================================

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="UPDATE_STATUS",
        module="followups",
        old_data={
            "id": follow_up.id,
            "status": old_status,
        },
        new_data={
            "id": follow_up.id,
            "status": new_status,
        }
    )

    db.commit()
    db.refresh(follow_up)

    # ========================================================
    # STANDARD SUCCESS RESPONSE
    # ========================================================

    return success_response(
        data=FollowUpResponse.model_validate(
            follow_up
        ).model_dump(mode="json"),
        message="Follow-up status updated successfully",
        code=200
    )


# ============================================================
# GET LEAD FOLLOW-UPS
# ============================================================

@router.get(
    "/leads/{lead_id}",
    response_model=APIResponse
)
def get_lead_follow_ups(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("view_customers")
    )
):
    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id,
            Lead.deleted_at.is_(None)
        )
        .first()
    )

    if not lead:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )

    follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.lead_id == lead_id
        )
        .order_by(
            FollowUp.date.asc()
        )
        .all()
    )

    return success_response(
        data=[
            FollowUpResponse.model_validate(
                follow_up
            ).model_dump(
                mode="json"
            )
            for follow_up in follow_ups
        ],
        message="Lead follow-ups retrieved successfully",
        code=200
    )


# ============================================================
# GET CUSTOMER FOLLOW-UPS
# ============================================================

@router.get(
    "/customers/{customer_id}",
    response_model=APIResponse
)
def get_customer_follow_ups(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("view_customers")
    )
):
    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.deleted_at.is_(None)
        )
        .first()
    )

    if not customer:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.customer_id == customer_id
        )
        .order_by(
            FollowUp.date.asc()
        )
        .all()
    )

    return success_response(
        data=[
            FollowUpResponse.model_validate(
                follow_up
            ).model_dump(
                mode="json"
            )
            for follow_up in follow_ups
        ],
        message="Customer follow-ups retrieved successfully",
        code=200
    )