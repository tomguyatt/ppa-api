import contextlib
import functools

from requests.compat import urljoin  # type: ignore
from requests.utils import prepend_scheme_if_needed

import requests_mock


ADDRESS = "127.0.0.1"

ENDPOINTS = {
    "images": "/backend/v1/rest/images",
    "revisions": "/backend/v1/rest/revisions",
    "tasks": "/backend/v1/rest/tasks",
    "start_task": "backend/v1/rest/rpc/start_task",
    "cancel_task": "backend/v1/rest/rpc/cancel_task",
    "task_result": "backend/v1/rest/rpc/task_result",
    "version": "backend/v1/version",
    "users": "backend/v1/rest/users",
}


def _generate_url(endpoint):
    return urljoin(prepend_scheme_if_needed(ADDRESS, "https"), ENDPOINTS[endpoint])


@contextlib.contextmanager
def mock_requests(mocked_requests):

    if unsupported_methods := [r[0] for r in mocked_requests if r[0] not in {"get", "post"}]:
        raise ValueError(
            "Mock request method(s) '{}' not supported.".format(
                ", ".join(list(set(unsupported_methods)))
            )
        )

    with requests_mock.Mocker() as mocker:
        for method, endpoint, responses in mocked_requests:
            getattr(mocker, method)(
                _generate_url(endpoint),
                [responses] if not isinstance(responses, list) else responses,
            )
        yield mocker


@contextlib.contextmanager
def mock_request(method: str, endpoint: str, responses):
    with mock_requests([(method, endpoint, responses)]) as mocker:
        yield mocker


IMAGES_MOCKER = functools.partial(mock_request, "get", "images")
REVISIONS_MOCKER = functools.partial(mock_request, "get", "revisions")
VERSION_MOCKER = functools.partial(mock_request, "get", "version")
USERS_MOCKER = functools.partial(mock_request, "get", "users")
TASKS_MOCKER = functools.partial(mock_request, "get", "tasks")
START_TASK_MOCKER = functools.partial(mock_request, "post", "start_task")
CANCEL_TASK_MOCKER = functools.partial(mock_request, "post", "cancel_task")
TASK_RESULT_MOCKER = functools.partial(mock_request, "post", "task_result")
