from dataclasses import dataclass

from requests import Response

from api_clients_and_models.auth_api_client import AuthAPIClient
from api_clients_and_models.models.user_model import User
from utils.custom_requests import post_request, get_request


# TODO: no versioning in the api endpoints/headers
# TODO: In the signup endpoint possible issue 2 /api/


@dataclass
class AccountEndpoints:
    base_url: str

    @property
    def create_bank_account(self) -> str:
        return f"{self.base_url}/api/accounts"

    @property
    def get_bank_account(self) -> str:
        return f"{self.base_url}/api/accounts/ID"


class BAMAPIClient:
    def __init__(self, base_url: str):
        self.urls = AccountEndpoints(base_url)
        self.headers: dict = {"Content-Type": "application/json"}

    def create_bank_account_request(self, first_name: str = None, last_name: str = None, date_of_birth: str = None, initial_deposit: int = None,
                                    token: str = None, user: User = None) -> Response:
        headers = self.headers.copy()

        if token or user.token:
            headers["X-API-KEY"] = token or user.token

        payload = {
            "first_name": first_name or user.bank_account_creation_info.first_name,
            "last_name": last_name or user.bank_account_creation_info.last_name,
            "date_of_birth": date_of_birth or user.bank_account_creation_info.date_of_birth,
            "initial_deposit": initial_deposit or user.bank_account_creation_info.initial_deposit
        }

        resp = post_request(url=self.urls.create_bank_account, headers=headers,
                            json=payload, verify=False)

        return resp

    def get_bank_account_id_request(self, user: User = None, bank_account_id: str = None, token: str = None) -> Response:
        headers = self.headers.copy()
        headers["X-API-KEY"] = token or user.token

        resp = get_request(url=self.urls.get_bank_account.replace("ID", bank_account_id), headers=self.headers,
                            verify=False)
        return resp
