from fastapi import APIRouter, Depends

from app.core.dependencies import require_permission
from app.models.users import User


router = APIRouter(
    prefix="/api/v1/permissions",
    tags=["Permissions"]
)


@router.get(
    "/test/create-lead",
    summary="Test Create Lead Permission"
)
def test_create_lead_permission(
    current_user: User = Depends(
        require_permission("create_lead")
    )
):
    return {
        "message": "Create Lead permission granted",
        "user_id": current_user.id,
        "role_id": current_user.role_id,
        "permission": "create_lead"
    }


@router.get(
    "/test/delete-lead",
    summary="Test Delete Lead Permission"
)
def test_delete_lead_permission(
    current_user: User = Depends(
        require_permission("delete_lead")
    )
):
    return {
        "message": "Delete Lead permission granted",
        "user_id": current_user.id,
        "role_id": current_user.role_id,
        "permission": "delete_lead"
    }


@router.get(
    "/test/view-customers",
    summary="Test View Customers Permission"
)
def test_view_customers_permission(
    current_user: User = Depends(
        require_permission("view_customers")
    )
):
    return {
        "message": "View Customers permission granted",
        "user_id": current_user.id,
        "role_id": current_user.role_id,
        "permission": "view_customers"
    }


@router.get(
    "/test/assign-lead",
    summary="Test Assign Lead Permission"
)
def test_assign_lead_permission(
    current_user: User = Depends(
        require_permission("assign_lead")
    )
):
    return {
        "message": "Assign Lead permission granted",
        "user_id": current_user.id,
        "role_id": current_user.role_id,
        "permission": "assign_lead"
    }


@router.get(
    "/test/manage-users",
    summary="Test Manage Users Permission"
)
def test_manage_users_permission(
    current_user: User = Depends(
        require_permission("manage_users")
    )
):
    return {
        "message": "Manage Users permission granted",
        "user_id": current_user.id,
        "role_id": current_user.role_id,
        "permission": "manage_users"
    }