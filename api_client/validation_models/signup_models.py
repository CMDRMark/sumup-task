from pydantic import BaseModel, field_validator
from datetime import datetime, timezone


class RegistrationResponse(BaseModel):
    id: int
    username: str

    @field_validator('id', mode="after")
    def id_must_be_positive(cls, value: int):
        if value <= 0:
            raise ValueError("id must be positive")
        return value

    @field_validator('username', mode='after')
    def username_must_be_not_empty(cls, value: str):
        if value.strip() == "":
            raise ValueError("username should not be empty")
        return value


class LoginResponseModel(BaseModel):
    api_key: str
    expires_at: datetime

    @field_validator("api_key", mode="after")
    def api_key_must_not_be_empty(cls, value: str) -> str:
        """
        Validate that apiKey is not empty.
        """
        if not value:
            raise ValueError("apiKey must not be empty")
        return value

    @field_validator("expires_at", mode="after")
    def expires_must_be_future(cls, value: datetime) -> datetime:
        """
        Validate that expires_at is ISO8601, handles 'Z',
        and is strictly in the future.
        """
        now = datetime.now(timezone.utc)
        if value <= now:
            raise ValueError(f"expires_at must be in the future. Got: {value.isoformat()}")
        return value
