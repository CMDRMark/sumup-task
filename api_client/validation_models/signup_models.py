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
            raise ValueError("id must be positive")
        return value


class LoginResponseModel(BaseModel):
    api_key: str
    expires_at: str

    @field_validator("api_key", mode="after")
    def api_key_must_not_be_empty(cls, value: str) -> str:
        """
        Validate that apiKey is not empty.
        """
        if not value:
            raise ValueError("apiKey must not be empty")
        return value

    @field_validator("expires_at", mode="after")
    def expires_must_be_future(cls, value: str) -> str:
        """
        Validate that expires_at is ISO8601, handles 'Z',
        and is strictly in the future.
        """
        raw = value

        # Remove Z if present
        if raw.endswith("Z"):
            raw = raw[:-1]

        # If nanoseconds present, trim to microseconds
        if "." in raw:
            date_part, frac_part = raw.split(".")
            frac_part = frac_part[:6]  # microseconds only
            raw = f"{date_part}.{frac_part}"

        try:
            dt = datetime.fromisoformat(raw)
        except Exception as e:
            raise ValueError(f"Invalid ISO timestamp: {value}") from e

        # Assume UTC
        dt = dt.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        if dt <= now:
            raise ValueError(f"expires_at must be in the future. Got: {dt.isoformat()}")

        return value
