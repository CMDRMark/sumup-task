# Bugs, Issues & Missing Information

## General API Improvement Suggestions

- **Endpoint paths**  
  The signup endpoint is currently misconfigured as:  
  `/api/auth/api/signup`  
  A more appropriate path would be:  
  `/api/auth/signup`

- **Lack of API versioning**  
  Endpoints do not support versioning. Following the standard (e.g. `/api/v1/...`) makes future changes easier and helps with backward compatibility.

- **Insufficient error handling**  
  The API does not provide robust or descriptive error responses, making debugging and client error handling difficult.

---

## User Registration

- **Weak input validation**  
  Users can register with empty or whitespace-only usernames and passwords. This breaks standard login/registration test cases. Some tests were skipped to avoid polluting the overall test report.

- **Incorrect status code on success**  
  The API currently returns `200 OK` on successful registration. A more appropriate status would be `201 Created`.

---

## User Login

- **No response body on login failure**  
  Incorrect login credentials result in a response with no body. A proper error message should be returned.

- **Inconsistent response format**  
  API documentation describes fields like `apiKey` and `expiresAt` (camelCase), but the actual response uses `api_key` and `expires_at` (snake_case). Either the documentation or the implementation should be corrected.

- **Token format**  
  The API returns a UUID as a token. While this may be a limitation of the test server, a JWT would be more appropriate, allowing for payload validation and expiration decoding.

---

## Bank Account Creation

- **Unclear logic for initial deposit**  
  Creating an account with `initial_deposit = 1000` results in a balance of `999.9`, suggesting rounding or fees. More information is needed to validate this behavior.

- **Mismatched `created_at` timestamps**  
  The timestamp in the account creation response differs from the one returned by account retrieval. This could be a bug or undocumented logic.

- **Incorrect status code for long `full_name`**  
  When `full_name` exceeds 50 characters, the API returns `411 Length Required` instead of `400 Bad Request`.

- **Whitespace values are accepted**  
  Providing `first_name` or `last_name` as empty spaces returns a `200 OK` response. This input should be considered invalid.

- **Double names accepted**  
  Names like `Mary Jane` are accepted, which is correct behavior, but should be clarified in documentation.

- **No sanitization of whitespace**  
  Leading/trailing spaces in `first_name` and `last_name` are not trimmed by the server. The values are stored as-is, which is not ideal.

- **Non-string inputs are accepted**  
  Numeric values, booleans, and stringified numbers are accepted for `first_name` and `last_name`. Need clarification on whether this behavior is valid.

- **`initial_deposit` behavior unclear**  
  - Can be `0`: Not documented.
  - Can be negative: Likely a bug.
  - Can be a string: Handled correctly, but not documented.

- **`date_of_birth` allows unrealistic ages**  
  Users as old as 200 years can register. Age validation is missing.

---

## Bank Account Retrieval

- **Missing authentication enforcement**  
  Bank account info can be retrieved without passing an API token. This is a security issue.

- **Undocumented enum values**  
  Possible values for `iban_issuance_status` are not documented. This makes it difficult to write complete test cases.