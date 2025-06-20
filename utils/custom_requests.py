import json
import os
from typing import Any, Callable
import requests

from utils.logger import logger


def log_request_response_info(func: Callable):

    def wrapper(*args, **kwargs):
        hide_secrets = os.getenv('HIDE_SECRETS')
        response: requests.Response = func(*args, **kwargs)

        logger.debug(f"Request URL: {response.url}")
        logger.debug(f"Request Method: {response.request.method}")

        headers = dict(response.request.headers)
        if "X-API-KEY" in headers and hide_secrets:
            headers["X-API-KEY"] = "***"
        logger.debug(f"Request Headers:\n{json.dumps(headers, indent=2)}")

        body = response.request.body
        if isinstance(body, bytes):
            try:
                body_str = body.decode()
                body_json = json.loads(body_str)
                if "password" in body_json and hide_secrets:
                    body_json["password"] = "***"
                body_pretty = json.dumps(body_json, indent=2)
            except Exception:
                body_pretty = body.decode(errors="replace")
        else:
            body_pretty = str(body)


        logger.debug(f"Request Body:\n{body_pretty}")

        logger.debug(f"Response Status Code: {response.status_code}")

        response_headers = dict(response.headers)
        if "x-api-key" in response_headers and hide_secrets:
            response_headers["x-api-key"] = "***"
        logger.debug(f"Response Headers:\n{json.dumps(response_headers, indent=2)}")

        try:
            response_json = response.json()
            if "api_key" in response_json and hide_secrets:
                response_json["api_key"] = "***"
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