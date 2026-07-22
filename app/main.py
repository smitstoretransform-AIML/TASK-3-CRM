from fastapi import FastAPI

from app.core.database import Base, engine
from app.models import (
    Role,
    Permission,
    RolePermission,
    User,
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CRM Task 3 API",
    description="CRM System Enhancement - Lead Management Module",
    version="1.0.0",
)


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