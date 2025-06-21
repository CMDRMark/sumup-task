# SumUp Bank Account Automation Suite

## Overview

This project provides a robust, extensible, and maintainable automation suite for validating the bank account creation flow of the SumUp QA challenge. It is designed for easy configuration, clear reporting, and seamless extension as requirements evolve.

---

## System Architecture

Below is a UML-style class diagram (Mermaid) showing the relationships between API clients, core application models, and test-specific data models.

```mermaid
classDiagram
    direction LR

    class LoginData {
        +username: str
        +password: str
    }

    class SignupData {
        +username: str
        +password: str
    }

    class User {
        +username: str
        +password: str
        +token: Optional~str~
        +id: Optional~int~
        +bank_accounts: dict of BankAccount
        +bank_account_creation_info: BankAccountCreationInfoModel
    }

    class BankAccountModel {
        +id: int
        +first_name: str
        +last_name: str
        +full_name: str
        +date_of_birth: str
        +initial_deposit: float
        +iban: Optional~str~
    }

    class BankAccountCreationInfoModel {
        +first_name: str
        +last_name: str
        +date_of_birth: str
        +initial_deposit: int
    }

    class BankAccountInfoResponseModel {
        +id: int
        +full_name: str
        +iban: Optional~str~
        +to_bank_account(): BankAccount
    }

    class BAMAPIClient {
        +create_bank_account(user: User)
        +get_bank_account_id(user: User, bank_account_id: str)
    }

    class AuthAPIClient {
        +register_user_request(user: User)
        +login_user_request(user: User)
    }

    class InvalidAccountScenario {
        +first_name: str
        +last_name: str
        +date_of_birth: str
        +initial_deposit: int
        +expected_status_code: int
        +expected_error: str
    }

    note for InvalidAccountScenario "Holds test data for invalid Bank account creation scenarios."

    %% Relationships
    BAMAPIClient ..> User : uses
    BAMAPIClient:create_bank_account ..> BankAccountCreationInfoModel : uses
    BAMAPIClient:get_bank_account_id ..> BankAccountInfoResponseModel : returns
    BAMAPIClient ..> AuthAPIClient : depends on
    
    AuthAPIClient ..> User : uses
    AuthAPIClient ..> LoginData : uses
    AuthAPIClient ..> SignupData : uses
    
    User "1" *-- "1" BankAccountCreationInfoModel : holds
    User "1" *-- "0..*" BankAccount : holds

    BankAccountInfoResponseModel ..> BankAccount : creates

%%    InvalidAccountScenario --o BankAccountCreationInfoModel : provides data
```

### How to read this diagram:
-   **Relationships:**
    -   `*--` (Composition): A `User` is composed of its `BankAccount`s.
    -   `..>` (Dependency/Uses): `BAMAPIClient` depends on `User` for making requests.
    -   `--o` (Aggregation): `InvalidAccountScenario` is used to provide data for creating `BankAccountCreationInfoModel` in tests.
-   **Notes:** Provide extra context, such as the purpose of the `InvalidAccountScenario` class.

---

## Setup & Execution

### Prerequisites
- Python 3.10+
- Pip (Python package installer)

### Installation
1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <repo-name>
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    *(Assuming you have a `requirements.txt` file)*
    ```bash
    pip install pytest pydantic requests
    ```

### Running Tests
-   **Run all tests:**
    ```bash
    pytest
    ```
-   **Run tests for a specific environment (e.g., TEST):**
    ```bash
    pytest --env=TEST
    ```
-   **Save newly created users to the data file:**
    ```bash
    pytest --save-new-user
    ```

## Configuration
The test suite can be configured for different environments (e.g., `TEST`, `STAGING`). Environment-specific parameters like the base URL are managed via fixtures that are selected by the `--env` command-line flag.

-   **Base URL:** Set in `tests/conftest.py`.
-   **API Key:** Handled automatically upon user login.
-   **Test Data:** Stored in `user_accounts_resources/` for each environment.

## Known Issues & TODOs
-   **Bug:** The API returns a `411 Length Required` status code for some invalid account creation requests instead of a more appropriate `400 Bad Request`. This is noted in `test_create_bank_account_with_invalid_data`.
-   **TODO:** Implement logic to separately verify the `initial_deposit` calculation, as its value in the response may differ from the request due to backend processing.
-   **TODO:** Enhance the test reports with more detailed context for failures.