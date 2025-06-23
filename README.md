# SumUp Bank Account Automation Suite

## Overview

This project provides a robust, extensible, and maintainable automation suite for validating the bank account creation
flow of the SumUp QA challenge. It is designed for easy configuration, clear reporting, and seamless extension as
requirements evolve.

This framework uses API clients as objects to interact with the SumUp Bank Account API.

User is presented as a core model that interacts with API clients to perform actions like creating bank accounts,
retrieving account details.

Main test cases capture business logic of interaction of User with the API client.

### Repository Structure

- `api_clients_and_models/`: Contains API client implementations and core application models.
- `test_data/`: Holds test data files, including registered users and invalid inputs for test parametrization.
- `tests/`: Contains test cases that validate the functionality of the API clients and models. Also includes a `conftest.py` file with fixtures specific to this level of testing.
- `tests/<service_folder>/`: Contains tests for a specific service or logical API unit. May include a local `conftest.py` for service-specific fixtures and hooks.
- `output/`: Stores test reports and other output files generated during test execution.
- `conftest.py`: Global configuration file for `pytest`, shared across all tests (located at the root of the project).
- `requirements.txt`: Lists Python dependencies required to run the tests.
- `pytest.ini`: Configuration file for `pytest`, defining test discovery rules, execution parameters, and reporting settings.
- `README.md`: Provides an overview of the project, setup instructions, and guidelines for running tests.

---

Pytest automatically discovers `conftest.py` files in the directory tree, applying fixtures and hooks based on location:

- The **root `conftest.py`** defines global fixtures shared across all tests.
- The **`tests/conftest.py`** is scoped to the `tests/` directory and its subfolders.
- Any **`conftest.py` inside a specific test folder** (e.g., `tests/service_x/conftest.py`) provides fixtures/hooks only to the tests within that folder.

This structure allows clear fixture scoping and modular test configuration.

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
#### Available pytest cli arguments:

- `--env`: Specify the environment (e.g., `LOCAL`, `DEV`, `TEST`, `STAGING`, `PROD`). `TEST` by default.
- `--save-registered-users`: Save newly created users/bank accounts to [registered_users](test_data/registered_users)
  for the specified environment. False by default.
- `--hide-secrets`: Hide sensitive information in test reports (e.g., API keys, passwords). False by default.

## Dockerized run
- **Build the Docker image:**
    ```bash
    docker build -t sumup-bank-account-tests .
    ```
- **Run the Docker container:**
   ```bash
    docker run --rm -v $(pwd):/app sumup-bank-account-tests --env=TEST --hide-secrets
    ```
   You can pass/replace pytest arguments as needed.

## Configuration

As mentioned above, test run can be configured for different environments.

- **Base URL:** Set in [conftest.py](conftest.py).
- **Base URL mapping:** Defined in [url_mapping.py](api_clients_and_models/url_mapping.py) for each environment.
- **Pytest configs:** Configured in [pytest.ini](pytest.ini) for test discovery, execution parameters and reporting.

#### Implemented pytest markers:

- `@pytest.mark.prod_safe`: Marks tests that are safe to run in production environments. If --env=PROD is specified,
  only these tests will be executed and all the secrets will be hidden in logs (logic is implemented
  here [conftest.py](conftest.py))

## Report

Regardless if you run the tests locally or inside a container, test suite generates an HTML report in
the [output](output) directory. You can view it by opening [report.html](output/report.html) in your browser.

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
- **Implement proper user credentials management:** Use secure vaults or secret management tools to handle sensitive information like API keys and user credentials.
- **Implement DB Validations**: Add database validations to ensure data integrity and consistency after API operations.
- **Implement more complex test scenarios:** Create tests that simulate real-world user interactions and workflows (e2e tests).

## Approach to extending the test suite

The main idea was to create a test suite that is easy to extend and maintain. This is achieved with a modular structure,
where each component has a clear responsibility and can be easily modified or replaced.

This is implemented by using API clients as objects that encapsulate the logic of interacting with the API, and core application models that represent the main entities in the system (e.g., User, BankAccount).
Response models are used to validate the responses from the API and ensure that they match the expected structure.
And test parametrization is done via simple data classes that define the expected input and output for each test case.

In order to extend the test suite you can modify/add API clients, extend the Response models, extend the User class with more information related to the user, introduce more parametrization by adding new data to the test data files.



## Test task caveats 
As I was testing the test suite on different machines I noticed, that users created on one machine, were not available, when tests were running on another machine. 

This might be the logic of test server, that's why some fixtures for getting registered users (with or without bank accounts) have a built-in logic to read the files and register new users on the fly.

Initially that was not the case, but to ensure that the tests will work on any machine, the registered users files will be empty. 

That's why some fixtures might have a bit too complicated logic due to the limitation of test server. 

Because of that some test data for invalid login/signup scenarios is stored in the [invalid_data](test_data/invalid_data) folder are not correct and need to be updated manually.

## Known Issues
### Check the issues here: [Bugs and Issues.md](Bugs%20and%20Issues.md)
