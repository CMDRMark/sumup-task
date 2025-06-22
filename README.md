# SumUp Bank Account Automation Suite

## Overview

This project provides a robust, extensible, and maintainable automation suite for validating the bank account creation
flow of the SumUp QA challenge. It is designed for easy configuration, clear reporting, and seamless extension as
requirements evolve.

This framework uses API clients as objects to interact with the SumUp Bank Account API.

User is presented as a core model that interacts with API clients to perform actions like creating bank accounts,
retrieving account details.

Main test cases capture business logic of interaction of User with the API client.

---

## System Architecture

Below you can find UML-style class diagrams (Mermaid) showing the relationships between API clients, core application
models, and test-specific data models.

[API clients and User relation.md](API%20clients%20and%20User%20relation.md)  
[Test parametrization logic.md](Test%20parametrization%20logic.md)  
[Full models relations.md](Full%20models%20relations.md)

## Setup & Execution

### Prerequisites

- Python 3.11+ or Docker

## Local run

### Install Python 3.11

- **On macOS (with Homebrew)**

    ```bash
    brew install python@3.11
    brew link python@3.11 --force
    ```
- on **Ubuntu/Debian:**

    ```bash
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt update
    sudo apt install python3.11 python3.11-venv python3.11-dev -y
    ```
- on **Windows:**

  Download the installer from the [official Python website](https://www.python.org/downloads/release/python-3110/) and follow the installation instructions.

### Environment Setup

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

- **Run all tests:**
  ```bash
  pytest .
  ```

## Dockerized run

1. **Build the Docker image:**
    ```bash
    docker build -t sumup-bank-account-tests .
    ```
2. **Run the Docker container:**
   ```bash
    docker run --rm -v $(pwd):/app sumup-bank-account-tests --env=TEST --hide-secrets
    ```
   You can pass/replace pytest arguments as needed.

### Report

Regardless if you run the tests locally or inside a container, test suite generates an HTML report in
the [output](output) directory. You can view it by opening [report.html](output/report.html) in your browser.

#### Available pytest cli arguments:

- `--env`: Specify the environment (e.g., `LOCAL`, `DEV`, `TEST`, `STAGING`, `PROD`). `TEST` by default.
- `--save-registered-users`: Save newly created users/bank accounts to [registered_users](test_data/registered_users)
  for the specified environment. False by default.
- `--hide-secrets`: Hide sensitive information in test reports (e.g., API keys, passwords). False by default.

#### Implemented pytest markers:

- `@pytest.mark.prod_safe`: Marks tests that are safe to run in production environments. If --env=PROD is specified,
  only these tests will be executed and all the secrets will be hidden in logs (logic is implemented
  here [conftest.py](conftest.py))

## Configuration

As mentioned above, test run can be configured for different environments.

- **Base URL:** Set in [conftest.py](conftest.py).
- **Base URL mapping:** Defined in [url_mapping.py](api_clients_and_models/url_mapping.py) for each environment.
- **Pytest configs:** Configured in [pytest.ini](pytest.ini) for test discovery, execution parameters and reporting.

## Test Data Management

- **API Key:** Handled automatically upon user login.
- **User Accounts:** Created during test execution or loaded from environment-specific files
  in [registered_users](test_data/registered_users).
- **Test Data For Test Parametrization:** Stored in [invalid_data](test_data/invalid_data).

## Future Improvements

- **Enhance Test Coverage:** Add more test cases to cover edge cases and additional business logic.
- **Improve Error Handling:** Implement more robust error handling in API clients to gracefully manage unexpected responses.
- **Extend invalid response models:** Add more specific invalid response models to improve test coverage and error handling.
- **Performance Testing:** Implement performance tests to ensure the API can handle high loads. (needs to be implemented in the different repo to not mix python and performance testing)
  tools).
- **Collect feedback from QA Engineers:** Gather insights from QA engineers to identify test framework improvements ideas.
- **CI/CD Integration:** Integrate the test suite with CI/CD pipelines for automated testing on code changes.

## Known Issues and TODOs
### Check the issues here: [Bugs and Issues.md](Bugs%20and%20Issues.md)
