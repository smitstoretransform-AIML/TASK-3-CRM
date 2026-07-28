from fastapi.testclient import TestClient


# ============================================================
# REGISTER USER
# ============================================================

def test_register_user(client: TestClient):

    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test Admin",
            "email": "testadmin@example.com",
            "password": "Test@123",
            "role_id": 1
        }
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["message"] == "User registered successfully"
    assert response_data["data"]["name"] == "Test Admin"
    assert response_data["data"]["email"] == "testadmin@example.com"
    assert response_data["data"]["role_id"] == 1

    # Password should never be returned
    assert "password" not in response_data["data"]


# ============================================================
# LOGIN USER
# ============================================================

def test_login_user(client: TestClient):

    # First register the user
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Login Test User",
            "email": "logintest@example.com",
            "password": "Test@123",
            "role_id": 1
        }
    )

    assert register_response.status_code == 201

    # Then login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "logintest@example.com",
            "password": "Test@123"
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["message"] == "Login successful"

    assert "access_token" in response_data["data"]
    assert response_data["data"]["token_type"] == "bearer"

    assert response_data["data"]["access_token"]


# ============================================================
# REGISTER WITH DUPLICATE EMAIL
# ============================================================

def test_register_duplicate_email(client: TestClient):

    user_data = {
        "name": "Duplicate User",
        "email": "duplicate@example.com",
        "password": "Test@123",
        "role_id": 1
    }

    first_response = client.post(
        "/api/v1/auth/register",
        json=user_data
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/auth/register",
        json=user_data
    )

    print("DUPLICATE EMAIL RESPONSE:")
    print(second_response.json())

    assert second_response.status_code == 400


# ============================================================
# REGISTER WITH INVALID ROLE
# ============================================================

def test_register_invalid_role(client: TestClient):

    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Invalid Role User",
            "email": "invalidrole@example.com",
            "password": "Test@123",
            "role_id": 999999
        }
    )

    print("INVALID ROLE RESPONSE:")
    print(response.json())

    assert response.status_code == 404


# ============================================================
# LOGIN WITH WRONG EMAIL
# ============================================================

def test_login_invalid_email(client: TestClient):

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "Test@123"
        }
    )

    print("INVALID EMAIL LOGIN RESPONSE:")
    print(response.json())

    assert response.status_code == 401


# ============================================================
# LOGIN WITH WRONG PASSWORD
# ============================================================

def test_login_invalid_password(client: TestClient):

    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Wrong Password User",
            "email": "wrongpassword@example.com",
            "password": "Correct@123",
            "role_id": 1
        }
    )

    assert register_response.status_code == 201

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrongpassword@example.com",
            "password": "Wrong@123"
        }
    )

    print("INVALID PASSWORD RESPONSE:")
    print(response.json())

    assert response.status_code == 401



# ============================================================
# GET MY PROFILE
# ============================================================

def test_get_my_profile(client: TestClient):

    # Register user
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Profile Test User",
            "email": "profiletest@example.com",
            "password": "Test@123",
            "role_id": 1
        }
    )

    assert register_response.status_code == 201

    # Login user
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "profiletest@example.com",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    access_token = (
        login_response.json()["data"]["access_token"]
    )

    # Request profile
    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["message"] == "Profile retrieved successfully"

    assert response_data["data"]["name"] == "Profile Test User"
    assert response_data["data"]["email"] == "profiletest@example.com"
    assert response_data["data"]["role_id"] == 1

    # Password must never be returned
    assert "password" not in response_data["data"]