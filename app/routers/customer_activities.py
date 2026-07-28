from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permission
from app.core.responses import success_response

from app.models.customer_activities import CustomerActivity
from app.models.customers import Customer
from app.models.users import User

from app.schemas.customer_activities import (
    CustomerActivityCreate,
    CustomerActivityCreateApiResponse,
    CustomerActivityResponse,
    CustomerTimelineApiResponse,
    CustomerTimelineResponse,
)


router = APIRouter(
    prefix="/api/v1/customers",
    tags=["Customer Activities"]
)


# ============================================================
# CREATE CUSTOMER ACTIVITY
# ============================================================

@router.post(
    "/{customer_id}/activities",
    response_model=CustomerActivityCreateApiResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer_activity(
    customer_id: int,
    activity_data: CustomerActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("create_customer_activity")
    )
):
    # --------------------------------------------------------
    # Check if customer exists
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Create customer activity
    # --------------------------------------------------------

    new_activity = CustomerActivity(
        customer_id=customer_id,
        type=activity_data.type,
        description=activity_data.description,
        created_by=current_user.id
    )

    db.add(new_activity)

    db.commit()
    db.refresh(new_activity)

    # --------------------------------------------------------
    # Convert SQLAlchemy model to Pydantic response
    # --------------------------------------------------------

    activity_response = (
        CustomerActivityResponse.model_validate(
            new_activity
        )
    )

    # --------------------------------------------------------
    # Standard success response
    # --------------------------------------------------------

    return success_response(
        data=activity_response,
        message="Customer activity created successfully",
        code=201
    )


# ============================================================
# GET CUSTOMER TIMELINE
# ============================================================

@router.get(
    "/{customer_id}/timeline",
    response_model=CustomerTimelineApiResponse,
    status_code=status.HTTP_200_OK
)
def get_customer_timeline(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("view_customers")
    )
):
    # --------------------------------------------------------
    # Check if customer exists
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Get customer activities
    # --------------------------------------------------------

    activities = (
        db.query(CustomerActivity)
        .filter(
            CustomerActivity.customer_id == customer_id
        )
        .order_by(
            CustomerActivity.created_at.asc()
        )
        .all()
    )

    # --------------------------------------------------------
    # Convert SQLAlchemy models to Pydantic responses
    # --------------------------------------------------------

    timeline_data = [
        CustomerTimelineResponse(
            type=activity.type,
            description=activity.description,
            date=activity.created_at
        )
        for activity in activities
    ]

    # --------------------------------------------------------
    # Standard success response
    # --------------------------------------------------------

    return success_response(
        data=timeline_data,
        message="Customer timeline retrieved successfully",
        code=200
    )

