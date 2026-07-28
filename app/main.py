from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.database import Base, engine
from app.core.exception_handlers import (
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.core.responses import success_response

from app.background.scheduler import (
    start_scheduler,
    stop_scheduler,
)

from app.models import (
    Role,
    Permission,
    RolePermission,
    User,
    Customer,
)

from app.routers.auth import router as auth_router
from app.routers.customers import router as customer_router
from app.routers import permissions
from app.routers.leads import router as leads_router
from app.routers.audit_logs import router as audit_logs_router
from app.routers import customer_activities
from app.routers.follow_ups import router as follow_ups_router
from app.routers.notifications import router as notifications_router


# =========================================================
# APPLICATION LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Start background scheduler
    start_scheduler()

    yield

    # Stop background scheduler
    stop_scheduler()


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="CRM Task 3 API",
    description="CRM System Enhancement - Lead Management Module",
    version="1.0.0",
    lifespan=lifespan,
)


# =========================================================
# GLOBAL EXCEPTION HANDLERS
# =========================================================

# Handles HTTP errors:
# 400, 401, 403, 404, 405, 409, etc.
app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)


# Handles validation errors:
# 422 Unprocessable Entity
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)


# Handles unexpected server errors:
# 500 Internal Server Error
app.add_exception_handler(
    Exception,
    general_exception_handler,
)


# =========================================================
# DATABASE TABLE CREATION
# =========================================================

# Create database tables if they do not exist
Base.metadata.create_all(
    bind=engine
)


# =========================================================
# REGISTER ROUTERS
# =========================================================

app.include_router(
    auth_router
)

app.include_router(
    customer_router
)

app.include_router(
    permissions.router
)

app.include_router(
    leads_router
)

app.include_router(
    audit_logs_router
)

app.include_router(
    customer_activities.router
)

app.include_router(
    follow_ups_router
)

app.include_router(
    notifications_router
)


# =========================================================
# ROOT API
# =========================================================

@app.get("/")
def root():

    return success_response(
        data=None,
        message="CRM Task 3 API is running",
        code=200,
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():

    return success_response(
        data={
            "status": "healthy"
        },
        message="Health check successful",
        code=200,
    )
