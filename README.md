# SumUp Bank Account Automation Suite

## Overview

This project provides a robust, extensible, and maintainable automation suite for validating the bank account creation flow of the SumUp QA challenge. It is designed for easy configuration, clear reporting, and seamless extension as requirements evolve.

---

## System Architecture

Below is a UML-style class diagram (Mermaid) showing the relationships between API clients, core application models, and test-specific data models.

```mermaid
classDiagram
    direction LR

    package "Core Application Models" {
        class User {
            +username: str
            +password: str
            +token: Optional[str]
            +bank_accounts: dict~BankAccount~
            +bank_account_creation_info: BankAccountCreationInfoModel
        }

        class BankAccount {
            +id: int
            +full_name: str
            +iban: Optional[str]
        }

        class BankAccountCreationInfoModel {
            +first_name: str
            +last_name: str
            +date_of_birth: str
        }

        class BankAccountInfoResponseModel {
            +id: int
            +full_name: str
            +iban: Optional[str]
            +to_bank_account(): BankAccount
        }
    }

    package "API Clients" {
        class BAMAPIClient {
            +create_bank_account(user: User)
        }
        class AuthAPIClient {
            +login_user_request(user: User)
        }
    }

    package "Test Infrastructure" {
        class InvalidAccountScenario {
            +first_name: str
            +last_name: str
            +date_of_birth: str
            +expected_status_code: int
            +expected_error: str
        }
        note for InvalidAccountScenario "Structures parameterized test data for invalid account creation tests."
    }

    ' Relationships
    BAMAPIClient ..> User : "uses for request"
    BAMAPIClient ..> BankAccountInfoResponseModel : "returns"
    AuthAPIClient ..> User : "uses for request"

    User "1" *-- "1" BankAccountCreationInfoModel : "holds"
    User "1" *-- "0..*" BankAccount : "holds"

    BankAccountInfoResponseModel ..> BankAccount : "creates"

    ' Test-specific relationship (conceptual)
    InvalidAccountScenario --o BankAccountCreationInfoModel : "provides data for"
```

### How to read this diagram:
-   **Packages:** The components are grouped into `Core Application Models`, `API Clients`, and `Test Infrastructure` to clarify their roles.
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