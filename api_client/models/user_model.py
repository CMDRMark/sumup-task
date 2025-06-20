import random
from typing import Optional

from pydantic import BaseModel, Field

from api_client.models.bank_account_creation_models import BankAccountCreationInfoModel
from api_client.models.bank_account_model import BankAccount


class User(BaseModel):
    username: str
    password: str
    token: Optional[str] = Field(default=None)
    id: int = Field(default=None)
    bank_accounts: dict[str, BankAccount] = Field(default_factory=dict)
    bank_account_creation_info: BankAccountCreationInfoModel = Field(default_factory=dict)

    def to_dict(self):
        return {"username": self.username,
                "password": self.password,
                "id": self.id,
                "bank_accounts": self.bank_accounts,
                "bank_account_creation_info": self.bank_account_creation_info
                }

    def get_random_bank_account_id(self) -> Optional[int]:
        if self.bank_accounts:
            return random.choice(list(self.bank_accounts.keys()))
        return None

    def get_random_bank_account_info(self) -> Optional[BankAccount]:
        bank_account_id = random.choice(list(self.bank_accounts.keys()))
        return BankAccount.model_validate(self.bank_accounts.get(bank_account_id))

    def get_bank_account_info_by_id(self, bank_account_id: str) -> Optional[BankAccount]:
        return BankAccount.model_validate(self.bank_accounts.get(bank_account_id))
