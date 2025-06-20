import json
from typing import Any, Callable
import requests

from utils.logger import logger


def log_request_response_info(func: Callable):

    def wrapper(*args, **kwargs):
        response: requests.Response = func(*args, **kwargs)

        logger.debug(f"Request URL: {response.url}")
        logger.debug(f"Request Method: {response.request.method}")

        headers = dict(response.request.headers)
        logger.debug(f"Request Headers:\n{json.dumps(headers, indent=2)}")

        body = response.request.body
        if isinstance(body, bytes):
            try:
                body_str = body.decode()
                body_json = json.loads(body_str)
                body_pretty = json.dumps(body_json, indent=2)
            except Exception:
                body_pretty = body.decode(errors="replace")
        else:
            body_pretty = str(body)

        logger.debug(f"Request Body:\n{body_pretty}")

        logger.debug(f"Response Status Code: {response.status_code}")

        response_headers = dict(response.headers)
        logger.debug(f"Response Headers:\n{json.dumps(response_headers, indent=2)}")

        try:
            response_json = response.json()
            response_pretty = json.dumps(response_json, indent=2)
        except Exception:
            response_pretty = response.text

        logger.debug(f"Response Body:\n{response_pretty}")

        return response

    return wrapper


@log_request_response_info
def get_request(url, headers=None, cookies=None, json=None, data=None, verify=False):
    return requests.get(url=url, headers=headers, cookies=cookies, json=json, data=data, verify=verify)


@log_request_response_info
def post_request(url, headers=None, cookies=None, json=None, data=None, verify=False):
    return requests.post(url=url, headers=headers, cookies=cookies, json=json, data=data, verify=verify)


@log_request_response_info
def delete_request(url, headers=None, cookies=None, json=None, data=None, verify=False):
    return requests.delete(url=url, headers=headers, cookies=cookies, json=json, data=data, verify=verify)


@log_request_response_info
def put_request(url, headers=None, cookies=None, json=None, data=None, verify=False):
    return requests.put(url=url, headers=headers, cookies=cookies, json=json, data=data, verify=verify)


@log_request_response_info
def options_request(url, headers=None, cookies=None, json=None, data=None, verify=False):
    return requests.options(url=url, headers=headers, cookies=cookies, json=json, data=data, verify=verify)