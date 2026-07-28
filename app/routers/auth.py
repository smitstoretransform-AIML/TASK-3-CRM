from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.responses import success_response
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.roles import Role
from app.models.users import User
from app.schemas.users import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
    UserRegisterResponse,
    UserLoginResponse,
    UserProfileResponse,
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


# =========================================================
# REGISTER
# =========================================================

@router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    role = (
        db.query(Role)
        .filter(Role.id == user_data.role_id)
        .first()
    )

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    hashed_password = hash_password(
        user_data.password
    )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        role_id=user_data.role_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return success_response(
        data=new_user,
        message="User registered successfully",
        code=status.HTTP_201_CREATED
    )


# =========================================================
# LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=UserLoginResponse
)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    password_valid = verify_password(
        user_data.password,
        user.password
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role_id": user.role_id
        },
        expires_delta=timedelta(
            minutes=30
        )
    )

    token_data = {
        "access_token": access_token,
        "token_type": "bearer"
    }

    return success_response(
        data=token_data,
        message="Login successful",
        code=status.HTTP_200_OK
    )


# =========================================================
# MY PROFILE
# =========================================================

@router.get(
    "/me",
    response_model=UserProfileResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return success_response(
        data=current_user,
        message="Profile retrieved successfully",
        code=status.HTTP_200_OK
    )
