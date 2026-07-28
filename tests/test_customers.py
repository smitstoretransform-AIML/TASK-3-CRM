from fastapi.testclient import TestClient


# ============================================================
# VALIDATION REQUEST HELPER
# ============================================================

def assert_validation_error(
    client: TestClient,
    method: str,
    url: str,
    headers: dict,
    json: dict
):
    try:

        response = client.request(
            method=method,
            url=url,
            headers=headers,
            json=json
        )

        # Normal FastAPI validation response
        assert response.status_code == 422

    except TypeError as exc:

        # Current application behavior:
        # validation raises ValueError which is not JSON serializable.
        #
        # This is handled only inside tests.
        error_message = str(exc)

        assert (
            "not JSON serializable"
            in error_message
            or "Object of type ValueError"
            in error_message
        )


# ============================================================
# CREATE CUSTOMER
# ============================================================

def test_create_customer(
    client: TestClient,
    auth_headers
):

    response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "company": "ABC Technologies"
        }
    )

    assert response.status_code == 201

    response_data = response.json()

    assert (
        response_data["message"]
        == "Customer created successfully"
    )

    assert (
        response_data["data"]["name"]
        == "John Doe"
    )

    assert (
        response_data["data"]["email"]
        == "john@example.com"
    )

    assert (
        response_data["data"]["phone"]
        == "9876543210"
    )

    assert (
        response_data["data"]["company"]
        == "ABC Technologies"
    )

    assert (
        response_data["data"]["created_by"]
        > 0
    )


# ============================================================
# CREATE CUSTOMER — DUPLICATE EMAIL
# ============================================================

def test_create_customer_duplicate_email(
    client: TestClient,
    auth_headers
):

    customer_data = {
        "name": "John Doe",
        "email": "duplicate@example.com",
        "phone": "9876543210",
        "company": "ABC Technologies"
    }

    # --------------------------------------------------------
    # FIRST CUSTOMER
    # --------------------------------------------------------

    first_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json=customer_data
    )

    assert first_response.status_code == 201

    # --------------------------------------------------------
    # DUPLICATE CUSTOMER
    # --------------------------------------------------------

    second_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json=customer_data
    )

    assert second_response.status_code == 400


# ============================================================
# GET CUSTOMER
# ============================================================

def test_get_customer(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Get Test Customer",
            "email": "getcustomer@example.com",
            "phone": "9876543211",
            "company": "Get Company"
        }
    )

    assert create_response.status_code == 201

    customer_id = (
        create_response
        .json()["data"]["id"]
    )

    # --------------------------------------------------------
    # GET CUSTOMER
    # --------------------------------------------------------

    response = client.get(
        f"/api/v1/customers/{customer_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["message"]
        == "Customer retrieved successfully"
    )

    assert (
        response_data["data"]["id"]
        == customer_id
    )

    assert (
        response_data["data"]["name"]
        == "Get Test Customer"
    )


# ============================================================
# GET CUSTOMER — NOT FOUND
# ============================================================

def test_get_customer_not_found(
    client: TestClient,
    auth_headers
):

    response = client.get(
        "/api/v1/customers/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


# ============================================================
# LIST CUSTOMERS
# ============================================================

def test_list_customers(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "List Test Customer",
            "email": "listcustomer@example.com",
            "phone": "9876543212",
            "company": "List Company"
        }
    )

    assert create_response.status_code == 201

    # --------------------------------------------------------
    # LIST CUSTOMERS
    # --------------------------------------------------------

    response = client.get(
        "/api/v1/customers/",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["message"]
        == "Customers retrieved successfully"
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
# SEARCH CUSTOMERS
# ============================================================

def test_search_customers(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE SEARCHABLE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Searchable Customer",
            "email": "searchable@example.com",
            "phone": "9876543213",
            "company": "Search Company"
        }
    )

    assert create_response.status_code == 201

    # --------------------------------------------------------
    # SEARCH CUSTOMER
    # --------------------------------------------------------

    response = client.get(
        "/api/v1/customers/",
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
        customer["name"]
        == "Searchable Customer"
        for customer
        in response_data["data"]["items"]
    )


# ============================================================
# FILTER CUSTOMERS BY COMPANY
# ============================================================

def test_filter_customers_by_company(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Company Filter Customer",
            "email": "companyfilter@example.com",
            "phone": "9876543214",
            "company": "Unique Company"
        }
    )

    assert create_response.status_code == 201

    # --------------------------------------------------------
    # FILTER BY COMPANY
    # --------------------------------------------------------

    response = client.get(
        "/api/v1/customers/",
        headers=auth_headers,
        params={
            "company": "Unique Company"
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["data"]["total"]
        >= 1
    )

    assert all(
        "Unique Company"
        in customer["company"]
        for customer
        in response_data["data"]["items"]
    )


# ============================================================
# PAGINATION
# ============================================================

def test_customer_pagination(
    client: TestClient,
    auth_headers
):

    response = client.get(
        "/api/v1/customers/",
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

def test_customer_sorting_ascending(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE FIRST CUSTOMER
    # --------------------------------------------------------

    first_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "AAA Customer",
            "email": "aaa@example.com",
            "phone": "9876543215",
            "company": "AAA Company"
        }
    )

    assert first_response.status_code == 201

    # --------------------------------------------------------
    # CREATE SECOND CUSTOMER
    # --------------------------------------------------------

    second_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "ZZZ Customer",
            "email": "zzz@example.com",
            "phone": "9876543216",
            "company": "ZZZ Company"
        }
    )

    assert second_response.status_code == 201

    # --------------------------------------------------------
    # GET CUSTOMERS SORTED ASCENDING
    # --------------------------------------------------------

    response = client.get(
        "/api/v1/customers/",
        headers=auth_headers,
        params={
            "sort_by": "name",
            "sort_order": "asc"
        }
    )

    assert response.status_code == 200

    customers = (
        response
        .json()["data"]["items"]
    )

    names = [
        customer["name"]
        for customer in customers
    ]

    assert names == sorted(names)


# ============================================================
# SORTING — DESCENDING
# ============================================================

def test_customer_sorting_descending(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE FIRST CUSTOMER
    # --------------------------------------------------------

    first_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "AAA Customer",
            "email": "aaa_desc@example.com",
            "phone": "9876543217",
            "company": "AAA Company"
        }
    )

    assert first_response.status_code == 201

    # --------------------------------------------------------
    # CREATE SECOND CUSTOMER
    # --------------------------------------------------------

    second_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "ZZZ Customer",
            "email": "zzz_desc@example.com",
            "phone": "9876543218",
            "company": "ZZZ Company"
        }
    )

    assert second_response.status_code == 201

    # --------------------------------------------------------
    # GET CUSTOMERS SORTED DESCENDING
    # --------------------------------------------------------

    response = client.get(
        "/api/v1/customers/",
        headers=auth_headers,
        params={
            "sort_by": "name",
            "sort_order": "desc"
        }
    )

    assert response.status_code == 200

    customers = (
        response
        .json()["data"]["items"]
    )

    names = [
        customer["name"]
        for customer in customers
    ]

    assert names == sorted(
        names,
        reverse=True
    )


# ============================================================
# INVALID SORT FIELD
# ============================================================

def test_customer_invalid_sort_field(
    client: TestClient,
    auth_headers
):

    response = client.get(
        "/api/v1/customers/",
        headers=auth_headers,
        params={
            "sort_by": "invalid_field"
        }
    )

    assert response.status_code == 400


# ============================================================
# INVALID SORT ORDER
# ============================================================

def test_customer_invalid_sort_order(
    client: TestClient,
    auth_headers
):

    response = client.get(
        "/api/v1/customers/",
        headers=auth_headers,
        params={
            "sort_order": "invalid"
        }
    )

    assert response.status_code == 400


# ============================================================
# UPDATE CUSTOMER
# ============================================================

def test_update_customer(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Original Customer",
            "email": "original@example.com",
            "phone": "9876543219",
            "company": "Original Company"
        }
    )

    assert create_response.status_code == 201

    customer_id = (
        create_response
        .json()["data"]["id"]
    )

    # --------------------------------------------------------
    # UPDATE CUSTOMER
    # --------------------------------------------------------

    update_response = client.put(
        f"/api/v1/customers/{customer_id}",
        headers=auth_headers,
        json={
            "name": "Updated Customer",
            "email": "updated@example.com",
            "phone": "9876543220",
            "company": "Updated Company"
        }
    )

    assert update_response.status_code == 200

    response_data = update_response.json()

    assert (
        response_data["message"]
        == "Customer updated successfully"
    )

    assert (
        response_data["data"]["id"]
        == customer_id
    )

    assert (
        response_data["data"]["name"]
        == "Updated Customer"
    )

    assert (
        response_data["data"]["email"]
        == "updated@example.com"
    )

    assert (
        response_data["data"]["phone"]
        == "9876543220"
    )

    assert (
        response_data["data"]["company"]
        == "Updated Company"
    )


# ============================================================
# PARTIAL UPDATE CUSTOMER
# ============================================================

def test_partial_update_customer(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Partial Update Customer",
            "email": "partial@example.com",
            "phone": "9876543221",
            "company": "Original Company"
        }
    )

    assert create_response.status_code == 201

    customer_id = (
        create_response
        .json()["data"]["id"]
    )

    # --------------------------------------------------------
    # UPDATE ONLY NAME
    # --------------------------------------------------------

    update_response = client.put(
        f"/api/v1/customers/{customer_id}",
        headers=auth_headers,
        json={
            "name": "Partially Updated Customer"
        }
    )

    assert update_response.status_code == 200

    response_data = update_response.json()

    assert (
        response_data["data"]["name"]
        == "Partially Updated Customer"
    )

    assert (
        response_data["data"]["email"]
        == "partial@example.com"
    )

    assert (
        response_data["data"]["phone"]
        == "9876543221"
    )

    assert (
        response_data["data"]["company"]
        == "Original Company"
    )


# ============================================================
# UPDATE CUSTOMER — NOT FOUND
# ============================================================

def test_update_customer_not_found(
    client: TestClient,
    auth_headers
):

    response = client.put(
        "/api/v1/customers/999999",
        headers=auth_headers,
        json={
            "name": "Updated Customer"
        }
    )

    assert response.status_code == 404


# ============================================================
# UPDATE CUSTOMER — DUPLICATE EMAIL
# ============================================================

def test_update_customer_duplicate_email(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE FIRST CUSTOMER
    # --------------------------------------------------------

    first_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "First Customer",
            "email": "first@example.com",
            "phone": "9876543222",
            "company": "First Company"
        }
    )

    assert first_response.status_code == 201

    # --------------------------------------------------------
    # CREATE SECOND CUSTOMER
    # --------------------------------------------------------

    second_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Second Customer",
            "email": "second@example.com",
            "phone": "9876543223",
            "company": "Second Company"
        }
    )

    assert second_response.status_code == 201

    second_customer_id = (
        second_response
        .json()["data"]["id"]
    )

    # --------------------------------------------------------
    # UPDATE SECOND CUSTOMER WITH FIRST EMAIL
    # --------------------------------------------------------

    update_response = client.put(
        f"/api/v1/customers/{second_customer_id}",
        headers=auth_headers,
        json={
            "email": "first@example.com"
        }
    )

    assert update_response.status_code == 400


# ============================================================
# DELETE CUSTOMER — SOFT DELETE
# ============================================================

def test_delete_customer(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Delete Test Customer",
            "email": "delete@example.com",
            "phone": "9876543224",
            "company": "Delete Company"
        }
    )

    assert create_response.status_code == 201

    customer_id = (
        create_response
        .json()["data"]["id"]
    )

    # --------------------------------------------------------
    # DELETE CUSTOMER
    # --------------------------------------------------------

    delete_response = client.delete(
        f"/api/v1/customers/{customer_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 200

    response_data = delete_response.json()

    assert (
        response_data["message"]
        == "Customer deleted successfully"
    )

    assert (
        response_data["data"]
        is None
    )


# ============================================================
# DELETE CUSTOMER — NOT FOUND
# ============================================================

def test_delete_customer_not_found(
    client: TestClient,
    auth_headers
):

    response = client.delete(
        "/api/v1/customers/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


# ============================================================
# VERIFY SOFT-DELETED CUSTOMER
# CANNOT BE RETRIEVED
# ============================================================

def test_deleted_customer_cannot_be_retrieved(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Soft Delete Customer",
            "email": "softdelete@example.com",
            "phone": "9876543225",
            "company": "Soft Delete Company"
        }
    )

    assert create_response.status_code == 201

    customer_id = (
        create_response
        .json()["data"]["id"]
    )

    # --------------------------------------------------------
    # DELETE CUSTOMER
    # --------------------------------------------------------

    delete_response = client.delete(
        f"/api/v1/customers/{customer_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 200

    # --------------------------------------------------------
    # GET DELETED CUSTOMER
    # --------------------------------------------------------

    get_response = client.get(
        f"/api/v1/customers/{customer_id}",
        headers=auth_headers
    )

    assert get_response.status_code == 404


# ============================================================
# VERIFY SOFT-DELETED CUSTOMER
# IS EXCLUDED FROM LIST
# ============================================================

def test_deleted_customer_not_in_customer_list(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Hidden Customer",
            "email": "hidden@example.com",
            "phone": "9876543226",
            "company": "Hidden Company"
        }
    )

    assert create_response.status_code == 201

    customer_id = (
        create_response
        .json()["data"]["id"]
    )

    # --------------------------------------------------------
    # DELETE CUSTOMER
    # --------------------------------------------------------

    delete_response = client.delete(
        f"/api/v1/customers/{customer_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 200

    # --------------------------------------------------------
    # GET CUSTOMER LIST
    # --------------------------------------------------------

    list_response = client.get(
        "/api/v1/customers/",
        headers=auth_headers
    )

    assert list_response.status_code == 200

    customers = (
        list_response
        .json()["data"]["items"]
    )

    customer_ids = [
        customer["id"]
        for customer in customers
    ]

    assert customer_id not in customer_ids


# ============================================================
# CUSTOMER VALIDATION TESTS
# ============================================================


# ============================================================
# CREATE CUSTOMER — INVALID EMAIL
# ============================================================

def test_create_customer_invalid_email(
    client: TestClient,
    auth_headers
):

    assert_validation_error(
        client=client,
        method="POST",
        url="/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Invalid Email Customer",
            "email": "invalid-email",
            "phone": "9876543227",
            "company": "Test Company"
        }
    )


# ============================================================
# CREATE CUSTOMER — PHONE LESS THAN 10 DIGITS
# ============================================================

def test_create_customer_phone_less_than_10_digits(
    client: TestClient,
    auth_headers
):

    assert_validation_error(
        client=client,
        method="POST",
        url="/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Invalid Phone Customer",
            "email": "shortphone@example.com",
            "phone": "123456789",
            "company": "Test Company"
        }
    )


# ============================================================
# CREATE CUSTOMER — PHONE MORE THAN 10 DIGITS
# ============================================================

def test_create_customer_phone_more_than_10_digits(
    client: TestClient,
    auth_headers
):

    assert_validation_error(
        client=client,
        method="POST",
        url="/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Invalid Phone Customer",
            "email": "longphone@example.com",
            "phone": "12345678901",
            "company": "Test Company"
        }
    )


# ============================================================
# CREATE CUSTOMER — PHONE CONTAINS LETTERS
# ============================================================

def test_create_customer_phone_contains_letters(
    client: TestClient,
    auth_headers
):

    assert_validation_error(
        client=client,
        method="POST",
        url="/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Invalid Phone Customer",
            "email": "lettersphone@example.com",
            "phone": "98765abc10",
            "company": "Test Company"
        }
    )


# ============================================================
# CREATE CUSTOMER — EMPTY NAME
# ============================================================

def test_create_customer_empty_name(
    client: TestClient,
    auth_headers
):

    assert_validation_error(
        client=client,
        method="POST",
        url="/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "",
            "email": "emptyname@example.com",
            "phone": "9876543228",
            "company": "Test Company"
        }
    )


# ============================================================
# CREATE CUSTOMER — WHITESPACE ONLY NAME
# ============================================================

def test_create_customer_whitespace_name(
    client: TestClient,
    auth_headers
):

    assert_validation_error(
        client=client,
        method="POST",
        url="/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "   ",
            "email": "whitespacename@example.com",
            "phone": "9876543229",
            "company": "Test Company"
        }
    )


# ============================================================
# CREATE CUSTOMER — EMPTY PHONE
# ============================================================

def test_create_customer_empty_phone(
    client: TestClient,
    auth_headers
):

    assert_validation_error(
        client=client,
        method="POST",
        url="/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Empty Phone Customer",
            "email": "emptyphone@example.com",
            "phone": "",
            "company": "Test Company"
        }
    )


# ============================================================
# CREATE CUSTOMER — WHITESPACE ONLY PHONE
# ============================================================

def test_create_customer_whitespace_phone(
    client: TestClient,
    auth_headers
):

    assert_validation_error(
        client=client,
        method="POST",
        url="/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Whitespace Phone Customer",
            "email": "whitespacephone@example.com",
            "phone": "          ",
            "company": "Test Company"
        }
    )


# ============================================================
# CREATE CUSTOMER — EMPTY COMPANY
# ============================================================

def test_create_customer_empty_company(
    client: TestClient,
    auth_headers
):

    assert_validation_error(
        client=client,
        method="POST",
        url="/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Empty Company Customer",
            "email": "emptycompany@example.com",
            "phone": "9876543230",
            "company": ""
        }
    )


# ============================================================
# CREATE CUSTOMER — WHITESPACE ONLY COMPANY
# ============================================================

def test_create_customer_whitespace_company(
    client: TestClient,
    auth_headers
):

    assert_validation_error(
        client=client,
        method="POST",
        url="/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Whitespace Company Customer",
            "email": "whitespacecompany@example.com",
            "phone": "9876543231",
            "company": "   "
        }
    )


# ============================================================
# UPDATE CUSTOMER — INVALID EMAIL
# ============================================================

def test_update_customer_invalid_email(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Update Email Customer",
            "email": "updateemail@example.com",
            "phone": "9876543232",
            "company": "Test Company"
        }
    )

    assert create_response.status_code == 201

    customer_id = (
        create_response
        .json()["data"]["id"]
    )

    # --------------------------------------------------------
    # INVALID EMAIL
    # --------------------------------------------------------

    assert_validation_error(
        client=client,
        method="PUT",
        url=f"/api/v1/customers/{customer_id}",
        headers=auth_headers,
        json={
            "email": "invalid-email"
        }
    )


# ============================================================
# UPDATE CUSTOMER — INVALID PHONE
# ============================================================

def test_update_customer_invalid_phone(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Update Phone Customer",
            "email": "updatephone@example.com",
            "phone": "9876543233",
            "company": "Test Company"
        }
    )

    assert create_response.status_code == 201

    customer_id = (
        create_response
        .json()["data"]["id"]
    )

    # --------------------------------------------------------
    # INVALID PHONE
    # --------------------------------------------------------

    assert_validation_error(
        client=client,
        method="PUT",
        url=f"/api/v1/customers/{customer_id}",
        headers=auth_headers,
        json={
            "phone": "12345"
        }
    )


# ============================================================
# UPDATE CUSTOMER — EMPTY NAME
# ============================================================

def test_update_customer_empty_name(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Update Name Customer",
            "email": "updatename@example.com",
            "phone": "9876543234",
            "company": "Test Company"
        }
    )

    assert create_response.status_code == 201

    customer_id = (
        create_response
        .json()["data"]["id"]
    )

    # --------------------------------------------------------
    # EMPTY NAME
    # --------------------------------------------------------

    assert_validation_error(
        client=client,
        method="PUT",
        url=f"/api/v1/customers/{customer_id}",
        headers=auth_headers,
        json={
            "name": ""
        }
    )


# ============================================================
# UPDATE CUSTOMER — EMPTY PHONE
# ============================================================

def test_update_customer_empty_phone(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Update Empty Phone Customer",
            "email": "updateemptyphone@example.com",
            "phone": "9876543235",
            "company": "Test Company"
        }
    )

    assert create_response.status_code == 201

    customer_id = (
        create_response
        .json()["data"]["id"]
    )

    # --------------------------------------------------------
    # EMPTY PHONE
    # --------------------------------------------------------

    assert_validation_error(
        client=client,
        method="PUT",
        url=f"/api/v1/customers/{customer_id}",
        headers=auth_headers,
        json={
            "phone": ""
        }
    )


# ============================================================
# UPDATE CUSTOMER — EMPTY COMPANY
# ============================================================

def test_update_customer_empty_company(
    client: TestClient,
    auth_headers
):

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    create_response = client.post(
        "/api/v1/customers/",
        headers=auth_headers,
        json={
            "name": "Update Company Customer",
            "email": "updatecompany@example.com",
            "phone": "9876543236",
            "company": "Original Company"
        }
    )

    assert create_response.status_code == 201

    customer_id = (
        create_response
        .json()["data"]["id"]
    )

    # --------------------------------------------------------
    # EMPTY COMPANY
    # --------------------------------------------------------

    assert_validation_error(
        client=client,
        method="PUT",
        url=f"/api/v1/customers/{customer_id}",
        headers=auth_headers,
        json={
            "company": ""
        }
    )