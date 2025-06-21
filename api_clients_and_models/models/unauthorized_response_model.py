from pydantic import BaseModel, field_validator


class UnauthorizedResponseModel(BaseModel):
    timestamp: str
    status: int
    error: str
    message: str
    path: str

    @field_validator("timestamp", "error", "message", "path")
    def fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field must not be empty")
        return value

    @field_validator("status")
    def status_code_must_be_403(cls, value: int) -> int:
        if value != 403:
            raise ValueError("Status code must be 403 for unauthorized responses")
        return value

    @field_validator("message")
    def message_must_be_access_denied(cls, value: str) -> str:
        if value != "Access Denied":
            raise ValueError("Message must be 'Access Denied' for unauthorized responses")
        return value

    @field_validator("error")
    def error_must_be_forbidden(cls, value: str) -> str:
        if value != "Forbidden":
            raise ValueError("Error must be 'Forbidden' for unauthorized responses")
        return value
