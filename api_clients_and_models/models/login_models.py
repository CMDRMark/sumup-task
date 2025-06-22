from datetime import datetime, timezone
from pydantic import BaseModel, field_validator


class LoginResponseModel(BaseModel):
    api_key: str
    expires_at: datetime

    @field_validator("api_key", mode="after")
    def api_key_must_not_be_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("apiKey must not be empty")
        return value

    @field_validator("expires_at", mode="after")
    def expires_must_be_future(cls, value: datetime) -> datetime:
        now = datetime.now(timezone.utc)
        if value <= now:
            raise ValueError(f"expires_at must be in the future. Got: {value.isoformat()}")
        return value
