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
