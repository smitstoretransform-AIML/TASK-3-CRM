from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permission
from app.models.customer_activities import CustomerActivity
from app.models.customers import Customer
from app.models.users import User

from app.schemas.customer_activities import (
    CustomerActivityCreate,
    CustomerActivityResponse,
    CustomerTimelineResponse,
)

router = APIRouter(
    prefix="/api/v1/customers",
    tags=["Customer Activities"]
)


@router.post(
    "/{customer_id}/activities",
    response_model=CustomerActivityResponse,
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
    # Check if customer exists
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

    # # Verify created_by user exists
    # created_by_user = (
    #     db.query(User)
    #     .filter(
    #         User.id == activity_data.created_by
    #     )
    #     .first()
    # )

    # if not created_by_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Created by user not found"
    #     )




    # Create activity
    new_activity = CustomerActivity(
        customer_id=customer_id,
        type=activity_data.type,
        description=activity_data.description,
        created_by=current_user.id
)





    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    return new_activity


@router.get(
    "/{customer_id}/timeline",
    response_model=list[CustomerTimelineResponse]
)
def get_customer_timeline(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("view_customers")
    )
):
    # Check if customer exists
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

    # Get customer activities
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

    return [
        {
            "type": activity.type,
            "description": activity.description,
            "date": activity.created_at,
        }
        for activity in activities
    ]