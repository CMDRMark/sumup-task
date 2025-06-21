from pydantic import BaseModel, field_validator


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
