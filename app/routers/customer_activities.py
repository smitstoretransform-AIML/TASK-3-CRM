from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permission
from app.core.responses import success_response

from app.models.customer_activities import CustomerActivity
from app.models.customers import Customer
from app.models.leads import Lead
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
# CREATE ACTIVITY
# ============================================================

@router.post(
    "/activities",
    response_model=CustomerActivityCreateApiResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer_activity(
    activity_data: CustomerActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_permission("create_customer_activity")
    )
):

    # ========================================================
    # LEAD ACTIVITY
    # ========================================================

    if activity_data.lead_id is not None:

        lead = (
            db.query(Lead)
            .filter(
                Lead.id == activity_data.lead_id,
                Lead.deleted_at.is_(None)
            )
            .first()
        )

        if not lead:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead not found"
            )

        new_activity = CustomerActivity(
            lead_id=activity_data.lead_id,
            customer_id=None,
            type=activity_data.type,
            description=activity_data.description,
            created_by=current_user.id
        )

    # ========================================================
    # CUSTOMER ACTIVITY
    # ========================================================

    else:

        customer = (
            db.query(Customer)
            .filter(
                Customer.id == activity_data.customer_id,
                Customer.deleted_at.is_(None)
            )
            .first()
        )

        if not customer:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        new_activity = CustomerActivity(
            lead_id=None,
            customer_id=activity_data.customer_id,
            type=activity_data.type,
            description=activity_data.description,
            created_by=current_user.id
        )

    # ========================================================
    # SAVE ACTIVITY
    # ========================================================

    db.add(new_activity)

    db.commit()

    db.refresh(new_activity)

    # ========================================================
    # RESPONSE
    # ========================================================

    activity_response = (
        CustomerActivityResponse.model_validate(
            new_activity,
            from_attributes=True
        )
    )

    return success_response(
        data=activity_response.model_dump(
            mode="json"
        ),
        message="Activity created successfully",
        code=status.HTTP_201_CREATED
    )


# ============================================================
# GET COMPLETE CUSTOMER TIMELINE
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

    # ========================================================
    # FIND CUSTOMER
    # ========================================================

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

    # ========================================================
    # BUILD TIMELINE QUERY
    # ========================================================

    # Always get activities directly belonging
    # to the current customer.
    #
    # If customer was converted from a lead,
    # also get all activities belonging to
    # the original lead.

    if customer.lead_id is not None:

        activities = (
            db.query(CustomerActivity)
            .filter(
                or_(
                    CustomerActivity.customer_id == customer.id,
                    CustomerActivity.lead_id == customer.lead_id
                )
            )
            .order_by(
                CustomerActivity.created_at.asc()
            )
            .all()
        )

    else:

        activities = (
            db.query(CustomerActivity)
            .filter(
                CustomerActivity.customer_id == customer.id
            )
            .order_by(
                CustomerActivity.created_at.asc()
            )
            .all()
        )

    # ========================================================
    # BUILD TIMELINE RESPONSE
    # ========================================================

    timeline_data = [

        CustomerTimelineResponse(
            id=activity.id,
            lead_id=activity.lead_id,
            customer_id=activity.customer_id,
            type=activity.type,
            description=activity.description,
            created_by=activity.created_by,
            date=activity.created_at
        )

        for activity in activities
    ]

    # ========================================================
    # RETURN TIMELINE
    # ========================================================

    return success_response(
        data=[
            item.model_dump(
                mode="json"
            )
            for item in timeline_data
        ],
        message="Customer timeline retrieved successfully",
        code=status.HTTP_200_OK
    )