from pydantic import BaseModel
from typing import Optional


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