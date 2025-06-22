# SumUp Bank Account Automation Suite

## Overview

This project provides a robust, extensible, and maintainable automation suite for validating the bank account creation flow of the SumUp QA challenge. It is designed for easy configuration, clear reporting, and seamless extension as requirements evolve.

---

## System Architecture

Below you can find UML-style class diagrams (Mermaid) showing the relationships between API clients, core application models, and test-specific data models.

[API clients and User relation.md](API%20clients%20and%20User%20relation.md)  
[Test parametrization logic.md](Test%20parametrization%20logic.md)  
[Full models relations.md](Full%20models%20relations.md)

## Setup & Execution

### Prerequisites
- Python 3.11+ or Docker

## Local run

### Installation
1. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running Tests
-   **Run all tests:**
    ```bash
    pytest .
    ```
## Dockerized run 

### Create an image
1. **Build the Docker image:**
    ```bash
    docker build -t sumup-bank-account-tests .
    ```
2. **Run the Docker container:**
    ```bash
    docker run --rm -v $(pwd):/app sumup-bank-account-tests
    ```
### Report 
By default, test suite generates an HTML report in the [output](output) directory. You can view it by opening [report.html](output/report.html) in your browser.

#### Available pytest cli arguments:  
-   `--env`: Specify the environment (e.g., `LOCAL`, `DEV`, `TEST`, `STAGING`, `PROD`).
-   `--save-registered-users`: Save newly created users/bank accounts to [registered_users](test_data/registered_users) for the specified environment.
-   `--hide-secrets`: Hide sensitive information in test reports (e.g., API keys, passwords).

## Configuration
The test suite can be configured for different environments.

- **Base URL:** Set in [conftest.py](conftest.py).
- **Base URL mapping:** Defined in [url_mapping.py](api_clients_and_models/url_mapping.py) for each environment.
- **Pytest configs:** Configured in [pytest.ini](pytest.ini) for test discovery, execution parameters and reporting. 

## Test Data Management
- **API Key:** Handled automatically upon user login.
- **User Accounts:** Created during test execution or loaded from environment-specific files in [registered_users](test_data/registered_users).
- **Test Data For Test Parametrization:** Stored in [invalid_data](test_data/invalid_data).



## Known Issues & TODOs
-   **Bug:** The API returns a `411 Length Required` status code for some invalid account creation requests instead of a more appropriate `400 Bad Request`. This is noted in `test_create_bank_account_with_invalid_data`.
-   **TODO:** Implement logic to separately verify the `initial_deposit` calculation, as its value in the response may differ from the request due to backend processing.
-   **TODO:** Enhance the test reports with more detailed context for failures.