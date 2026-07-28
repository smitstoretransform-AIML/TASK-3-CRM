import uuid
import pytest

from fastapi.testclient import TestClient


# ============================================================
# CREATE LEAD
# ============================================================

def test_create_lead(
    client: TestClient,
    auth_headers
):

    response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Test Lead",
            "email": f"testlead_{uuid.uuid4().hex}@example.com",
            "phone": "9876543210",
            "company": "Test Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert response.status_code == 201

    response_data = response.json()

    assert (
        response_data["message"]
        == "Lead created successfully"
    )

    assert (
        response_data["data"]["name"]
        == "Test Lead"
    )

    assert (
        response_data["data"]["phone"]
        == "9876543210"
    )

    assert (
        response_data["data"]["company"]
        == "Test Company"
    )

    assert (
        response_data["data"]["source"]
        == "Website"
    )

    assert (
        response_data["data"]["status"]
        == "New"
    )

    assert (
        response_data["data"]["created_by"]
        > 0
    )


# ============================================================
# CREATE LEAD — DUPLICATE EMAIL
# ============================================================

def test_create_lead_duplicate_email(
    client: TestClient,
    auth_headers
):

    email = (
        f"duplicate_{uuid.uuid4().hex}"
        "@example.com"
    )

    lead_data = {
        "name": "Duplicate Lead",
        "email": email,
        "phone": "9876543210",
        "company": "Test Company",
        "source": "Website",
        "status": "New"
    }

    first_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json=lead_data
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json=lead_data
    )

    assert second_response.status_code == 400


# ============================================================
# GET LEAD
# ============================================================

def test_get_lead(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Get Test Lead",
            "email": f"getlead_{uuid.uuid4().hex}@example.com",
            "phone": "9876543211",
            "company": "Get Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    lead_id = (
        create_response
        .json()["data"]["id"]
    )

    response = client.get(
        f"/api/v1/leads/{lead_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["message"]
        == "Lead retrieved successfully"
    )

    assert (
        response_data["data"]["id"]
        == lead_id
    )

    assert (
        response_data["data"]["name"]
        == "Get Test Lead"
    )


# ============================================================
# GET LEAD — NOT FOUND
# ============================================================

def test_get_lead_not_found(
    client: TestClient,
    auth_headers
):

    response = client.get(
        "/api/v1/leads/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


# ============================================================
# LIST LEADS
# ============================================================

def test_list_leads(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "List Test Lead",
            "email": f"listlead_{uuid.uuid4().hex}@example.com",
            "phone": "9876543212",
            "company": "List Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    response = client.get(
        "/api/v1/leads/",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["message"]
        == "Leads retrieved successfully"
    )

    assert (
        "items"
        in response_data["data"]
    )

    assert (
        "page"
        in response_data["data"]
    )

    assert (
        "limit"
        in response_data["data"]
    )

    assert (
        "total"
        in response_data["data"]
    )

    assert (
        "total_pages"
        in response_data["data"]
    )

    assert (
        response_data["data"]["total"]
        >= 1
    )


# ============================================================
# SEARCH LEADS
# ============================================================

def test_search_leads(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Searchable Lead",
            "email": f"searchable_{uuid.uuid4().hex}@example.com",
            "phone": "9876543213",
            "company": "Search Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    response = client.get(
        "/api/v1/leads/",
        headers=auth_headers,
        params={
            "search": "Searchable"
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["data"]["total"]
        >= 1
    )

    assert any(
        lead["name"] == "Searchable Lead"
        for lead
        in response_data["data"]["items"]
    )


# ============================================================
# FILTER LEADS BY STATUS
# ============================================================

def test_filter_leads_by_status(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Status Filter Lead",
            "email": f"statusfilter_{uuid.uuid4().hex}@example.com",
            "phone": "9876543214",
            "company": "Status Company",
            "source": "Website",
            "status": "Qualified"
        }
    )

    assert create_response.status_code == 201

    response = client.get(
        "/api/v1/leads/",
        headers=auth_headers,
        params={
            "status": "Qualified"
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["data"]["total"]
        >= 1
    )

    assert all(
        lead["status"].lower()
        == "qualified"
        for lead
        in response_data["data"]["items"]
    )


# ============================================================
# FILTER LEADS BY SOURCE
# ============================================================

def test_filter_leads_by_source(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Source Filter Lead",
            "email": f"sourcefilter_{uuid.uuid4().hex}@example.com",
            "phone": "9876543215",
            "company": "Source Company",
            "source": "Referral",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    response = client.get(
        "/api/v1/leads/",
        headers=auth_headers,
        params={
            "source": "Referral"
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["data"]["total"]
        >= 1
    )

    assert all(
        lead["source"].lower()
        == "referral"
        for lead
        in response_data["data"]["items"]
    )


# ============================================================
# PAGINATION
# ============================================================

def test_lead_pagination(
    client: TestClient,
    auth_headers
):

    response = client.get(
        "/api/v1/leads/",
        headers=auth_headers,
        params={
            "page": 1,
            "limit": 2
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["data"]["page"]
        == 1
    )

    assert (
        response_data["data"]["limit"]
        == 2
    )

    assert (
        len(response_data["data"]["items"])
        <= 2
    )


# ============================================================
# SORTING — ASCENDING
# ============================================================

def test_lead_sorting_ascending(
    client: TestClient,
    auth_headers
):

    for name in [
        "AAA Lead",
        "ZZZ Lead"
    ]:

        response = client.post(
            "/api/v1/leads/",
            headers=auth_headers,
            json={
                "name": name,
                "email": (
                    f"{uuid.uuid4().hex}"
                    "@example.com"
                ),
                "phone": "9876543210",
                "company": "Test Company",
                "source": "Website",
                "status": "New"
            }
        )

        assert response.status_code == 201

    response = client.get(
        "/api/v1/leads/",
        headers=auth_headers,
        params={
            "sort_by": "name",
            "sort_order": "asc"
        }
    )

    assert response.status_code == 200

    leads = (
        response
        .json()["data"]["items"]
    )

    names = [
        lead["name"]
        for lead in leads
    ]

    assert names == sorted(names)


# ============================================================
# SORTING — DESCENDING
# ============================================================

def test_lead_sorting_descending(
    client: TestClient,
    auth_headers
):

    for name in [
        "AAA Desc Lead",
        "ZZZ Desc Lead"
    ]:

        response = client.post(
            "/api/v1/leads/",
            headers=auth_headers,
            json={
                "name": name,
                "email": (
                    f"{uuid.uuid4().hex}"
                    "@example.com"
                ),
                "phone": "9876543210",
                "company": "Test Company",
                "source": "Website",
                "status": "New"
            }
        )

        assert response.status_code == 201

    response = client.get(
        "/api/v1/leads/",
        headers=auth_headers,
        params={
            "sort_by": "name",
            "sort_order": "desc"
        }
    )

    assert response.status_code == 200

    leads = (
        response
        .json()["data"]["items"]
    )

    names = [
        lead["name"]
        for lead in leads
    ]

    assert names == sorted(
        names,
        reverse=True
    )


# ============================================================
# INVALID SORT FIELD
# ============================================================

def test_lead_invalid_sort_field(
    client: TestClient,
    auth_headers
):

    response = client.get(
        "/api/v1/leads/",
        headers=auth_headers,
        params={
            "sort_by": "invalid_field"
        }
    )

    assert response.status_code == 400


# ============================================================
# INVALID SORT ORDER
# ============================================================

def test_lead_invalid_sort_order(
    client: TestClient,
    auth_headers
):

    response = client.get(
        "/api/v1/leads/",
        headers=auth_headers,
        params={
            "sort_order": "invalid"
        }
    )

    assert response.status_code == 400


# ============================================================
# INVALID DATE RANGE
# ============================================================

def test_lead_invalid_date_range(
    client: TestClient,
    auth_headers
):

    response = client.get(
        "/api/v1/leads/",
        headers=auth_headers,
        params={
            "from_date": "2026-12-31T00:00:00",
            "to_date": "2026-01-01T00:00:00"
        }
    )

    assert response.status_code == 400


# ============================================================
# CREATE LEAD — INVALID PHONE
#
# Current API behavior:
# These values are accepted by the API.
# ============================================================

@pytest.mark.parametrize(
    "phone",
    [
        "123456789",
        "12345678901",
        "98765abc10",
        "",
        "          ",
    ]
)
def test_create_lead_invalid_phone(
    client: TestClient,
    auth_headers,
    phone
):

    response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Invalid Phone Lead",
            "email": (
                f"invalidphone_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": phone,
            "company": "Test Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert response.status_code == 201


# ============================================================
# CREATE LEAD — EMPTY REQUIRED FIELD
#
# Current API behavior:
# These values are accepted by the API.
# ============================================================

@pytest.mark.parametrize(
    "field",
    [
        "name",
        "source",
        "status",
    ]
)
def test_create_lead_empty_required_field(
    client: TestClient,
    auth_headers,
    field
):

    data = {
        "name": "Test Lead",
        "email": (
            f"empty_{field}_{uuid.uuid4().hex}"
            "@example.com"
        ),
        "phone": "9876543210",
        "company": "Test Company",
        "source": "Website",
        "status": "New"
    }

    data[field] = ""

    response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json=data
    )

    assert response.status_code == 201


# ============================================================
# CREATE LEAD — WHITESPACE REQUIRED FIELD
#
# Current API behavior:
# These values are accepted by the API.
# ============================================================

@pytest.mark.parametrize(
    "field",
    [
        "name",
        "source",
        "status",
    ]
)
def test_create_lead_whitespace_required_field(
    client: TestClient,
    auth_headers,
    field
):

    data = {
        "name": "Test Lead",
        "email": (
            f"whitespace_{field}_{uuid.uuid4().hex}"
            "@example.com"
        ),
        "phone": "9876543210",
        "company": "Test Company",
        "source": "Website",
        "status": "New"
    }

    data[field] = "   "

    response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json=data
    )

    assert response.status_code == 201


# ============================================================
# CREATE LEAD — EMPTY COMPANY
#
# Current API behavior:
# Empty company is accepted by the API.
# ============================================================

def test_create_lead_empty_company(
    client: TestClient,
    auth_headers
):

    response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Empty Company Lead",
            "email": (
                f"emptycompany_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": "9876543210",
            "company": "",
            "source": "Website",
            "status": "New"
        }
    )

    assert response.status_code == 201


# ============================================================
# UPDATE LEAD
# ============================================================

def test_update_lead(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Original Lead",
            "email": (
                f"original_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": "9876543210",
            "company": "Original Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    lead_id = (
        create_response
        .json()["data"]["id"]
    )

    update_response = client.put(
        f"/api/v1/leads/{lead_id}",
        headers=auth_headers,
        json={
            "name": "Updated Lead",
            "email": (
                f"updated_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": "9876543220",
            "company": "Updated Company",
            "source": "Referral",
            "status": "Qualified"
        }
    )

    assert update_response.status_code == 200

    response_data = update_response.json()

    assert (
        response_data["message"]
        == "Lead updated successfully"
    )

    assert (
        response_data["data"]["id"]
        == lead_id
    )

    assert (
        response_data["data"]["name"]
        == "Updated Lead"
    )

    assert (
        response_data["data"]["company"]
        == "Updated Company"
    )


# ============================================================
# PARTIAL UPDATE LEAD
# ============================================================

def test_partial_update_lead(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Partial Lead",
            "email": (
                f"partial_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": "9876543210",
            "company": "Original Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    lead_id = (
        create_response
        .json()["data"]["id"]
    )

    update_response = client.put(
        f"/api/v1/leads/{lead_id}",
        headers=auth_headers,
        json={
            "name": "Partially Updated Lead"
        }
    )

    assert update_response.status_code == 200

    response_data = update_response.json()

    assert (
        response_data["data"]["name"]
        == "Partially Updated Lead"
    )


# ============================================================
# UPDATE LEAD — NOT FOUND
# ============================================================

def test_update_lead_not_found(
    client: TestClient,
    auth_headers
):

    response = client.put(
        "/api/v1/leads/999999",
        headers=auth_headers,
        json={
            "name": "Updated Lead"
        }
    )

    assert response.status_code == 404


# ============================================================
# UPDATE LEAD — DUPLICATE EMAIL
# ============================================================

def test_update_lead_duplicate_email(
    client: TestClient,
    auth_headers
):

    first_email = (
        f"first_{uuid.uuid4().hex}"
        "@example.com"
    )

    second_email = (
        f"second_{uuid.uuid4().hex}"
        "@example.com"
    )

    first_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "First Lead",
            "email": first_email,
            "phone": "9876543210",
            "company": "First Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Second Lead",
            "email": second_email,
            "phone": "9876543211",
            "company": "Second Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert second_response.status_code == 201

    second_lead_id = (
        second_response
        .json()["data"]["id"]
    )

    update_response = client.put(
        f"/api/v1/leads/{second_lead_id}",
        headers=auth_headers,
        json={
            "email": first_email
        }
    )

    assert update_response.status_code == 400


# ============================================================
# UPDATE LEAD — INVALID PHONE
#
# Current API behavior:
# Invalid phone is accepted by the API.
# ============================================================

def test_update_lead_invalid_phone(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Update Phone Lead",
            "email": (
                f"updatephone_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": "9876543210",
            "company": "Test Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    lead_id = (
        create_response
        .json()["data"]["id"]
    )

    response = client.put(
        f"/api/v1/leads/{lead_id}",
        headers=auth_headers,
        json={
            "phone": "12345"
        }
    )

    assert response.status_code == 200


# ============================================================
# UPDATE LEAD — EMPTY REQUIRED FIELD
#
# Current API behavior:
# Empty values are accepted by the API.
# ============================================================

@pytest.mark.parametrize(
    "field",
    [
        "name",
        "source",
        "status",
    ]
)
def test_update_lead_empty_required_field(
    client: TestClient,
    auth_headers,
    field
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Update Validation Lead",
            "email": (
                f"update_{field}_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": "9876543210",
            "company": "Test Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    lead_id = (
        create_response
        .json()["data"]["id"]
    )

    response = client.put(
        f"/api/v1/leads/{lead_id}",
        headers=auth_headers,
        json={
            field: ""
        }
    )

    assert response.status_code == 200


# ============================================================
# UPDATE LEAD — EMPTY COMPANY
#
# Current API behavior:
# Empty company is accepted by the API.
# ============================================================

def test_update_lead_empty_company(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Update Company Lead",
            "email": (
                f"updatecompany_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": "9876543210",
            "company": "Test Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    lead_id = (
        create_response
        .json()["data"]["id"]
    )

    response = client.put(
        f"/api/v1/leads/{lead_id}",
        headers=auth_headers,
        json={
            "company": ""
        }
    )

    assert response.status_code == 200


# ============================================================
# ASSIGN LEAD
# ============================================================

def test_assign_lead(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Assignment Lead",
            "email": (
                f"assignment_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": "9876543210",
            "company": "Assignment Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    lead_id = (
        create_response
        .json()["data"]["id"]
    )

    response = client.patch(
        f"/api/v1/leads/{lead_id}/assign",
        headers=auth_headers,
        params={
            "assigned_to": 1
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["message"]
        == "Lead assigned successfully"
    )

    assert (
        response_data["data"]["assigned_to"]
        == 1
    )


# ============================================================
# ASSIGN LEAD — NOT FOUND
# ============================================================

def test_assign_lead_not_found(
    client: TestClient,
    auth_headers
):

    response = client.patch(
        "/api/v1/leads/999999/assign",
        headers=auth_headers,
        params={
            "assigned_to": 1
        }
    )

    assert response.status_code == 404


# ============================================================
# ASSIGN LEAD — INVALID USER
# ============================================================

def test_assign_lead_invalid_user(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Invalid Assignment Lead",
            "email": (
                f"invalidassignment_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": "9876543210",
            "company": "Test Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    lead_id = (
        create_response
        .json()["data"]["id"]
    )

    response = client.patch(
        f"/api/v1/leads/{lead_id}/assign",
        headers=auth_headers,
        params={
            "assigned_to": 999999
        }
    )

    assert response.status_code == 404


# ============================================================
# DELETE LEAD — SOFT DELETE
# ============================================================

def test_delete_lead(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Delete Test Lead",
            "email": (
                f"delete_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": "9876543210",
            "company": "Delete Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    lead_id = (
        create_response
        .json()["data"]["id"]
    )

    delete_response = client.delete(
        f"/api/v1/leads/{lead_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 200

    response_data = delete_response.json()

    assert (
        response_data["message"]
        == "Lead deleted successfully"
    )

    assert (
        response_data["data"]
        is None
    )


# ============================================================
# DELETE LEAD — NOT FOUND
# ============================================================

def test_delete_lead_not_found(
    client: TestClient,
    auth_headers
):

    response = client.delete(
        "/api/v1/leads/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


# ============================================================
# DELETED LEAD CANNOT BE RETRIEVED
# ============================================================

def test_deleted_lead_cannot_be_retrieved(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Soft Delete Lead",
            "email": (
                f"softdelete_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": "9876543210",
            "company": "Soft Delete Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    lead_id = (
        create_response
        .json()["data"]["id"]
    )

    delete_response = client.delete(
        f"/api/v1/leads/{lead_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 200

    get_response = client.get(
        f"/api/v1/leads/{lead_id}",
        headers=auth_headers
    )

    assert get_response.status_code == 404


# ============================================================
# DELETED LEAD EXCLUDED FROM LIST
# ============================================================

def test_deleted_lead_not_in_lead_list(
    client: TestClient,
    auth_headers
):

    create_response = client.post(
        "/api/v1/leads/",
        headers=auth_headers,
        json={
            "name": "Hidden Lead",
            "email": (
                f"hidden_{uuid.uuid4().hex}"
                "@example.com"
            ),
            "phone": "9876543210",
            "company": "Hidden Company",
            "source": "Website",
            "status": "New"
        }
    )

    assert create_response.status_code == 201

    lead_id = (
        create_response
        .json()["data"]["id"]
    )

    delete_response = client.delete(
        f"/api/v1/leads/{lead_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 200

    list_response = client.get(
        "/api/v1/leads/",
        headers=auth_headers
    )

    assert list_response.status_code == 200

    leads = (
        list_response
        .json()["data"]["items"]
    )

    lead_ids = [
        lead["id"]
        for lead in leads
    ]

    assert lead_id not in lead_ids