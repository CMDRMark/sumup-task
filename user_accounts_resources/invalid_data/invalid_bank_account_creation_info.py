import datetime
from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional, Any


@dataclass
class InvalidAccountScenario:
    """Represents a single invalid account creation scenario."""
    first_name: Optional[Any]
    last_name: Optional[Any]
    date_of_birth: Optional[Any]
    initial_deposit: Optional[Any]
    expected_status_code: HTTPStatus
    expected_error: str


invalid_first_names = {
    "Empty First Name": InvalidAccountScenario("", "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name cannot be empty."),
    "Over 50 Characters First Name": InvalidAccountScenario("a" * 51, "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Full name must be less than 50 characters"),
    "Over 50 Characters First Name with Spaces": InvalidAccountScenario("a" * 49 + " ", "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Full name must be less than 50 characters"),
    "Over 50 Characters First Name with Last Name": InvalidAccountScenario("a" * 47, "Smith", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Full name must be less than 50 characters"),
    "Spaces for First Name": InvalidAccountScenario("     ", "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name cannot be empty."),
    "Double First Name": InvalidAccountScenario("John Martin", "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name cannot contain spaces."),
    "First Name with Extra Spaces": InvalidAccountScenario("John   ", "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name cannot have trailing spaces."),
    "Numeric First Name": InvalidAccountScenario("12345", "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name must be a string."),
    "Integer First Name": InvalidAccountScenario(12345, "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name must be a string."),
    "Special Characters in First Name": InvalidAccountScenario("!@#$%", "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name must be a string."),
    "Boolean First Name": InvalidAccountScenario(True, "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name must be a string."),
    "None First Name": InvalidAccountScenario(None, "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name cannot be null."),
    "List First Name": InvalidAccountScenario(["John"], "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name must be a string."),
    "Dict First Name": InvalidAccountScenario({"name": "John"}, "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name must be a string."),
    "SQL Injection First Name": InvalidAccountScenario("'; DROP TABLE users; --", "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name must be a string."),
    "XSS First Name": InvalidAccountScenario("<script>alert('XSS');</script>", "Doe", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "First name must be a string.")
}

invalid_last_names = {
    "Empty Last Name": InvalidAccountScenario("John", "", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name cannot be empty."),
    "Spaces for Last Name": InvalidAccountScenario("John", "     ", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name cannot be empty."),
    "Double Last Name": InvalidAccountScenario("John", "Doe Smith", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name cannot contain spaces."),
    "Last Name with Extra Spaces": InvalidAccountScenario("John", "Doe   ", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name cannot have trailing spaces."),
    "Numeric Last Name": InvalidAccountScenario("John", "12345", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name must be a string."),
    "Integer Last Name": InvalidAccountScenario("John", 12345, "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name must be a string."),
    "Special Characters in Last Name": InvalidAccountScenario("John", "!@#$%", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name must be a string."),
    "Boolean Last Name": InvalidAccountScenario("John", True, "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name must be a string."),
    "None Last Name": InvalidAccountScenario("John", None, "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name cannot be null."),
    "List Last Name": InvalidAccountScenario("John", ["Doe"], "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name must be a string."),
    "Dict Last Name": InvalidAccountScenario("John", {"name": "Doe"}, "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name must be a string."),
    "SQL Injection Last Name": InvalidAccountScenario("John", "'; DROP TABLE users; --", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name must be a string."),
    "XSS Last Name": InvalidAccountScenario("John", "<script>alert('XSS');</script>", "1990-01-01", 1000, HTTPStatus.BAD_REQUEST, "Last name must be a string.")
}

invalid_initial_deposits = {
    "Negative Initial Deposit": InvalidAccountScenario("John", "Doe", "1990-01-01", -1000, HTTPStatus.BAD_REQUEST, "Initial deposit must be a non-negative number."),
    "Zero Initial Deposit": InvalidAccountScenario("John", "Doe", "1990-01-01", 0, HTTPStatus.BAD_REQUEST, "Initial deposit must be a non-negative number."),
    "String Initial Deposit": InvalidAccountScenario("John", "Doe", "1990-01-01", "1000", HTTPStatus.BAD_REQUEST, "Initial deposit must be a number."),
    "Boolean Initial Deposit": InvalidAccountScenario("John", "Doe", "1990-01-01", True, HTTPStatus.BAD_REQUEST, "Initial deposit must be a number."),
    "None Initial Deposit": InvalidAccountScenario("John", "Doe", "1990-01-01", None, HTTPStatus.BAD_REQUEST, "Initial deposit cannot be null."),
    "List Initial Deposit": InvalidAccountScenario("John", "Doe", "1990-01-01", [1000], HTTPStatus.BAD_REQUEST, "Initial deposit must be a number."),
    "Dict Initial Deposit": InvalidAccountScenario("John", "Doe", "1990-01-01", {"amount": 1000}, HTTPStatus.BAD_REQUEST, "Initial deposit must be a number."),
    "SQL Injection Initial Deposit": InvalidAccountScenario("John", "Doe", "1990-01-01", "'; DROP TABLE users; --", HTTPStatus.BAD_REQUEST, "Initial deposit must be a number."),
    "XSS Initial Deposit": InvalidAccountScenario("John", "Doe", "1990-01-01", "<script>alert('XSS');</script>", HTTPStatus.BAD_REQUEST, "Initial deposit must be a number.")
}


invalid_date_of_birth = {
    "Empty Date of Birth": InvalidAccountScenario("John", "Doe", "", 1000, HTTPStatus.BAD_REQUEST, "Date of birth cannot be empty."),
    "Invalid Date Format": InvalidAccountScenario("John", "Doe", "01-01-1990", 1000, HTTPStatus.BAD_REQUEST, "Date of birth must be in YYYY-MM-DD format."),
    "Future Date of Birth": InvalidAccountScenario("John", "Doe", "2050-01-01", 1000, HTTPStatus.BAD_REQUEST, "Date of birth cannot be in the future."),
    "Less Than 18 Years Old": InvalidAccountScenario("John", "Doe", datetime.datetime.today().year - 17, 1000, HTTPStatus.BAD_REQUEST, "Account holder must be at least 18 years old"),
    "String Date of Birth": InvalidAccountScenario("John", "Doe", "January 1, 1990", 1000, HTTPStatus.BAD_REQUEST, "Date of birth must be in YYYY-MM-DD format."),
    "Boolean Date of Birth": InvalidAccountScenario("John", "Doe", True, 1000, HTTPStatus.BAD_REQUEST, "Date of birth must be a string."),
    "None Date of Birth": InvalidAccountScenario("John", "Doe", None, 1000, HTTPStatus.BAD_REQUEST, "Date of birth cannot be null."),
    "List Date of Birth": InvalidAccountScenario("John", "Doe", ["1990-01-01"], 1000, HTTPStatus.BAD_REQUEST, "Date of birth must be a string."),
    "Dict Date of Birth": InvalidAccountScenario("John", "Doe", {"date": "1990-01-01"}, 1000, HTTPStatus.BAD_REQUEST, "Date of birth must be a string."),
    "SQL Injection Date of Birth": InvalidAccountScenario("John", "Doe", "'; DROP TABLE users; --", 1000, HTTPStatus.BAD_REQUEST, "Date of birth must be a string."),
    "XSS Date of Birth": InvalidAccountScenario("John", "Doe", '<script>alert("XSS");</script>', 1000, HTTPStatus.BAD_REQUEST, "Date of birth must be a string.")
}

invalid_bank_account_creation_info = {
    **invalid_first_names,
    **invalid_last_names,
    **invalid_initial_deposits,
    **invalid_date_of_birth,
    "Empty Bank Account Creation Info": InvalidAccountScenario(None, None, None, None, HTTPStatus.BAD_REQUEST, "Bank account creation info cannot be empty."),
}
