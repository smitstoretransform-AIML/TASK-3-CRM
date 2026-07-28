import pytest


# ============================================================
# PERMISSION ENDPOINTS
# ============================================================

PERMISSION_ENDPOINTS = [
    (
        "/api/v1/permissions/test/create-lead",
        "create_lead",
    ),
    (
        "/api/v1/permissions/test/delete-lead",
        "delete_lead",
    ),
    (
        "/api/v1/permissions/test/view-customers",
        "view_customers",
    ),
    (
        "/api/v1/permissions/test/assign-lead",
        "assign_lead",
    ),
    (
        "/api/v1/permissions/test/manage-users",
        "manage_users",
    ),
]


# ============================================================
# TEST: PERMISSION GRANTED
# ============================================================

@pytest.mark.parametrize(
    "endpoint, permission_name",
    PERMISSION_ENDPOINTS
)
def test_permission_granted(
    client,
    auth_headers,
    endpoint,
    permission_name
):

    response = client.get(
        endpoint,
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.json()

    expected_message = (
        f"{permission_name.replace('_', ' ').title()} "
        "permission granted"
    )

    assert (
        response_data["message"]
        == expected_message
    )

    assert (
        response_data["user_id"]
        is not None
    )

    assert (
        response_data["role_id"]
        == 1
    )

    assert (
        response_data["permission"]
        == permission_name
    )


# ============================================================
# TEST: PERMISSION DENIED
# ============================================================

@pytest.mark.parametrize(
    "endpoint, permission_name",
    PERMISSION_ENDPOINTS
)
def test_permission_denied_without_required_permission(
    client,
    no_permission_headers,
    endpoint,
    permission_name
):

    response = client.get(
        endpoint,
        headers=no_permission_headers
    )

    # ========================================================
    # VERIFY FORBIDDEN STATUS
    # ========================================================

    assert response.status_code == 403


    # ========================================================
    # GET RESPONSE
    # ========================================================

    response_data = response.json()


    # ========================================================
    # VERIFY CUSTOM ERROR FORMAT
    # ========================================================

    assert response_data["code"] == 403

    assert (
        response_data["status"]
        == "error"
    )

    assert (
        response_data["message"]
        == "Permission denied"
    )


# ============================================================
# TEST: AUTHENTICATION REQUIRED
# ============================================================

@pytest.mark.parametrize(
    "endpoint, permission_name",
    PERMISSION_ENDPOINTS
)
def test_permission_requires_authentication(
    client,
    endpoint,
    permission_name
):

    response = client.get(
        endpoint
    )


    # ========================================================
    # VERIFY UNAUTHORIZED STATUS
    # ========================================================

    assert response.status_code == 401


    # ========================================================
    # GET RESPONSE
    # ========================================================

    response_data = response.json()


    # ========================================================
    # VERIFY CUSTOM ERROR FORMAT
    # ========================================================

    assert response_data["code"] == 401

    assert (
        response_data["status"]
        == "error"
    )

    assert (
        "message"
        in response_data
    )

    assert response_data["message"]