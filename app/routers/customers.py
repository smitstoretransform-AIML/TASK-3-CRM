from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.customers import Customer
from app.models.users import User
from app.schemas.customers import (
    CustomerCreate,
    CustomerListResponse,
    CustomerResponse,
    CustomerUpdate,
)


router = APIRouter(
    prefix="/api/v1/customers",
    tags=["Customers"]
)


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_customer = (
        db.query(Customer)
        .filter(
            Customer.email == customer_data.email,
            Customer.deleted_at.is_(None)
        )
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this email already exists"
        )

    new_customer = Customer(
        name=customer_data.name,
        email=customer_data.email,
        phone=customer_data.phone,
        company=customer_data.company,
        created_by=current_user.id
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@router.get(
    "/",
    response_model=CustomerListResponse
)
def list_customers(
    search: str | None = Query(
        default=None,
        description="Search by name, email, phone, or company"
    ),
    company: str | None = Query(
        default=None,
        description="Filter customers by company"
    ),
    created_by: int | None = Query(
        default=None,
        gt=0,
        description="Filter customers by creator user ID"
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
        description="Number of customers per page"
    ),
    sort_by: str = Query(
        default="created_at",
        description="Sort field: id, name, email, company, created_at, updated_at"
    ),
    sort_order: str = Query(
        default="desc",
        description="Sort order: asc or desc"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    allowed_sort_fields = {
        "id": Customer.id,
        "name": Customer.name,
        "email": Customer.email,
        "company": Customer.company,
        "created_at": Customer.created_at,
        "updated_at": Customer.updated_at,
    }

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid sort_by value. "
                "Allowed values: id, name, email, company, "
                "created_at, updated_at"
            )
        )

    sort_order = sort_order.lower()

    if sort_order not in {"asc", "desc"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="sort_order must be either 'asc' or 'desc'"
        )

    query = (
        db.query(Customer)
        .filter(Customer.deleted_at.is_(None))
    )

    if search:
        search_value = search.strip()

        if search_value:
            search_pattern = f"%{search_value}%"

            query = query.filter(
                or_(
                    Customer.name.ilike(search_pattern),
                    Customer.email.ilike(search_pattern),
                    Customer.phone.ilike(search_pattern),
                    Customer.company.ilike(search_pattern),
                )
            )

    if company:
        company_value = company.strip()

        if company_value:
            query = query.filter(
                Customer.company.ilike(
                    f"%{company_value}%"
                )
            )

    if created_by is not None:
        query = query.filter(
            Customer.created_by == created_by
        )

    total = query.with_entities(
        func.count(Customer.id)
    ).scalar()

    sort_column = allowed_sort_fields[sort_by]

    if sort_order == "asc":
        query = query.order_by(
            sort_column.asc()
        )
    else:
        query = query.order_by(
            sort_column.desc()
        )

    offset = (page - 1) * limit

    customers = (
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
        "items": customers,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    return customer


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    update_data = customer_data.model_dump(
        exclude_unset=True
    )

    if "email" in update_data:
        existing_customer = (
            db.query(Customer)
            .filter(
                Customer.email == update_data["email"],
                Customer.id != customer_id,
                Customer.deleted_at.is_(None)
            )
            .first()
        )

        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer with this email already exists"
            )

    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    return customer


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    customer.deleted_at = func.now()

    db.commit()

    return None