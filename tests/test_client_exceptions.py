import re

from collections import namedtuple
from typing import Callable

import pytest

from ppa_api import client, create, exceptions, models

import common
import mock_responses


exception_map = namedtuple("exception_map", ["exception", "pattern"])
EXCEPTIONS = {
    "permission_denied": exception_map(
        exception=exceptions.PermissionDenied,
        pattern=re.compile(
            r"Forbidden \(403\)\. The user associated with the API key does not have the required revisions permissions\."
        ),
    ),
    "authentication_failed": exception_map(
        exception=exceptions.AuthenticationFailed,
        pattern=re.compile(
            r"Forbidden \(403\)\. Failed to authenticate to PPA using the supplied API key\."
        ),
    ),
    "request_error": exception_map(
        exception=exceptions.RequestError,
        pattern=re.compile(
            r"\(400\) Request to https://127.0.0.1/backend/v1/rest/revisions failed: Check the request data"
        ),
    ),
    "non_json_response": exception_map(
        exception=exceptions.InvalidResponse,
        pattern=re.compile(
            r"Unhandled Non-JSON Response \(200\)\. Response body: I am an unhandled non-JSON response\."
        ),
    ),
    "server_error": exception_map(
        exception=exceptions.ServerError,
        pattern=re.compile(
            r"Internal Server Error \(500\)\. Message: This is a server error message\. "
            r"Details: Something went wrong server-side\. Hint: Check the PPA logs\."
        ),
    ),
    "credits_required": exception_map(
        exception=exceptions.CreditsRequired,
        pattern=re.compile(
            r"Credits Required \(402\)\. Cannot start the task as there are 0 credits available\."
        ),
    ),
    "unhandled_request_error": exception_map(
        exception=exceptions.UnhandledRequestError,
        pattern=re.compile(r"Unhandled \(410\)\. Response body: Something really weird happened\."),
    ),
    "version_error": exception_map(
        exception=exceptions.VersionError,
        pattern=re.compile(
            r"Operation 'start_task_async' is not supported on PPA appliances older than v2\.7\.1\."
        ),
    ),
}


@pytest.mark.parametrize(
    "mocker, mock_response, exception_map_key",
    [
        [common.REVISIONS_MOCKER, mock_responses.AUTH_FAILED, "authentication_failed"],
        [common.REVISIONS_MOCKER, mock_responses.PERMISSION_DENIED, "permission_denied"],
        [common.REVISIONS_MOCKER, mock_responses.REQUEST_ERROR, "request_error"],
        [common.REVISIONS_MOCKER, mock_responses.INVALID_NON_JSON, "non_json_response"],
        [common.REVISIONS_MOCKER, mock_responses.SERVER_ERROR, "server_error"],
        [common.REVISIONS_MOCKER, mock_responses.UNHANDLED, "unhandled_request_error"],
    ],
    ids=[
        "authentication_failed",
        "permission_denied",
        "request_error",
        "non_json_response",
        "server_error",
        "unhandled_request_error",
    ],
)
def test_request_exceptions(mocker: Callable, mock_response: dict, exception_map_key: str):
    exception_config = EXCEPTIONS[exception_map_key]
    with mocker(mock_response):
        with pytest.raises(exception_config.exception, match=exception_config.pattern):
            common.get_client().images()


def test_credits_error():
    error_config = EXCEPTIONS["credits_required"]
    with common.mock_requests(
        [
            ("get", "tasks", mock_responses.TASKS),
            ("get", "images", mock_responses.IMAGES),
            ("post", "start_task", mock_responses.CREDITS_ERROR),
        ]
    ):
        with pytest.raises(error_config.exception, match=error_config.pattern):
            common.get_client().start_task_async("test")


def test_unsupported_version():
    with common.VERSION_MOCKER(mock_responses.NOT_FOUND_TEXT):
        with pytest.raises(
            exceptions.VersionError,
            match="This package does not support PPA appliances older than v2.7.1.",
        ):
            client.PPAClient("127.0.0.1", api_key="dummy")


def test_create_invalid_item():
    with pytest.raises(
        TypeError,
        match=r"Can only create API records from a list or dictionary, received <class 'tuple'>\.",
    ):
        create._creator(models.Task, (1, 2, 3))
