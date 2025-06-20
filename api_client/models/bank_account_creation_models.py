from typing import Optional
from pydantic import BaseModel, Field

from api_client.models.bank_account_model import BankAccount


class BankAccountCreationInfoModel(BaseModel):
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    date_of_birth: Optional[str] = Field(default=None)
    initial_deposit: Optional[int] = Field(default=None)

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
        if self.iban_issuance_status != "REQUESTED":
            iban_issuance_comp = self.iban == other.iban
        if self.iban:
            iban_comp = self.iban == other.iban

        return all(x == True for x in (result, iban_issuance_comp, iban_comp))
