from fastapi import FastAPI

from app.core.database import Base, engine
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



Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CRM Task 3 API",
    description="CRM System Enhancement - Lead Management Module",
    version="1.0.0",
)


app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(permissions.router)
app.include_router(leads_router)
app.include_router(audit_logs_router)
app.include_router(customer_activities.router)
app.include_router(follow_ups_router)
app.include_router(notifications_router)


@app.get("/")
def root():
    return {
        "message": "CRM Task 3 API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }