from pydantic import ValidationError
from requests import Response
from typing import Type

from api_client.models.response_validation_model import ResponseValidationResult, T


def assert_response_schema(
    model: Type[T],
    response: Response,
    expected_status: int = 200
) -> ResponseValidationResult[T]:
    errors: list[str] = []
    parsed: T | None = None

    if response.status_code != expected_status:
        errors.append(
            f"HTTP status code {response.status_code} is not equal to expected status {expected_status}"
        )

    try:
        parsed = model.model_validate(response.json())
    except ValidationError as e:
        errors.append(
            f"Server response does not match {model.__name__} schema:\n{e}\nRaw response: {response.text}"
        )

    return ResponseValidationResult(data=parsed, errors=errors)
