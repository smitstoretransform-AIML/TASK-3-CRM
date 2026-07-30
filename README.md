# CRM System Enhancement – Lead Management Module

## Task 3: CRM Lead Management & Workflow Automation APIs

A production-oriented CRM backend API built with **Python FastAPI**, **SQLAlchemy**, **PostgreSQL (Neon)**, **JWT Authentication**, **Role-Based Access Control (RBAC)**, **Audit Logging**, **Notifications**, **Background Processing**, and **Email Notifications**.

This project extends the Customer Management foundation developed in Task 2 by introducing a complete CRM workflow for lead management, customer interactions, follow-ups, permissions, notifications, audit tracking, and automated background processes.

---

# 1. Project Overview

## Project Name

**CRM System Enhancement – Lead Management Module**

## Objective

The objective of this project is to extend the existing CRM API system with:

* Lead Management
* Customer Activity Tracking
* Customer Timeline
* Follow-up Management
* Role-Based Access Control
* Permission Management
* Lead Assignment
* Notifications
* Audit Logging
* Background Processing
* Email Notifications
* CRM workflow automation

The project follows a modular FastAPI architecture and provides RESTful APIs documented through Swagger/OpenAPI.

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
* Neon PostgreSQL

## Authentication

* JWT Authentication
* Password Hashing
* Protected API endpoints

## Authorization

* Role-Based Access Control (RBAC)
* Permission-based authorization

## API Documentation

* Swagger UI
* OpenAPI

Available at:

```text
/docs
```

## Testing

* Postman
* Postman Collection
* Pytest setup for automated API testing

## Background Processing

* Background scheduler
* Automated follow-up reminder processing
* Email notification processing

## Version Control

* Git
* GitHub

---

# 3. Core Features

The project provides the following major modules:

```text
Authentication
    ↓
Role & Permission Management
    ↓
Customer Management
    ↓
Lead Management
    ↓
Lead Assignment
    ↓
Lead Activities
    ↓
Lead Follow-ups
    ↓
Lead Qualification
    ↓
Lead Conversion
    ↓
Customer Activities
    ↓
Customer Timeline
    ↓
Customer Follow-ups
    ↓
Notifications
    ↓
Audit Logging
    ↓
Background Processing
    ↓
Email Notifications
```

---

# 4. Authentication

The API provides secure user authentication using JWT.

## Registration

Users can register using the registration API.

The registration flow is:

```text
Registration Request
        ↓
Validate Input
        ↓
Check Existing Email
        ↓
Hash Password
        ↓
Create User
        ↓
Save User
```

Passwords are stored securely using hashing rather than plain-text storage.

## Login

The login flow is:

```text
Login Request
        ↓
Find User
        ↓
Verify Password
        ↓
Generate JWT
        ↓
Return Access Token
```

The access token is then used to access protected APIs.

Example:

```text
Authorization: Bearer <JWT_TOKEN>
```

---

# 5. Role-Based Access Control

The application implements Role-Based Access Control with permission-based authorization.

## Available Roles

* Admin
* Manager
* Sales Executive
* Viewer

## Permission-Based Authorization

APIs use permission checks to determine whether the authenticated user is allowed to perform an operation.

Examples of permissions include:

```text
create_lead
delete_lead
assign_lead
view_customers
manage_users
create_followup
update_followup
create_customer_activity
view_audit_logs
```

The permission system is implemented using:

```text
Users
    ↓
Roles
    ↓
Role Permissions
    ↓
Permissions
    ↓
Protected API
```

Unauthorized access is rejected with an appropriate HTTP response.

Expected security behavior:

```text
No Token
    ↓
401 Unauthorized

Invalid Token
    ↓
401 Unauthorized

Valid Token + Missing Permission
    ↓
403 Forbidden

Valid Token + Required Permission
    ↓
API Access Granted
```

---

# 6. Customer Management

The CRM provides customer management functionality.

## Features

* Create Customer
* Get Customer
* List Customers
* Update Customer
* Delete Customer
* Search Customers
* Pagination
* Filtering
* Sorting
* Soft Delete

Customers are associated with the authenticated user who creates them.

Soft-deleted customers are excluded from normal customer queries.

---

# 7. Lead Management

The Lead Management module is the primary feature of Task 3.

## Features

* Create Lead
* Get Lead
* List Leads
* Update Lead
* Assign Lead
* Delete Lead
* Search Leads
* Filter Leads
* Sort Leads
* Pagination
* Date Range Filtering
* Soft Delete

## Lead Search

Leads can be searched using:

* Name
* Email
* Phone
* Company

## Lead Filters

Supported filters include:

* Status
* Source
* Assigned User
* Date Range

## Lead Sorting

Leads can be sorted by supported fields such as:

* ID
* Name
* Email
* Company
* Source
* Status
* Created Date
* Updated Date

Both ascending and descending sorting are supported.

## Lead Assignment

Leads can be assigned to users with the required permission.

The workflow is:

```text
Lead Created
      ↓
Lead Assigned
      ↓
Assigned User Receives Notification
      ↓
Assignment Recorded in Audit Log
```

When a lead is assigned to a user, a notification is generated.

---

# 8. Customer Activity Timeline

The CRM maintains a complete history of customer interactions.

Supported activity types:

* Call
* Email
* Meeting
* Note
* Follow-up

## Create Activity

Activities can be created against both Leads and Customers.

Example workflow:

```text
Lead Created
    ↓
Sales Team Contacts Lead
    ↓
Call Logged
    ↓
Email Logged
    ↓
Meeting Logged
```

## Customer Timeline

The timeline API returns customer interaction history ordered by activity creation time.

Example:

```text
Customer
    │
    ├── Call
    ├── Email
    ├── Meeting
    ├── Note
    └── Follow-up
```

---

# 9. Follow-up Management

The Follow-up module manages customer follow-up activities.

## Features

* Create Follow-up
* List Follow-ups
* Filter by Customer
* Filter by Status
* Filter by Date
* Today's Follow-ups
* Upcoming Follow-ups
* Overdue Follow-ups
* Update Follow-up Status

## Follow-up Statuses

```text
pending
completed
cancelled
```

## Follow-up Date Categories

```text
Today
Upcoming
Overdue
```

The overdue filter identifies pending follow-ups whose scheduled date has passed.

---

# 10. Notification System

The CRM includes a notification mechanism for user-specific notifications.

## Example

When a lead is assigned:

```text
New Lead Assigned

John Smith assigned to Alex
```

Notifications are stored in the database and associated with the target user.

## Notification Features

* List Notifications
* Filter by Read/Unread Status
* Pagination
* Mark Notification as Read
* Mark Notification as Unread

Users can only access their own notifications.

---

# 11. Audit Logging

The application maintains audit logs for important business operations.

Audit logging is used to track changes and provide historical information about system activity.

## Logged Operations

Examples include:

* Customer creation
* Customer update
* Customer deletion
* Lead creation
* Lead update
* Lead assignment
* Lead deletion
* Follow-up creation
* Follow-up status updates

## Audit Data

Audit records include:

```text
user_id
action
module
old_data
new_data
created_at
```

Example:

```text
User: Alex
Action: UPDATE
Module: customers

Old:
{
    "email": "abc@test.com"
}

New:
{
    "email": "xyz@test.com"
}
```

## Audit Log API Features

* List Audit Logs
* Filter by User
* Filter by Action
* Filter by Module
* Filter by Date Range
* Pagination
* Sorting

Audit logs provide traceability for important CRM operations.

---

# 12. Background Processing

The application includes background processing for automated CRM operations.

The background scheduler is integrated with the FastAPI application lifecycle.

```text
FastAPI Startup
      ↓
Scheduler Starts
      ↓
Background Jobs Run
      ↓
FastAPI Shutdown
      ↓
Scheduler Stops
```

Background processing supports automated follow-up reminder workflows and email notifications.

---

# 13. Email Notifications

The application supports email notifications for CRM follow-up reminders.

The workflow is:

```text
Follow-up Created
      ↓
Follow-up Becomes Eligible
      ↓
Background Scheduler Detects Follow-up
      ↓
Email Reminder Sent
      ↓
reminder_sent_at Updated
```

The `reminder_sent_at` field is used to prevent duplicate reminder emails.

```text
reminder_sent_at = NULL
        ↓
Email Sent Successfully
        ↓
reminder_sent_at = Timestamp
        ↓
Future Scheduler Runs
        ↓
Reminder Skipped
```

The email functionality was verified using a real accessible test email address.

The verification confirmed:

* Email configuration works
* Email delivery works
* Follow-up reminder processing works
* Reminder timestamp is updated
* Duplicate reminders are prevented

---

# 14. Database Design

The application uses PostgreSQL hosted on Neon.

The current CRM database contains the following 10 main tables:

```text
users
roles
permissions
role_permissions
customers
leads
customer_activities
followups
audit_logs
notifications
```

## Database Relationship Overview

```text
roles
  │
  └── users
        │
        ├── customers
        │      ├── customer_activities
        │      └── followups
        │
        ├── leads
        │      ├── created_by
        │      └── assigned_to
        │
        ├── audit_logs
        │
        └── notifications

roles
  │
  └── role_permissions
          │
          └── permissions
```

---

# 15. Database Tables

## users

Stores application users.

Main fields:

```text
id
name
email
password
role_id
created_at
```

Relationship:

```text
users.role_id → roles.id
```

---

## roles

Stores application roles.

Main fields:

```text
id
name
```

Available roles:

```text
Admin
Manager
Sales Executive
Viewer
```

---

## permissions

Stores available system permissions.

Main fields:

```text
id
name
```

---

## role_permissions

Maps roles to permissions.

Main fields:

```text
id
role_id
permission_id
```

Relationships:

```text
role_id → roles.id
permission_id → permissions.id
```

---

## customers

Stores CRM customer records.

Main fields:

```text
id
name
email
phone
company
created_by
created_at
updated_at
deleted_at
```

Relationships:

```text
created_by → users.id
```

Soft deletion is implemented using:

```text
deleted_at
```

---

## leads

Stores CRM sales leads.

Main fields:

```text
id
name
email
phone
company
source
status
assigned_to
created_by
created_at
updated_at
deleted_at
```

Relationships:

```text
assigned_to → users.id
created_by → users.id
```

Lead deletion uses soft delete.

---

## customer_activities

Stores customer interaction history.

Main fields:

```text
id
customer_id
type
description
created_by
created_at
```

Relationships:

```text
customer_id → customers.id
created_by → users.id
```

---

## followups

Stores customer follow-up records.

Main fields:

```text
id
customer_id
date
type
status
notes
created_at
reminder_sent_at
```

Relationship:

```text
customer_id → customers.id
```

---

## audit_logs

Stores historical system activity.

Main fields:

```text
id
user_id
action
module
old_data
new_data
created_at
```

Relationship:

```text
user_id → users.id
```

---

## notifications

Stores user-specific notifications.

Main fields:

```text
id
user_id
title
message
is_read
created_at
```

Relationship:

```text
user_id → users.id
```

---

# 16. API Response Format

The application uses a standardized API response format.

Successful response:

```json
{
    "code": 200,
    "status": "Success",
    "message": "Request successful",
    "data": {}
}
```

Error response:

```json
{
    "code": 400,
    "status": "Error",
    "message": "Request failed",
    "data": null
}
```

This standard response structure is implemented through the application's response utilities.

---

# 17. Error Handling

The application provides centralized exception handling for:

* HTTP exceptions
* Validation errors
* Unexpected server errors

Common HTTP responses include:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity
500 Internal Server Error
```

Validation errors are handled centrally and returned using the standard API response structure.

---

# 18. API Documentation

Swagger UI is available through FastAPI's automatic OpenAPI documentation.

Run the application and open:

```text
http://127.0.0.1:8000/docs
```

Alternative OpenAPI documentation:

```text
http://127.0.0.1:8000/redoc
```

---

# 19. Project Structure

The project follows a modular FastAPI architecture.

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
│   │   ├── responses.py
│   │   └── ...
│   │
│   ├── models/
│   │   ├── users.py
│   │   ├── roles.py
│   │   ├── permissions.py
│   │   ├── role_permissions.py
│   │   ├── customers.py
│   │   ├── leads.py
│   │   ├── customer_activities.py
│   │   ├── follow_ups.py
│   │   ├── audit_logs.py
│   │   └── notifications.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── customers.py
│   │   ├── leads.py
│   │   ├── permissions.py
│   │   ├── customer_activities.py
│   │   ├── follow_ups.py
│   │   ├── audit_logs.py
│   │   └── notifications.py
│   │
│   ├── schemas/
│   │   ├── users.py
│   │   ├── customers.py
│   │   ├── leads.py
│   │   ├── customer_activities.py
│   │   ├── follow_ups.py
│   │   ├── audit_logs.py
│   │   └── notifications.py
│   │
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── ...
│
├── pytest.ini
├── alembic.ini
├── requirements.txt
├── .env
└── README.md
```

---

# 20. Environment Setup

## Step 1 — Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project directory:

```bash
cd TASK-3
```

---

## Step 2 — Create Virtual Environment

Windows:

```powershell
python -m venv SMS_venv
```

Activate:

```powershell
SMS_venv\Scripts\activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>/<database>

SECRET_KEY=<your-secret-key>

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

SMTP_HOST=<smtp-host>

SMTP_PORT=<smtp-port>

SMTP_USERNAME=<smtp-username>

SMTP_PASSWORD=<smtp-password>

FROM_EMAIL=<sender-email>
```

Never commit real passwords, secrets, database credentials, or SMTP credentials to GitHub.

---

# 21. Database Setup

The project uses PostgreSQL/Neon.

Configure the database connection using:

```env
DATABASE_URL=...
```

Run Alembic migrations:

```bash
alembic upgrade head
```

The database contains the CRM tables and their required relationships.

---

# 22. Run the Application

Start FastAPI using:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 23. API Testing

The project includes a structured Postman Collection covering the application's API modules.

Testing was performed for:

* Authentication
* Customer APIs
* Lead APIs
* RBAC
* Permission checks
* Customer Activities
* Follow-ups
* Notifications
* Audit Logs
* Validation
* Error handling
* Pagination
* Filtering
* Sorting
* Search
* Soft delete behavior
* Email notification workflow

The APIs were verified manually through Postman during the final project verification phase.

---

# 24. Pytest API Testing — Bonus Task 3

Pytest API automation was started as part of Bonus Task 3.

The test environment was configured with:

```text
pytest.ini
conftest.py
SQLite test database
```

The intended automated test coverage includes:

* Authentication
* Customer APIs
* Lead APIs
* Permission APIs

The Pytest implementation was partially completed and is currently deferred.

Manual API verification through the structured Postman Collection was completed for the implemented CRM modules.

Therefore:

```text
Bonus Task 3 – Pytest API Testing
Status: Partially completed / Deferred
```

The existing Pytest setup can be extended in the future to achieve complete automated test coverage.

---

# 25. Postman Verification Strategy

The final verification process followed this sequence:

```text
Authentication
      ↓
Registration
      ↓
Login
      ↓
JWT Verification
      ↓
Customers + RBAC
      ↓
Leads + RBAC
      ↓
Lead Assignment
      ↓
Notifications
      ↓
Audit Logs
      ↓
Customer Activities
      ↓
Customer Timeline
      ↓
Follow-ups
      ↓
Follow-up Status
      ↓
Background Processing
      ↓
Email Notifications
```

The APIs were verified both individually and through cross-module workflows.

---

# 26. End-to-End CRM Workflow

## Lead Workflow

```text
User Login
    ↓
Create Lead
    ↓
Assign Lead
    ↓
Notification Generated
    ↓
Assigned User Receives Notification
    ↓
Update Lead
    ↓
Audit Log Created
    ↓
Delete Lead
    ↓
Soft Delete
    ↓
Audit Log Created
```

## Customer Engagement Workflow

```text
Customer Created
    ↓
Create Activity
    ↓
Activity Added to Timeline
    ↓
Create Follow-up
    ↓
Follow-up Becomes Due
    ↓
Background Scheduler Detects Follow-up
    ↓
Email Reminder Sent
    ↓
reminder_sent_at Updated
```

---

# 27. Security Verification

The following security scenarios were verified:

```text
Valid JWT
    → Protected API Access

No JWT
    → 401 Unauthorized

Invalid JWT
    → 401 Unauthorized

Valid JWT + Missing Permission
    → 403 Forbidden

Valid JWT + Required Permission
    → Access Granted
```

RBAC was verified alongside Customer and Lead API testing.

---

# 28. Deliverables

The final project deliverables include:

### 1. Source Code

GitHub repository containing the complete FastAPI project.

### 2. Database

* ER Diagram
* Database Schema
* Database relationship documentation

### 3. API Documentation

Swagger/OpenAPI:

```text
/docs
```

### 4. Testing

* Postman Collection
* Manual API verification
* RBAC verification
* Permission verification

### 5. Documentation

This `README.md` contains:

* Installation Steps
* Environment Setup
* Database Setup
* API Usage
* Project Architecture
* Database Overview
* Testing Strategy
* Feature Documentation

---

# 29. Project Verification Status

| Module                        | Status                         |
| ----------------------------- | ------------------------------ |
| User Registration             | Completed                      |
| JWT Login                     | Completed                      |
| Authentication Verification   | Completed                      |
| Roles                         | Completed                      |
| Permissions                   | Completed                      |
| RBAC                          | Completed                      |
| Customer CRUD                 | Completed                      |
| Customer Search               | Completed                      |
| Customer Filtering            | Completed                      |
| Customer Pagination           | Completed                      |
| Customer Sorting              | Completed                      |
| Customer Soft Delete          | Completed                      |
| Lead CRUD                     | Completed                      |
| Lead Search                   | Completed                      |
| Lead Filtering                | Completed                      |
| Lead Sorting                  | Completed                      |
| Lead Pagination               | Completed                      |
| Lead Assignment               | Completed                      |
| Lead Soft Delete              | Completed                      |
| Customer Activities           | Completed                      |
| Customer Timeline             | Completed                      |
| Follow-up Management          | Completed                      |
| Follow-up Filtering           | Completed                      |
| Follow-up Status Management   | Completed                      |
| Notifications                 | Completed                      |
| Audit Logging                 | Completed                      |
| Background Processing         | Completed                      |
| Email Notifications           | Completed                      |
| Postman API Verification      | Completed                      |
| ER Diagram                    | Completed                      |
| Database Schema Documentation | Completed                      |
| DFD                           | Completed                      |
| Pytest API Automation         | Partially Completed / Deferred |

---

# 30. Future Improvements

Potential future improvements include:

* Complete Pytest automation for all required modules
* Increase automated test coverage
* Add CI/CD pipeline
* Add Docker support
* Add Redis/Celery-based distributed background processing
* Add richer CRM reporting dashboards
* Add advanced lead workflow automation
* Add email templates
* Add email delivery tracking
* Add notification preferences
* Add refresh token support
* Add rate limiting
* Add production-grade logging and monitoring

---

# 31. Conclusion

This project extends the CRM foundation from Task 2 into a more complete CRM backend system focused on lead management and sales workflow automation.

The implementation includes:

```text
FastAPI
+ PostgreSQL / Neon
+ SQLAlchemy
+ JWT Authentication
+ RBAC
+ Permission Management
+ Customer Management
+ Lead Management
+ Lead Assignment
+ Customer Activity Timeline
+ Follow-up Management
+ Notifications
+ Audit Logging
+ Background Processing
+ Email Notifications
+ Postman API Testing
```

The project has been manually verified through the major CRM workflows and API modules.

The remaining deferred item is the completion of the full automated Pytest API test suite under Bonus Task 3.

---

# 32. Final Status

```text
CRM Task 3
        ↓
Core API Development      ✅
Authentication             ✅
Authorization / RBAC       ✅
Customer Management        ✅
Lead Management            ✅
Activity Timeline          ✅
Follow-up Management       ✅
Notifications              ✅
Audit Logging              ✅
Background Processing      ✅
Email Notifications        ✅
Database Documentation     ✅
ER Diagram                 ✅
DFD                        ✅
Postman Verification       ✅
README Documentation       ✅
Pytest Automation          ⏸️ Deferred
```

**Project Status: Core Task 3 implementation and verification completed.**
