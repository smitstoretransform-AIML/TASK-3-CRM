from typing import Any

from pydantic import BaseModel


class APIResponse(BaseModel):
    code: int
    status: str
    message: str
    data: Any = None


def success_response(
    data: Any = None,
    message: str = "Request successful",
    code: int = 200,
):
    return {
        "code": code,
        "status": "Success",
        "message": message,
        "data": data,
    }


def error_response(
    message: str = "Request failed",
    code: int = 400,
    data: Any = None,
):
    return {
        "code": code,
        "status": "Error",
        "message": message,
        "data": data,
    }