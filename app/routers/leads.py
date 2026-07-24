from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_permission,
)
from app.models.leads import Lead
from app.models.users import User
from app.schemas.leads import LeadCreate, LeadResponse


router = APIRouter(
    prefix="/api/v1/leads",
    tags=["Leads"]
)


@router.post(
    "/",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission("create_lead"))
    ]
)
def create_lead(
    lead_data: LeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if an active lead with the same email already exists
    existing_lead = (
        db.query(Lead)
        .filter(
            Lead.email == lead_data.email,
            Lead.deleted_at.is_(None)
        )
        .first()
    )

    if existing_lead:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lead with this email already exists"
        )

    # Validate assigned user if assignment is provided
    if lead_data.assigned_to is not None:
        assigned_user = (
            db.query(User)
            .filter(
                User.id == lead_data.assigned_to
            )
            .first()
        )

        if not assigned_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assigned user not found"
            )

    new_lead = Lead(
        name=lead_data.name,
        email=lead_data.email,
        phone=lead_data.phone,
        company=lead_data.company,
        source=lead_data.source,
        status=lead_data.status,
        assigned_to=lead_data.assigned_to,
        created_by=current_user.id
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return new_lead