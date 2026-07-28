from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.responses import error_response


# =========================================================
# HTTP EXCEPTION HANDLER
# Handles:
# 400
# 401
# 403
# 404
# 405
# 409
# etc.
# =========================================================

async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=str(exc.detail),
            code=exc.status_code,
            data=None
        )
    )


# =========================================================
# VALIDATION ERROR HANDLER
# Handles:
# 422 Unprocessable Entity
# =========================================================

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content=error_response(
            message="Validation error",
            code=422,
            data={
                "errors": exc.errors()
            }
        )
    )


# =========================================================
# GLOBAL UNHANDLED EXCEPTION HANDLER
# Handles:
# 500 Internal Server Error
# =========================================================

async def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content=error_response(
            message="Internal server error",
            code=500,
            data=None
        )
    )

