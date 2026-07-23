from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.customers import Customer
from app.models.users import User
from app.schemas.customers import (
    CustomerCreate,
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
    response_model=list[CustomerResponse]
)
def list_customers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    customers = (
        db.query(Customer)
        .filter(Customer.deleted_at.is_(None))
        .order_by(Customer.created_at.desc())
        .all()
    )

    return customers


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