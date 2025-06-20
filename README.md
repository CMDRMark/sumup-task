# SumUp Bank Account Automation Suite

## Overview

This project provides a robust, extensible, and maintainable automation suite for validating the bank account creation flow of the SumUp QA challenge. It is designed for easy configuration, clear reporting, and seamless extension as requirements evolve.

---

## System Architecture

Below is a UML-style class diagram (Mermaid) showing the relationships between API clients, models, and their interactions:

```mermaid
classDiagram
    %% Models
    class User {
        +username: str
        +password: str
        +token: Optional[str]
        +id: int
        +bank_accounts: dict[str, BankAccount]
        +bank_account_creation_info: BankAccountCreationInfoModel
        +to_dict()
        +get_random_bank_account_id()
        +get_random_bank_account_info()
        +get_bank_account_info_by_id()
    }

    class BankAccount {
        +id: int
        +first_name: str
        +last_name: str
        +full_name: str
        +date_of_birth: str
        +initial_deposit: float
        +iban_issuance_status: str
        +created_at: str
        +updated_at: str
        +iban: Optional[str]
        +to_dict()
        +diff()
    }

    class BankAccountCreationInfoModel {
        +first_name: Optional[str]
        +last_name: Optional[str]
        +date_of_birth: Optional[str]
        +initial_deposit: Optional[int]
        +to_dict()
    }

    class BankAccountInfoResponseModel {
        +id: int
        +first_name: str
        +last_name: str
        +date_of_birth: str
        +initial_deposit: float
        +full_name: str
        +iban_issuance_status: str
        +iban: Optional[str]
        +created_at: str
        +updated_at: str
        +to_bank_account(): BankAccount
    }

    class RegistrationResponse {
        +id: int
        +username: str
    }

    class LoginResponseModel {
        +api_key: str
        +expires_at: datetime
    }

    %% API Clients
    class AuthAPIClient {
        +register_user_request(user: User)
        +login_user_request(user: User)
    }

    class BAMAPIClient {
        +create_bank_account(user: User)
        +get_bank_account_id(user: User, bank_account_id: str)
    }

    %% Relationships
    User "1" o-- "*" BankAccount : bank_accounts
    User "1" o-- "1" BankAccountCreationInfoModel : bank_account_creation_info
    BankAccountInfoResponseModel "1" --> "1" BankAccount : to_bank_account()
    AuthAPIClient ..> User : uses
    AuthAPIClient ..> RegistrationResponse : returns
    AuthAPIClient ..> LoginResponseModel : returns
    BAMAPIClient ..> User : uses
    BAMAPIClient ..> BankAccountCreationInfoModel : uses (via User)
    BAMAPIClient ..> BankAccountInfoResponseModel : returns
```

**How to read this diagram:**  
- Solid lines (`o--`, `--`) show composition/aggregation (e.g., `User` has many `BankAccount`).
- Dashed lines (`..>`) show usage or return types (e.g., `AuthAPIClient` returns `RegistrationResponse`).
- Methods on models/clients are shown for key interactions.
- API Clients use models for requests and responses.

---

## [Add further sections here for: Setup, Running Tests, Configuration, Reporting, Known Issues, TODOs, etc.]
