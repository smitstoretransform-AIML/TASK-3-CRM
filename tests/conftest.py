import uuid

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

from app.models.roles import Role
from app.models.permissions import Permission
from app.models.role_permissions import RolePermission


# ============================================================
# TEST DATABASE
# ============================================================

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"


test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


# ============================================================
# CREATE TEST DATABASE TABLES
# ============================================================

Base.metadata.create_all(
    bind=test_engine
)


# ============================================================
# SEED TEST DATA
# ============================================================

def seed_test_data():

    db = TestingSessionLocal()

    try:

        # ====================================================
        # CREATE ADMIN ROLE
        # ====================================================

        admin_role = (
            db.query(Role)
            .filter(
                Role.id == 1
            )
            .first()
        )

        if not admin_role:

            admin_role = Role(
                id=1,
                name="Admin"
            )

            db.add(admin_role)
            db.flush()


        # ====================================================
        # CREATE NO-PERMISSION ROLE
        # ====================================================

        no_permission_role = (
            db.query(Role)
            .filter(
                Role.name == "Test No Permission Role"
            )
            .first()
        )

        if not no_permission_role:

            no_permission_role = Role(
                name="Test No Permission Role"
            )

            db.add(no_permission_role)
            db.flush()


        # ====================================================
        # REQUIRED PERMISSIONS
        # ====================================================

        required_permissions = [
            "view_customers",
            "create_lead",
            "assign_lead",
            "delete_lead",
            "manage_users",
        ]


        # ====================================================
        # CREATE ALL REQUIRED PERMISSIONS
        # ====================================================

        permissions = {}

        for permission_name in required_permissions:

            permission = (
                db.query(Permission)
                .filter(
                    Permission.name
                    == permission_name
                )
                .first()
            )

            if not permission:

                permission = Permission(
                    name=permission_name
                )

                db.add(permission)
                db.flush()

            permissions[
                permission_name
            ] = permission


        # ====================================================
        # ASSIGN ALL PERMISSIONS TO ADMIN
        # ====================================================

        for permission_name, permission in permissions.items():

            existing_mapping = (
                db.query(RolePermission)
                .filter(
                    RolePermission.role_id
                    == admin_role.id,

                    RolePermission.permission_id
                    == permission.id
                )
                .first()
            )

            if not existing_mapping:

                db.add(
                    RolePermission(
                        role_id=admin_role.id,
                        permission_id=permission.id
                    )
                )


        # ====================================================
        # ENSURE NO-PERMISSION ROLE HAS ZERO PERMISSIONS
        # ====================================================

        db.query(RolePermission).filter(
            RolePermission.role_id
            == no_permission_role.id
        ).delete(
            synchronize_session=False
        )


        # ====================================================
        # COMMIT TEST DATA
        # ====================================================

        db.commit()

    finally:

        db.close()


# ============================================================
# SEED TEST DATABASE
# ============================================================

seed_test_data()


# ============================================================
# OVERRIDE DATABASE DEPENDENCY
# ============================================================

def override_get_db():

    db = TestingSessionLocal()

    try:

        yield db

    finally:

        db.close()


app.dependency_overrides[
    get_db
] = override_get_db


# ============================================================
# TEST CLIENT FIXTURE
# ============================================================

@pytest.fixture
def client():

    with TestClient(app) as test_client:

        yield test_client


# ============================================================
# DATABASE SESSION FIXTURE
# ============================================================

@pytest.fixture
def db():

    session = TestingSessionLocal()

    try:

        yield session

    finally:

        session.close()


# ============================================================
# ADMIN AUTHENTICATION FIXTURE
# ============================================================

@pytest.fixture
def auth_headers(client):

    unique_email = (
        f"testadmin_{uuid.uuid4().hex}"
        "@example.com"
    )


    # ========================================================
    # REGISTER ADMIN
    # ========================================================

    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test Admin",
            "email": unique_email,
            "password": "Test@123",
            "role_id": 1
        }
    )

    assert register_response.status_code == 201


    # ========================================================
    # LOGIN ADMIN
    # ========================================================

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": unique_email,
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200


    # ========================================================
    # GET ACCESS TOKEN
    # ========================================================

    access_token = (
        login_response
        .json()["data"]["access_token"]
    )


    # ========================================================
    # RETURN AUTHORIZATION HEADER
    # ========================================================

    return {
        "Authorization": (
            f"Bearer {access_token}"
        )
    }


# ============================================================
# NO-PERMISSION USER FIXTURE
# ============================================================

@pytest.fixture
def no_permission_headers(
    client,
    db
):

    # ========================================================
    # GET NO-PERMISSION ROLE
    # ========================================================

    no_permission_role = (
        db.query(Role)
        .filter(
            Role.name
            == "Test No Permission Role"
        )
        .first()
    )

    assert no_permission_role is not None


    # ========================================================
    # DELETE ANY PERMISSIONS FOR THIS ROLE
    #
    # This guarantees that the role cannot access any
    # protected permission endpoint.
    # ========================================================

    db.query(RolePermission).filter(
        RolePermission.role_id
        == no_permission_role.id
    ).delete(
        synchronize_session=False
    )

    db.commit()


    # ========================================================
    # VERIFY ROLE HAS ZERO PERMISSIONS
    # ========================================================

    permission_count = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id
            == no_permission_role.id
        )
        .count()
    )

    assert permission_count == 0


    # ========================================================
    # CREATE UNIQUE USER EMAIL
    # ========================================================

    unique_email = (
        f"nopermission_{uuid.uuid4().hex}"
        "@example.com"
    )


    # ========================================================
    # REGISTER NO-PERMISSION USER
    # ========================================================

    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "No Permission User",
            "email": unique_email,
            "password": "Test@123",
            "role_id": no_permission_role.id
        }
    )

    assert register_response.status_code == 201


    # ========================================================
    # LOGIN NO-PERMISSION USER
    # ========================================================

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": unique_email,
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200


    # ========================================================
    # GET ACCESS TOKEN
    # ========================================================

    access_token = (
        login_response
        .json()["data"]["access_token"]
    )


    # ========================================================
    # RETURN AUTHORIZATION HEADER
    # ========================================================

    return {
        "Authorization": (
            f"Bearer {access_token}"
        )
    }