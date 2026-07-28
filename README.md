# CRM System Enhancement – Lead Management Module

A production-oriented CRM backend API built with **Python, FastAPI, SQLAlchemy, PostgreSQL, JWT Authentication, Role-Based Access Control (RBAC), Audit Logging, Notifications, Background Processing, and Automated API Testing**.

This project extends the CRM API system developed in Task 2 by adding Lead Management, Customer Activity Tracking, Follow-up Management, Role-Based Access Control, Notifications, Audit Logging, and Background Processing.

---

## 1. Project Overview

### Project Name

**CRM System Enhancement – Lead Management Module**

### Objective

The objective of this project is to extend an existing CRM API system with real-world CRM workflow features, including:

* Lead Management
* Customer Activity Tracking
* Customer Timeline
* Follow-up Management
* Role-Based Access Control
* Permission Management
* Lead Assignment
* Notification System
* Audit Logging
* Background Processing
* API Testing

The system is designed using a modular FastAPI architecture with reusable database models, Pydantic schemas, API routers, authentication, authorization, and standardized API responses.

---

# 2. Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

## Database

* PostgreSQL
* Neon PostgreSQL for cloud database hosting
* SQLite for automated test database

## Authentication

* JWT Authentication
* Password hashing
* Token-based authentication

## Authorization

* Role-Based Access Control (RBAC)
* Permission-based authorization

## API Documentation

* Swagger UI
* OpenAPI

## API Testing

* Pytest
* Postman Collection

## Database Migration

* Alembic

## Background Processing

* Background scheduler
* Scheduled CRM workflow processing

## Version Control

* Git
* GitHub

---

# 3. Main Features

The application provides the following major features:

### Authentication

* User Registration
* User Login
* JWT Token Authentication
* Current User Authentication
* Protected API endpoints

### Customer Management

* Create Customer
* Get Customer
* List Customers
* Update Customer
* Soft Delete Customer
* Customer Search
* Pagination
* Filtering
* Sorting

### Lead Management

* Create Lead
* List Leads
* Get Single Lead
* Update Lead
* Assign Lead
* Soft Delete Lead
* Lead Search
* Lead Filtering
* Lead Pagination
* Lead Sorting
* Date Range Filtering

### Customer Activity Timeline

* Create Customer Activity
* Get Customer Timeline
* Track:

  * Calls
  * Emails
  * Meetings
  * Notes
  * Follow-ups

### Follow-up Management

* Create Follow-up
* List Follow-ups
* Filter by Status
* Filter by Customer
* Today's Follow-ups
* Upcoming Follow-ups
* Overdue Follow-ups
* Update Follow-up Status
* Pagination

### Role-Based Access Control

The system supports role-based permissions for CRM operations.

Available roles include:

* Admin
* Manager
* Sales Executive
* Viewer

Permissions include:

* Create Lead
* Delete Lead
* View Customers
* Assign Lead
* Manage Users
* Create Customer Activity
* Create Follow-up
* Update Follow-up
* View Audit Logs

### Notification System

Notifications are generated for important workflow events.

For example:

* When a lead is assigned to a user
* When a new lead is assigned during lead creation
* When a lead assignment changes

Users can:

* Get their notifications
* Filter notifications by read status
* Mark notifications as read/unread

### Audit Logging

The application maintains an audit trail for important operations.

Audit logs store:

* User ID
* Action
* Module
* Previous data
* New data
* Created timestamp

Audit logging is implemented for important CRM operations such as:

* Lead creation
* Lead update
* Lead assignment
* Lead deletion
* Customer operations
* Follow-up creation
* Follow-up status updates

### Background Processing

The application includes background scheduler functionality for automated CRM workflow processing.

The application starts the scheduler during application startup and stops it during application shutdown.

---

# 4. Project Structure

```text
TASK-3/
│
├── app/
│   │
│   ├── background/
│   │   └── scheduler.py
│   │
│   ├── core/
│   │   ├── audit.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── exception_handlers.py
│   │   └── responses.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── roles.py
│   │   ├── permissions.py
│   │   ├── role_permissions.py
│   │   ├── users.py
│   │   ├── customers.py
│   │   ├── leads.py
│   │   ├── audit_logs.py
│   │   ├── customer_activities.py
│   │   ├── follow_ups.py
│   │   └── notifications.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── customers.py
│   │   ├── permissions.py
│   │   ├── leads.py
│   │   ├── audit_logs.py
│   │   ├── customer_activities.py
│   │   ├── follow_ups.py
│   │   └── notifications.py
│   │
│   ├── schemas/
│   │   ├── users.py
│   │   ├── customers.py
│   │   ├── leads.py
│   │   ├── audit_logs.py
│   │   ├── customer_activities.py
│   │   ├── follow_ups.py
│   │   └── notifications.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_customers.py
│   ├── test_leads.py
│   └── test_permissions.py
│
├── pytest.ini
├── alembic.ini
├── requirements.txt
├── .env
└── README.md
```

---

# 5. Installation Steps

## Step 1: Clone the Repository

Clone the project from GitHub:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project directory:

```bash
cd TASK-3
```

---

## Step 2: Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv SMS_venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\SMS_venv\Scripts\Activate.ps1
```

If using Command Prompt:

```cmd
SMS_venv\Scripts\activate
```

---

## Step 3: Install Dependencies

Install all required dependencies:

```bash
pip install -r requirements.txt
```

---

## Step 4: Install Testing Dependencies

Install Pytest and HTTP testing support:

```bash
pip install pytest httpx
```

If required by the project environment:

```bash
pip install sqlalchemy
```

---

# 6. Environment Setup

Create a `.env` file in the root project directory.

Example:

```env
DATABASE_URL=postgresql+psycopg://username:password@host/database
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Environment Variables

| Variable                      | Description                                |
| ----------------------------- | ------------------------------------------ |
| `DATABASE_URL`                | PostgreSQL/Neon database connection string |
| `SECRET_KEY`                  | Secret key used for JWT authentication     |
| `ALGORITHM`                   | JWT signing algorithm                      |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time                  |

### Important

Do not commit the `.env` file to GitHub.

Add `.env` to `.gitignore`:

```gitignore
.env
SMS_venv/
__pycache__/
.pytest_cache/
*.pyc
```

---

# 7. Database Setup

The project uses **PostgreSQL** as the primary application database.

The application database is hosted using **Neon PostgreSQL**.

SQLAlchemy is used as the ORM layer.

Database configuration is handled through:

```text
app/core/database.py
```

The database connection is configured using the `DATABASE_URL` environment variable.

---

## Database Connection

The application uses:

```python
engine = create_engine(
    settings.DATABASE_URL,
    echo=True
)
```

The SQLAlchemy session is provided through the `get_db()` dependency.

---

## Database Migration

The project uses Alembic for database migrations.

Create a new migration:

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback the latest migration:

```bash
alembic downgrade -1
```

Check the current migration:

```bash
alembic current
```

Check migration history:

```bash
alembic history
```

---

# 8. Database Tables

The project contains the following major database entities:

* Users
* Roles
* Permissions
* Role Permissions
* Customers
* Leads
* Audit Logs
* Customer Activities
* Follow-ups
* Notifications

### Users

Stores CRM user accounts and authentication information.

### Roles

Stores available user roles:

* Admin
* Manager
* Sales Executive
* Viewer

### Permission Matrix

| Permission / Feature     | Admin | Manager | Sales Executive | Viewer |
| ------------------------ | ----: | ------: | --------------: | -----: |
| Create Lead              |   Yes |     Yes |             Yes |     No |
| Delete Lead              |   Yes |     Yes |              No |     No |
| View Customers           |   Yes |     Yes |             Yes |    Yes |
| Assign Lead              |   Yes |     Yes |              No |     No |
| Manage Users             |   Yes |      No |              No |     No |
| Create Customer Activity |   Yes |     Yes |             Yes |     No |
| Create Follow-up         |   Yes |     Yes |             Yes |     No |
| Update Follow-up         |   Yes |     Yes |             Yes |     No |
| View Audit Logs          |   Yes |      No |              No |     No |


### Permissions

Stores individual permissions available in the system.

### Role Permissions

Maps roles to their assigned permissions.

### Customers

Stores CRM customer information.

### Leads

Stores sales lead information and assignment details.

### Audit Logs

Stores historical records of important system operations.

### Customer Activities

Stores customer interaction history.

### Follow-ups

Stores scheduled customer follow-ups and their status.

### Notifications

Stores user-specific system notifications.

---

# 9. Run the Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# 10. API Documentation

FastAPI automatically provides interactive API documentation.

## Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger can be used to:

* View all API endpoints
* View request schemas
* View response schemas
* Test APIs
* Authenticate using JWT
* Verify API responses

---

## ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

---

# 11. API Usage

All application APIs use the following base URL:

```text
http://127.0.0.1:8000/api/v1
```

Authentication-protected endpoints require a JWT token.

The token should be provided using the HTTP Authorization header:

```text
Authorization: Bearer <access_token>
```

---

# 12. Authentication APIs

## Register User

```http
POST /api/v1/auth/register
```

Purpose:

Creates a new CRM user account.

---

## Login

```http
POST /api/v1/auth/login
```

Purpose:

Authenticates the user and returns a JWT access token.

The returned access token should be used for protected API requests.

---

# 13. Customer APIs

Customer management APIs provide CRUD operations and support search, filtering, pagination, and sorting.

Typical operations include:

```http
POST /api/v1/customers/
GET /api/v1/customers/
GET /api/v1/customers/{customer_id}
PUT /api/v1/customers/{customer_id}
DELETE /api/v1/customers/{customer_id}
```

Customer APIs support:

* Customer creation
* Customer listing
* Customer retrieval
* Customer updates
* Soft deletion
* Search
* Pagination
* Filtering
* Sorting

---

# 14. Lead APIs

The Lead Management module provides complete sales lead management.

## Create Lead

```http
POST /api/v1/leads/
```

Example request:

```json
{
    "name": "John Smith",
    "email": "john@test.com",
    "phone": "+123456789",
    "company": "ABC Corporation",
    "source": "Website",
    "status": "New"
}
```

---

## List Leads

```http
GET /api/v1/leads/
```

Pagination example:

```text
GET /api/v1/leads/?page=1&limit=20
```

Search example:

```text
GET /api/v1/leads/?search=john
```

Status filter:

```text
GET /api/v1/leads/?status=Qualified
```

Assigned user filter:

```text
GET /api/v1/leads/?assigned_to=5
```

Date range filter:

```text
GET /api/v1/leads/?from_date=2026-07-01&to_date=2026-07-31
```

Sorting:

```text
GET /api/v1/leads/?sort_by=created_at&sort_order=desc
```

---

## Get Single Lead

```http
GET /api/v1/leads/{lead_id}
```

---

## Update Lead

```http
PUT /api/v1/leads/{lead_id}
```

Example:

```json
{
    "status": "Qualified",
    "company": "XYZ Ltd"
}
```

---

## Assign Lead

```http
PATCH /api/v1/leads/{lead_id}/assign
```

Example:

```text
PATCH /api/v1/leads/1/assign?assigned_to=5
```

When a lead is assigned to a user, the system creates a notification for the assigned user.

---

## Delete Lead

```http
DELETE /api/v1/leads/{lead_id}
```

Lead deletion is implemented as a soft delete.

The deletion is also recorded through audit logging.

---

# 15. Customer Activity APIs

Customer activities maintain the interaction history of a customer.

Supported activity types:

* Call
* Email
* Meeting
* Note
* Follow-up

---

## Create Customer Activity

```http
POST /api/v1/customers/{customer_id}/activities
```

Example request:

```json
{
    "type": "Call",
    "description": "Discussed pricing and requirements"
}
```

The authenticated user is automatically stored as the activity creator.

---

## Get Customer Timeline

```http
GET /api/v1/customers/{customer_id}/timeline
```

The timeline contains the customer's historical activities.

Example response data:

```json
[
    {
        "type": "Call",
        "description": "Discussed pricing",
        "date": "2026-07-21T10:30:00"
    },
    {
        "type": "Email",
        "description": "Proposal sent",
        "date": "2026-07-22T11:00:00"
    }
]
```

---

# 16. Follow-up APIs

Follow-ups are used to schedule and track future customer interactions.

---

## Create Follow-up

```http
POST /api/v1/followups/
```

Example request:

```json
{
    "customer_id": 10,
    "followup_date": "2026-08-01",
    "type": "Email",
    "notes": "Send quotation"
}
```

New follow-ups are created with:

```text
status = pending
```

---

## List Follow-ups

```http
GET /api/v1/followups/
```

Filter by status:

```text
GET /api/v1/followups/?status=pending
```

Filter by customer:

```text
GET /api/v1/followups/?customer_id=10
```

Today's follow-ups:

```text
GET /api/v1/followups/?date=today
```

Upcoming follow-ups:

```text
GET /api/v1/followups/?date=upcoming
```

Overdue follow-ups:

```text
GET /api/v1/followups/?date=overdue
```

Pagination:

```text
GET /api/v1/followups/?page=1&limit=20
```

---

## Update Follow-up Status

```http
PATCH /api/v1/followups/{followup_id}/status
```

Example request:

```json
{
    "status": "completed"
}
```

Supported statuses:

* pending
* completed
* cancelled

---

# 17. Role-Based Access Control

The application uses permission-based authorization.

The main roles are:

| Role            | Description                         |
| --------------- | ----------------------------------- |
| Admin           | Full system access                  |
| Manager         | Management and lead workflow access |
| Sales Executive | Sales and customer workflow access  |
| Viewer          | Read-only access                    |

Examples of permissions include:

```text
create_lead
delete_lead
view_customers
assign_lead
manage_users
create_customer_activity
create_followup
update_followup
view_audit_logs
```

Protected endpoints verify the authenticated user's permissions before allowing access.

---

# 18. Permission APIs

Permission-related endpoints are available for managing and verifying role-based permissions.

Permissions are associated with roles through the role-permission mapping.

The system ensures that users without the required permission receive an authorization error.

Example:

```text
403 Forbidden
```

when a user attempts to access a restricted endpoint.

---

# 19. Notification APIs

Notifications are user-specific.

A user can only access their own notifications.

---

## Get Notifications

```http
GET /api/v1/notifications/
```

Filter unread notifications:

```text
GET /api/v1/notifications/?is_read=false
```

Filter read notifications:

```text
GET /api/v1/notifications/?is_read=true
```

Pagination:

```text
GET /api/v1/notifications/?page=1&limit=20
```

---

## Mark Notification as Read/Unread

```http
PATCH /api/v1/notifications/{notification_id}/read
```

Example:

```json
{
    "is_read": true
}
```

---

# 20. Audit Log APIs

Audit logs provide a history of important CRM actions.

---

## List Audit Logs

```http
GET /api/v1/audit-logs/
```

Filter by user:

```text
GET /api/v1/audit-logs/?user_id=5
```

Filter by action:

```text
GET /api/v1/audit-logs/?action=CREATE
```

Filter by module:

```text
GET /api/v1/audit-logs/?module=leads
```

Date range:

```text
GET /api/v1/audit-logs/?from_date=2026-07-01&to_date=2026-07-31
```

Pagination:

```text
GET /api/v1/audit-logs/?page=1&limit=20
```

Sorting:

```text
GET /api/v1/audit-logs/?sort_by=created_at&sort_order=desc
```

Audit log access is protected by the appropriate permission.

---

# 21. Standard API Response Format

The application uses a common response format for successful API responses.

Example:

```json
{
    "code": 200,
    "status": "Success",
    "message": "Request successful",
    "data": {}
}
```

Successful creation example:

```json
{
    "code": 201,
    "status": "Success",
    "message": "Lead created successfully",
    "data": {}
}
```

Error response example:

```json
{
    "code": 400,
    "status": "Error",
    "message": "Request failed",
    "data": null
}
```

The standard response utility is implemented in:

```text
app/core/responses.py
```

---

# 22. Error Handling

The application includes centralized exception handling.

The following errors are handled consistently:

* HTTP errors
* Validation errors
* Authentication errors
* Authorization errors
* Not Found errors
* Bad Request errors
* Internal Server Errors

FastAPI validation errors return appropriate `422` responses.

Unauthorized users receive appropriate authentication or permission errors.

Unexpected server errors are handled through the global exception handler.

---

# 23. API Testing

The project includes automated API testing using:

* Pytest
* SQLite test database

The test database is separated from the production PostgreSQL/Neon database.

The testing configuration is defined using:

```text
pytest.ini
```

Example:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
```

The test setup is configured in:

```text
tests/conftest.py
```

---

## Automated Test Modules

The automated testing setup covers:

### Authentication Tests

* User Registration
* User Login
* Invalid Login

### Customer API Tests

* Create Customer
* List Customers
* Get Customer
* Update Customer
* Delete Customer

### Lead API Tests

* Create Lead
* List Leads
* Get Lead
* Update Lead
* Assign Lead
* Delete Lead

### Permission API Tests

* Authorized Access
* Unauthorized Access

Run the test suite:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

---

# 24. Postman Collection

The project includes a Postman Collection for manual API verification.

The Postman collection can be used to test:

* Authentication
* Customer APIs
* Lead APIs
* Permission APIs
* Customer Activity APIs
* Follow-up APIs
* Notification APIs
* Audit Log APIs

The Postman Collection should be included with the final project deliverables.

---

# 25. Swagger API Documentation

FastAPI automatically generates Swagger/OpenAPI documentation.

After starting the application, open:

```text
http://127.0.0.1:8000/docs
```

The Swagger interface allows API consumers and evaluators to:

* Explore all available APIs
* View request parameters
* View request bodies
* View response structures
* Authorize using JWT
* Execute API requests
* Verify API responses

The Swagger `/docs` URL is part of the project documentation deliverables.

---

# 26. Background Scheduler

The application includes background scheduler functionality.

The scheduler is started when the FastAPI application starts and stopped when the application shuts down.

The scheduler implementation is located at:

```text
app/background/scheduler.py
```

The architecture can support automated CRM workflows such as:

* Daily follow-up reminders
* Automated notification processing
* Scheduled CRM reports
* Other periodic background operations

---

# 27. Health Check

The application provides a health check endpoint:

```http
GET /health
```

Example response:

```json
{
    "code": 200,
    "status": "Success",
    "message": "Health check successful",
    "data": {
        "status": "healthy"
    }
}
```

---

# 28. Root Endpoint

The application provides a root endpoint:

```http
GET /
```

Example response:

```json
{
    "code": 200,
    "status": "Success",
    "message": "CRM Task 3 API is running",
    "data": null
}
```

---

# 29. Running the Complete Project

### Step 1

Activate the virtual environment:

```powershell
.\SMS_venv\Scripts\Activate.ps1
```

### Step 2

Verify the `.env` configuration.

### Step 3

Run database migrations:

```bash
alembic upgrade head
```

### Step 4

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

### Step 5

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

### Step 6

Authenticate using the login API.

### Step 7

Authorize Swagger using the JWT token.

### Step 8

Test the APIs module by module.

---

# 30. Recommended API Verification Flow

For manual API verification, follow this sequence:

```text
1. Register User
        ↓
2. Login
        ↓
3. Get JWT Token
        ↓
4. Authorize Protected APIs
        ↓
5. Verify Customer APIs
        ↓
6. Verify Lead APIs
        ↓
7. Verify Lead Assignment
        ↓
8. Verify Notifications
        ↓
9. Verify Customer Activities
        ↓
10. Verify Customer Timeline
        ↓
11. Verify Follow-ups
        ↓
12. Verify Audit Logs
        ↓
13. Verify RBAC Permissions
```

---

# 31. Git Workflow

The project uses Git for version control.

Basic workflow:

```bash
git status
```

Add changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Update CRM Task 3 APIs"
```

Push changes:

```bash
git push origin main
```

Before pushing final changes, verify:

* Application starts successfully
* Database connection works
* Alembic migrations are up to date
* Swagger documentation loads
* Postman APIs work
* Automated tests are verified
* No `.env` or secrets are committed

---

# 32. Final Deliverables

The final submission should include:

### 1. Source Code

GitHub repository containing the complete FastAPI project.

### 2. Database Documentation

* ER Diagram
* Database Schema

### 3. API Documentation

Swagger/OpenAPI documentation available through:

```text
/docs
```

### 4. API Testing

Postman Collection containing the API requests used for testing.

### 5. README Documentation

This README should include:

* Installation Steps
* Environment Setup
* Database Setup
* API Usage

---

# 33. Project Completion Checklist

## Authentication

* [x] User Registration
* [x] JWT Login
* [x] Protected APIs
* [x] Authentication testing

## Customer Management

* [x] Customer CRUD
* [x] Search
* [x] Pagination
* [x] Filtering
* [x] Sorting
* [x] Soft Delete

## Lead Management

* [x] Create Lead
* [x] List Leads
* [x] Get Lead
* [x] Update Lead
* [x] Assign Lead
* [x] Soft Delete
* [x] Search
* [x] Filtering
* [x] Pagination
* [x] Sorting
* [x] Date Range Filtering

## Customer Activity

* [x] Create Activity
* [x] Customer Timeline

## Follow-ups

* [x] Create Follow-up
* [x] List Follow-ups
* [x] Status Filtering
* [x] Customer Filtering
* [x] Today's Follow-ups
* [x] Upcoming Follow-ups
* [x] Overdue Follow-ups
* [x] Update Follow-up Status

## RBAC

* [x] Roles
* [x] Permissions
* [x] Role-Permission Mapping
* [x] Permission-Based Authorization

## Notifications

* [x] Create Notifications
* [x] Get User Notifications
* [x] Read/Unread Filtering
* [x] Mark Notification Read/Unread

## Audit Logging

* [x] Audit Log Model
* [x] Audit Log Creation
* [x] Audit Log Listing
* [x] Filtering
* [x] Pagination
* [x] Sorting

## Background Processing

* [x] Background Scheduler Integration

## API Testing

* [x] Pytest Setup
* [x] SQLite Test Database
* [x] Authentication Tests
* [x] Customer API Tests
* [x] Lead API Tests
* [x] Permission API Tests
* [x] Postman Collection

## Documentation

* [x] Swagger/OpenAPI
* [x] README
* [ ] ER Diagram
* [ ] Database Schema Documentation
* [ ] Final Postman Collection Export
* [ ] Final GitHub Push

---

# 34. Conclusion

This project implements a modular CRM backend system using FastAPI with authentication, authorization, lead management, customer management, workflow automation, notifications, audit logging, and background processing.

The system follows a structured architecture with:

* FastAPI routers
* SQLAlchemy models
* Pydantic schemas
* JWT authentication
* Permission-based RBAC
* Centralized exception handling
* Standardized API responses
* Database migrations
* Audit logging
* Automated testing
* Swagger/OpenAPI documentation

The project is designed to demonstrate practical CRM backend architecture, database relationships, REST API development, authentication and authorization, sales workflow management, and enterprise-level backend development practices.
