from pydantic import ValidationError
from requests import Response
from typing import Type, Union

from api_clients_and_models.models.response_validation_model import ResponseValidationResult, T


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


def assert_sent_information_equals_to_received_information(
    sent_info: dict,
    received_info: dict,
    exclude_fields: Union[list[str], str, None] = None
) -> bool:
    if exclude_fields:
        if isinstance(exclude_fields, list):
            exclude_fields = set(exclude_fields)
        else:
            exclude_fields = {exclude_fields}
    else:
        exclude_fields = set()

    common_keys = (set(sent_info.keys()) & set(received_info.keys())) - exclude_fields

    sent_info_filtered = {k: v for k, v in sent_info.items() if k in common_keys}
    received_info_filtered = {k: v for k, v in received_info.items() if k in common_keys}

    return sent_info_filtered == received_info_filtered

