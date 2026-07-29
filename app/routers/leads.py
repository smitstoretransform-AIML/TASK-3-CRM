from datetime import datetime
from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_
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
from app.models.leads import Lead
from app.models.notifications import Notification
from app.models.users import User
from app.schemas.leads import (
    LeadCreate,
    LeadListResponse,
    LeadResponse,
    LeadUpdate,
)


router = APIRouter(
    prefix="/api/v1/leads",
    tags=["Leads"]
)


# ============================================================
# CREATE LEAD
# ============================================================

@router.post(
    "/",
    response_model=APIResponse,
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

    # ========================================================
    # VALIDATE ASSIGNED USER
    # ========================================================

    assigned_user = None

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

    # ========================================================
    # CREATE LEAD
    # ========================================================

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

    # ========================================================
    # CREATE NOTIFICATION
    # ========================================================

    if (
        lead_data.assigned_to is not None
        and assigned_user is not None
    ):
        notification = Notification(
            user_id=assigned_user.id,
            title="New Lead Assigned",
            message=(
                f"{new_lead.name} assigned to "
                f"{assigned_user.name}"
            ),
            is_read=False,
            created_at=datetime.utcnow()
        )

        db.add(notification)

    # ========================================================
    # CREATE AUDIT LOG
    # ========================================================

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="CREATE",
        module="leads",
        old_data=None,
        new_data={
            "name": new_lead.name,
            "email": new_lead.email,
            "phone": new_lead.phone,
            "company": new_lead.company,
            "source": new_lead.source,
            "status": new_lead.status,
            "assigned_to": new_lead.assigned_to,
        }
    )

    db.commit()
    db.refresh(new_lead)

    lead_response = LeadResponse.model_validate(
        new_lead,
        from_attributes=True
    )

    return success_response(
        data=lead_response.model_dump(
            mode="json"
        ),
        message="Lead created successfully",
        code=201
    )


# ============================================================
# LIST LEADS
# ============================================================

@router.get(
    "/",
    response_model=APIResponse
)
def list_leads(
    search: str | None = Query(
        default=None,
        description="Search by name, email, phone, or company"
    ),
    status_filter: str | None = Query(
        default=None,
        alias="status",
        description="Filter by lead status"
    ),
    source: str | None = Query(
        default=None,
        description="Filter by lead source"
    ),
    assigned_to: int | None = Query(
        default=None,
        gt=0,
        description="Filter by assigned user ID"
    ),
    from_date: datetime | None = Query(
        default=None,
        description="Filter leads created from this date"
    ),
    to_date: datetime | None = Query(
        default=None,
        description="Filter leads created until this date"
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
        description="Number of leads per page"
    ),
    sort_by: str = Query(
        default="created_at",
        description=(
            "Sort field: id, name, email, company, "
            "source, status, created_at, updated_at"
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
    # ALLOWED SORT FIELDS
    # ========================================================

    allowed_sort_fields = {
        "id": Lead.id,
        "name": Lead.name,
        "email": Lead.email,
        "company": Lead.company,
        "source": Lead.source,
        "status": Lead.status,
        "created_at": Lead.created_at,
        "updated_at": Lead.updated_at,
    }

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid sort_by value. "
                "Allowed values: id, name, email, company, "
                "source, status, created_at, updated_at"
            )
        )

    # ========================================================
    # VALIDATE SORT ORDER
    # ========================================================

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
    # VALIDATE DATE RANGE
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
    # BASE QUERY
    # ========================================================

    query = (
        db.query(Lead)
        .filter(
            Lead.deleted_at.is_(None)
        )
    )

    # ========================================================
    # SEARCH FILTER
    # ========================================================

    if search:

        search_value = search.strip()

        if search_value:

            search_pattern = (
                f"%{search_value}%"
            )

            query = query.filter(
                or_(
                    Lead.name.ilike(
                        search_pattern
                    ),
                    Lead.email.ilike(
                        search_pattern
                    ),
                    Lead.phone.ilike(
                        search_pattern
                    ),
                    Lead.company.ilike(
                        search_pattern
                    ),
                )
            )

    # ========================================================
    # STATUS FILTER
    # ========================================================

    if status_filter:

        status_value = (
            status_filter.strip()
        )

        if status_value:

            query = query.filter(
                Lead.status.ilike(
                    status_value
                )
            )

    # ========================================================
    # SOURCE FILTER
    # ========================================================

    if source:

        source_value = source.strip()

        if source_value:

            query = query.filter(
                Lead.source.ilike(
                    source_value
                )
            )

    # ========================================================
    # ASSIGNED USER FILTER
    # ========================================================

    if assigned_to is not None:

        query = query.filter(
            Lead.assigned_to == assigned_to
        )

    # ========================================================
    # DATE RANGE FILTER
    # ========================================================

    if from_date is not None:

        query = query.filter(
            Lead.created_at >= from_date
        )

    if to_date is not None:

        query = query.filter(
            Lead.created_at <= to_date
        )

    # ========================================================
    # COUNT TOTAL RECORDS
    # ========================================================

    total = query.with_entities(
        func.count(Lead.id)
    ).scalar()

    # ========================================================
    # SORTING
    # ========================================================

    sort_column = (
        allowed_sort_fields[sort_by]
    )

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

    leads = (
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
    # CONVERT SQLALCHEMY OBJECTS TO PYDANTIC
    # ========================================================

    lead_list = LeadListResponse(
        items=[
            LeadResponse.model_validate(
                lead,
                from_attributes=True
            )
            for lead in leads
        ],
        page=page,
        limit=limit,
        total=total,
        total_pages=total_pages,
    )

    return success_response(
        data=lead_list.model_dump(
            mode="json"
        ),
        message="Leads retrieved successfully",
        code=200
    )


# ============================================================
# GET SINGLE LEAD
# ============================================================

@router.get(
    "/{lead_id}",
    response_model=APIResponse
)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    lead_response = LeadResponse.model_validate(
        lead,
        from_attributes=True
    )

    return success_response(
        data=lead_response.model_dump(
            mode="json"
        ),
        message="Lead retrieved successfully",
        code=200
    )


# ============================================================
# UPDATE LEAD
# ============================================================

@router.put(
    "/{lead_id}",
    response_model=APIResponse
)
def update_lead(
    lead_id: int,
    lead_data: LeadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    update_data = lead_data.model_dump(
        exclude_unset=True
    )

    # ========================================================
    # PREVENT DIRECT CONVERSION
    # ========================================================

    if (
        "status" in update_data
        and update_data["status"].strip().lower()
        == "converted"
        and lead.status.strip().lower()
        != "converted"
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Lead cannot be directly marked as Converted. "
                "Use the lead conversion endpoint instead."
            )
        )

    # ========================================================
    # CHECK DUPLICATE EMAIL
    # ========================================================

    if "email" in update_data:

        existing_lead = (
            db.query(Lead)
            .filter(
                Lead.email == update_data["email"],
                Lead.id != lead_id,
                Lead.deleted_at.is_(None)
            )
            .first()
        )

        if existing_lead:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Lead with this email "
                    "already exists"
                )
            )

    # ========================================================
    # VALIDATE ASSIGNED USER
    # ========================================================

    if (
        "assigned_to" in update_data
        and update_data["assigned_to"] is not None
    ):

        assigned_user = (
            db.query(User)
            .filter(
                User.id ==
                update_data["assigned_to"]
            )
            .first()
        )

        if not assigned_user:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assigned user not found"
            )

    # ========================================================
    # CAPTURE OLD VALUES
    # ========================================================

    old_data = {}

    for field in update_data:

        old_data[field] = getattr(
            lead,
            field
        )

    # ========================================================
    # CHECK ASSIGNMENT CHANGE
    # ========================================================

    old_assigned_to = lead.assigned_to

    new_assigned_to = update_data.get(
        "assigned_to"
    )

    assignment_changed = (
        "assigned_to" in update_data
        and old_assigned_to != new_assigned_to
        and new_assigned_to is not None
    )

    # ========================================================
    # UPDATE LEAD
    # ========================================================

    for field, value in update_data.items():

        setattr(
            lead,
            field,
            value
        )

    # ========================================================
    # CAPTURE NEW VALUES
    # ========================================================

    new_data = {}

    for field in update_data:

        new_data[field] = getattr(
            lead,
            field
        )

    # ========================================================
    # CREATE ASSIGNMENT NOTIFICATION
    # ========================================================

    if assignment_changed:

        assigned_user = (
            db.query(User)
            .filter(
                User.id == new_assigned_to
            )
            .first()
        )

        if assigned_user:

            notification = Notification(
                user_id=assigned_user.id,
                title="New Lead Assigned",
                message=(
                    f"{lead.name} assigned to "
                    f"{assigned_user.name}"
                ),
                is_read=False,
                created_at=datetime.utcnow()
            )

            db.add(notification)

    # ========================================================
    # CREATE AUDIT LOG
    # ========================================================

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="UPDATE",
        module="leads",
        old_data=old_data,
        new_data=new_data
    )

    db.commit()
    db.refresh(lead)

    lead_response = LeadResponse.model_validate(
        lead,
        from_attributes=True
    )

    return success_response(
        data=lead_response.model_dump(
            mode="json"
        ),
        message="Lead updated successfully",
        code=200
    )


# ============================================================
# CONVERT LEAD TO CUSTOMER
# ============================================================

@router.post(
    "/{lead_id}/convert",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission("create_customer"))
    ]
)
def convert_lead_to_customer(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ========================================================
    # GET ACTIVE LEAD
    # ========================================================

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

    # ========================================================
    # CHECK IF LEAD IS ALREADY CONVERTED
    # ========================================================

    if lead.status.strip().lower() == "converted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lead has already been converted"
        )

    # ========================================================
    # CHECK EXISTING CUSTOMER LINKED TO LEAD
    # ========================================================

    existing_customer = (
        db.query(Customer)
        .filter(
            Customer.lead_id == lead.id,
            Customer.deleted_at.is_(None)
        )
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "This lead is already linked "
                "to an existing customer"
            )
        )

    # ========================================================
    # CHECK CUSTOMER WITH SAME EMAIL
    # ========================================================

    existing_customer_by_email = (
        db.query(Customer)
        .filter(
            Customer.email == lead.email,
            Customer.deleted_at.is_(None)
        )
        .first()
    )

    if existing_customer_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "A customer with this email already exists. "
                "This lead cannot be converted automatically."
            )
        )

    # ========================================================
    # CAPTURE OLD LEAD DATA
    # ========================================================

    old_lead_data = {
        "status": lead.status,
        "assigned_to": lead.assigned_to,
    }

    # ========================================================
    # CREATE CUSTOMER
    # ========================================================

    new_customer = Customer(
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        company=lead.company,
        lead_id=lead.id,
        created_by=current_user.id,
    )

    db.add(new_customer)

    # ========================================================
    # UPDATE LEAD STATUS
    # ========================================================

    lead.status = "Converted"

    # ========================================================
    # CREATE AUDIT LOG
    # ========================================================

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="CONVERT",
        module="leads",
        old_data=old_lead_data,
        new_data={
            "status": lead.status,
            "customer_lead_id": lead.id,
        }
    )

    # ========================================================
    # CREATE NOTIFICATION
    # ========================================================

    if lead.assigned_to is not None:

        notification = Notification(
            user_id=lead.assigned_to,
            title="Lead Converted",
            message=(
                f"Lead '{lead.name}' has been "
                f"converted into a customer"
            ),
            is_read=False,
            created_at=datetime.utcnow()
        )

        db.add(notification)

    # ========================================================
    # COMMIT TRANSACTION
    # ========================================================

    try:

        db.commit()

        db.refresh(new_customer)
        db.refresh(lead)

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Lead conversion failed. "
                "No changes were saved."
            )
        )

    # ========================================================
    # BUILD RESPONSE
    # ========================================================

    lead_response = LeadResponse.model_validate(
        lead,
        from_attributes=True
    )

    customer_data = {
        "id": new_customer.id,
        "name": new_customer.name,
        "email": new_customer.email,
        "phone": new_customer.phone,
        "company": new_customer.company,
        "lead_id": new_customer.lead_id,
        "created_by": new_customer.created_by,
        "created_at": new_customer.created_at,
        "updated_at": new_customer.updated_at,
    }

    return success_response(
        data={
            "lead": lead_response.model_dump(
                mode="json"
            ),
            "customer": customer_data,
        },
        message="Lead converted to customer successfully",
        code=201
    )


# ============================================================
# ASSIGN LEAD
# ============================================================

@router.patch(
    "/{lead_id}/assign",
    response_model=APIResponse,
    dependencies=[
        Depends(require_permission("assign_lead"))
    ]
)
def assign_lead(
    lead_id: int,
    assigned_to: int = Query(
        ...,
        gt=0,
        description="User ID to assign the lead to"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    assigned_user = (
        db.query(User)
        .filter(
            User.id == assigned_to
        )
        .first()
    )

    if not assigned_user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned user not found"
        )

    # ========================================================
    # CAPTURE PREVIOUS ASSIGNMENT
    # ========================================================

    old_assigned_to = lead.assigned_to

    # ========================================================
    # CHECK ASSIGNMENT CHANGE
    # ========================================================

    assignment_changed = (
        old_assigned_to != assigned_to
    )

    # ========================================================
    # UPDATE ASSIGNMENT
    # ========================================================

    lead.assigned_to = assigned_to

    # ========================================================
    # CREATE NOTIFICATION
    # ========================================================

    if assignment_changed:

        notification = Notification(
            user_id=assigned_user.id,
            title="New Lead Assigned",
            message=(
                f"{lead.name} assigned to "
                f"{assigned_user.name}"
            ),
            is_read=False,
            created_at=datetime.utcnow()
        )

        db.add(notification)

    # ========================================================
    #  
    # ========================================================

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="ASSIGN",
        module="leads",
        old_data={
            "assigned_to": old_assigned_to
        },
        new_data={
            "assigned_to": assigned_to
        }
    )

    db.commit()
    db.refresh(lead)

    lead_response = LeadResponse.model_validate(
        lead,
        from_attributes=True
    )

    return success_response(
        data=lead_response.model_dump(
            mode="json"
        ),
        message="Lead assigned successfully",
        code=200
    )



# ============================================================
# CONVERT LEAD TO CUSTOMER
# ============================================================

@router.post(
    "/{lead_id}/convert",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED
)
def convert_lead_to_customer(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ========================================================
    # GET LEAD
    # ========================================================

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

    # ========================================================
    # CHECK LEAD STATUS
    # ========================================================

    if lead.status.lower() == "converted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lead has already been converted to a customer"
        )

    # ========================================================
    # CHECK WHETHER CUSTOMER ALREADY EXISTS
    # ========================================================

    existing_customer = (
        db.query(Customer)
        .filter(
            Customer.lead_id == lead.id,
            Customer.deleted_at.is_(None)
        )
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer already exists for this lead"
        )

    # ========================================================
    # CHECK DUPLICATE CUSTOMER EMAIL
    # ========================================================

    existing_customer_by_email = (
        db.query(Customer)
        .filter(
            Customer.email == lead.email,
            Customer.deleted_at.is_(None)
        )
        .first()
    )

    if existing_customer_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "A customer with this email already exists"
            )
        )

    # ========================================================
    # CREATE CUSTOMER
    # ========================================================

    new_customer = Customer(
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        company=lead.company,
        lead_id=lead.id,
        created_by=current_user.id
    )

    db.add(new_customer)

    # Flush so customer.id is generated before audit/response
    db.flush()

    # ========================================================
    # UPDATE LEAD STATUS
    # ========================================================

    old_status = lead.status

    lead.status = "Converted"

    # ========================================================
    # CREATE AUDIT LOG
    # ========================================================

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="CONVERT",
        module="leads",
        old_data={
            "lead_id": lead.id,
            "status": old_status
        },
        new_data={
            "lead_id": lead.id,
            "status": "Converted",
            "customer_id": new_customer.id
        }
    )

    # ========================================================
    # CREATE NOTIFICATION
    # ========================================================

    if lead.assigned_to is not None:

        notification = Notification(
            user_id=lead.assigned_to,
            title="Lead Converted",
            message=(
                f"Lead '{lead.name}' has been converted "
                f"to customer '{new_customer.name}'"
            ),
            is_read=False,
            created_at=datetime.utcnow()
        )

        db.add(notification)

    # ========================================================
    # COMMIT TRANSACTION
    # ========================================================

    db.commit()

    db.refresh(new_customer)
    db.refresh(lead)

    # ========================================================
    # RESPONSE
    # ========================================================

    return success_response(
        data={
            "lead": {
                "id": lead.id,
                "status": lead.status
            },
            "customer": {
                "id": new_customer.id,
                "lead_id": new_customer.lead_id,
                "name": new_customer.name,
                "email": new_customer.email,
                "phone": new_customer.phone,
                "company": new_customer.company
            }
        },
        message="Lead converted to customer successfully",
        code=status.HTTP_201_CREATED
    )

# ============================================================
# DELETE LEAD - SOFT DELETE
# ============================================================

@router.delete(
    "/{lead_id}",
    response_model=APIResponse,
    dependencies=[
        Depends(require_permission("delete_lead"))
    ]
)
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    # ========================================================
    # PREVENT DELETING CONVERTED LEAD
    # ========================================================

    if lead.status.strip().lower() == "converted":

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Converted leads cannot be deleted. "
                "Manage the associated customer instead."
            )
        )

    # ========================================================
    # CAPTURE LEAD DATA BEFORE SOFT DELETE
    # ========================================================

    old_data = {
        "name": lead.name,
        "email": lead.email,
        "phone": lead.phone,
        "company": lead.company,
        "source": lead.source,
        "status": lead.status,
        "assigned_to": lead.assigned_to,
        "created_by": lead.created_by,
    }

    # ========================================================
    # SOFT DELETE
    # ========================================================

    lead.deleted_at = func.now()

    # ========================================================
    # CREATE AUDIT LOG
    # ========================================================

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="DELETE",
        module="leads",
        old_data=old_data,
        new_data=None
    )

    db.commit()

    return success_response(
        data=None,
        message="Lead deleted successfully",
        code=200
    )