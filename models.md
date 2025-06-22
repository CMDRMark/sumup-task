```mermaid
classDiagram
    class BankAccount {
        int id
        str first_name
        str last_name
        str full_name
        str date_of_birth
        float initial_deposit
        str iban_issuance_status
        str created_at
        str updated_at
        str iban
    }
    class BankAccountCreationInfoModel {
        str first_name
        str last_name
        str date_of_birth
        int initial_deposit
    }
    class BankAccountInfoResponseModel {
        int id
        str first_name
        str last_name
        str date_of_birth
        float initial_deposit
        str full_name
        str iban_issuance_status
        str iban
        str created_at
        str updated_at
    }
    class User {
        str username
        str password
        str token
        int id
        dict~str, BankAccount~ bank_accounts
        BankAccountCreationInfoModel bank_account_creation_info
    }
    class RegistrationResponse {
        int id
        str username
    }
    class UnauthorizedResponseModel {
        str timestamp
        int status
        str error
        str message
        str path
    }
    class LoginResponseModel {
        str api_key
        datetime expires_at
    }
    User --> BankAccount
    User --> BankAccountCreationInfoModel
    BankAccountInfoResponseModel --> BankAccount
    BankAccountInfoResponseModel --> BankAccountCreationInfoModel
