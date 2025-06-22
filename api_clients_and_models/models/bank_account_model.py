import datetime

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Any


class BankAccount(BaseModel):
    id: int
    first_name: str
    last_name: str
    full_name: str
    date_of_birth: str
    initial_deposit: float
    iban_issuance_status: str
    created_at: str
    updated_at: str
    iban: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth,
            "initial_deposit": self.initial_deposit,
            "iban_issuance_status": self.iban_issuance_status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "iban": self.iban
        }

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented

        result = (
                self.id == other.id and
                self.first_name == other.first_name and
                self.last_name == other.last_name and
                self.full_name == other.full_name and
                self.date_of_birth == other.date_of_birth and
                self.initial_deposit == other.initial_deposit and
                self.created_at == other.created_at
        )

        iban_comp = True
        if self.iban and other.iban:
            iban_comp = self.iban == other.iban

        return result and iban_comp

    def diff(self, other) -> dict:
        if not isinstance(other, BankAccount):
            raise TypeError(f"Cannot diff BankAccount with {type(other)}")
        exclude_fields = {"updated_at", "iban_issuance_status"}
        if not self.iban:
            exclude_fields.add("iban")
        self_dict = self.model_dump(exclude=exclude_fields)
        other_dict = other.model_dump(exclude=exclude_fields)
        return {
            k: (self_dict[k], other_dict.get(k))
            for k in self_dict
            if self_dict[k] != other_dict.get(k)
        }

    def __sub__(self, other):
        return self.diff(other)


class BankAccountCreationInfoModel(BaseModel):
    first_name: Any = Field(default=None)
    last_name: Any = Field(default=None)
    date_of_birth: Any = Field(default=None)
    initial_deposit: Any = Field(default=None)

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "initial_deposit": self.initial_deposit
        }


class BankAccountInfoResponseModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: str
    initial_deposit: float
    full_name: str
    iban_issuance_status: str
    iban: Optional[str] = None
    created_at: str
    updated_at: str

    @field_validator("id", mode="after")
    def id_must_be_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("id must be a positive integer")
        return value

    @field_validator("first_name", "last_name", "full_name", mode="after")
    def names_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field must not be empty")
        return value

    @field_validator("date_of_birth", mode="after")
    def date_of_birth_must_be_valid(cls, value: str) -> str:
        try:
            dob = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("date_of_birth must be in the format YYYY-MM-DD")

        today = datetime.date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age < 18:
            raise ValueError("Person must be at least 18 years old")
        if age > 130:
            raise ValueError("Person must be less than 130 years old")
        return value

    @field_validator("iban_issuance_status", mode="after")
    def iban_issuance_status_must_be_valid(cls, value: str) -> str:
        valid_statuses = {"REQUESTED", "ISSUED", "REJECTED", "SUCCESSFUL", "FAILED"}
        if value not in valid_statuses:
            raise ValueError(f"iban_issuance_status must be one of {valid_statuses}")
        return value

    @field_validator("iban", mode="after")
    def iban_must_be_none_or_valid(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            if not value.isalnum():
                raise ValueError("iban must be a valid alphanumeric string")
            if not (15 <= len(value) <= 34):
                raise ValueError("iban must be between 15 and 34 characters long")
        return value

    @field_validator("created_at", "updated_at", mode="after")
    def datetime_must_be_iso8601(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("Must be in ISO8601 format")
        return value

    @model_validator(mode="after")
    def check_full_name(self):
        expected = f"{self.first_name} {self.last_name}"
        if self.full_name != expected:
            raise ValueError(f"full_name must be '{expected}'")
        return self

    def to_bank_account(self) -> BankAccount:
        return BankAccount(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            date_of_birth=self.date_of_birth,
            initial_deposit=self.initial_deposit,
            full_name=self.full_name,
            iban_issuance_status=self.iban_issuance_status,
            iban=self.iban,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    def __eq__(self, other):
        if not isinstance(other, BankAccountInfoResponseModel):
            return False
        iban_issuance_comp = False
        iban_comp = False
        result = self.id == other.id and self.first_name == other.first_name and self.last_name == other.last_name \
               and self.date_of_birth == other.date_of_birth and self.initial_deposit == other.initial_deposit \
               and self.full_name == other.full_name and self.created_at == other.created_at
        if self.iban and other.iban:
            iban_comp = self.iban == other.iban

        return all(x == True for x in (result, iban_issuance_comp, iban_comp))
