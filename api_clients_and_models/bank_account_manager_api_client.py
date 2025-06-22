from dataclasses import dataclass

from requests import Response

from api_clients_and_models.models.user_model import User
from utils.custom_requests import post_request, get_request


@dataclass
class AccountEndpoints:
    """
    A dataclass to define bank account-related API endpoints.

    Attributes:
        base_url (str): The base URL for the API.
    """
    base_url: str

    @property
    def create_bank_account(self) -> str:
        """
        Constructs the endpoint URL for creating a bank account.

        Returns:
            str: The URL for the create bank account endpoint.
        """
        return f"{self.base_url}/api/accounts"

    @property
    def get_bank_account(self) -> str:
        """
        Constructs the endpoint URL for retrieving a bank account by ID.

        Returns:
            str: The URL for the get bank account endpoint.
        """
        return f"{self.base_url}/api/accounts/ID"


class BAMAPIClient:
    """
    A client for interacting with bank account-related API endpoints.

    Attributes:
        urls (AccountEndpoints): An instance of AccountEndpoints containing the API URLs.
        headers (dict): Default headers for API requests.
    """

    def __init__(self, base_url: str):
        """
        Initializes the BAMAPIClient with the base URL.

        Args:
            base_url (str): The base URL for the API.
        """
        self.urls = AccountEndpoints(base_url)
        self.headers: dict = {"Content-Type": "application/json"}

    def create_bank_account_request(self,
                                    first_name: str = None,
                                    last_name: str = None,
                                    date_of_birth: str = None,
                                    initial_deposit: int = None,
                                    token: str = None,
                                    user: User = None) -> Response:
        """
        Sends a request to create a new bank account.

        Args:
            first_name (str, optional): The first name of the account holder. Defaults to None.
            last_name (str, optional): The last name of the account holder. Defaults to None.
            date_of_birth (str, optional): The date of birth of the account holder. Defaults to None.
            initial_deposit (int, optional): The initial deposit amount. Defaults to None.
            token (str, optional): The authentication token. Defaults to None.
            user (User, optional): A User object containing account creation info and token. Defaults to None.

        Returns:
            Response: The HTTP response from the API.
        """
        headers = self.headers.copy()

        if token or user.token:
            headers["X-API-KEY"] = token or user.token

        payload = {
            "first_name": first_name or user.bank_account_creation_info.first_name,
            "last_name": last_name or user.bank_account_creation_info.last_name,
            "date_of_birth": date_of_birth or user.bank_account_creation_info.date_of_birth,
            "initial_deposit": initial_deposit or user.bank_account_creation_info.initial_deposit
        }

        resp = post_request(url=self.urls.create_bank_account,
                            headers=headers,
                            json=payload,
                            verify=False)

        return resp

    def get_bank_account_id_request(self,
                                    user: User = None,
                                    bank_account_id: str = None,
                                    token: str = None) -> Response:
        """
        Sends a request to retrieve a bank account by its ID.

        Args:
            user (User, optional): A User object containing the authentication token. Defaults to None.
            bank_account_id (str, optional): The ID of the bank account to retrieve. Defaults to None.
            token (str, optional): The authentication token. Defaults to None.

        Returns:
            Response: The HTTP response from the API.
        """
        headers = self.headers.copy()
        headers["X-API-KEY"] = token or user.token

        resp = get_request(url=self.urls.get_bank_account.replace("ID", bank_account_id),
                           headers=self.headers,
                           verify=False)
        return resp