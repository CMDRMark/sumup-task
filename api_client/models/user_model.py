import random
from typing import Optional

from pydantic import BaseModel, Field

from api_client.models.bank_account_model import BankAccount, BankAccountCreationInfoModel


class User(BaseModel):
    username: str
    password: str
    token: Optional[str] = Field(default=None)
    id: int = Field(default=None)
    bank_accounts: dict[str, BankAccount] = Field(default_factory=dict)
    bank_account_creation_info: BankAccountCreationInfoModel = Field(default_factory=dict)

    def to_dict(self):
        bank_account_creation_info = self.bank_account_creation_info
        if isinstance(self.bank_account_creation_info, BankAccountCreationInfoModel):
            bank_account_creation_info = self.bank_account_creation_info.to_dict()
        bank_accounts = {}
        for k, v in self.bank_accounts.items():
            if isinstance(v, BankAccount):
                bank_accounts[k] = v.to_dict()
            else:
                # If not a model instance, assume it's already a dict (for backward compatibility)
                bank_accounts[k] = v
        return {
            "username": self.username,
            "password": self.password,
            "token": self.token,
            "id": self.id,
            "bank_accounts": bank_accounts,
            "bank_account_creation_info": bank_account_creation_info
        }

    def bank_account_creation_info_is_empty(self) -> bool:
        """Returns True if all fields are None or empty."""
        return any(self.to_dict().values())

    def get_random_bank_account_id(self) -> Optional[int]:
        if self.bank_accounts:
            return int(random.choice(list(self.bank_accounts.keys())))
        return None

    def get_random_bank_account_info(self) -> Optional[BankAccount]:
        bank_account_id = random.choice(list(self.bank_accounts.keys()))
        return BankAccount.model_validate(self.bank_accounts.get(bank_account_id))

    def get_bank_account_info_by_id(self, bank_account_id: str) -> Optional[BankAccount]:
        return BankAccount.model_validate(self.bank_accounts.get(bank_account_id))
