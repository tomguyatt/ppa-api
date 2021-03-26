import uuid

from typing import Callable, Optional, List

import pytest

from ppa_api import exceptions, models

import common
import mock_responses


TEST_NAME = "Dummy Task"
TEST_UUID = str(uuid.uuid4())
TASK_BY_UUID_PARAMS = {"uuid": [f"eq.{TEST_UUID}"]}
PPA = common.get_client()


# Tests that only need a single mocked endpoint are parametrized, everything else is tested further down.
@pytest.mark.parametrize(
    "mocker, mock_response, instance_method, return_tests, query_string, request_body, expected_exception, exception_pattern",
    [
        [
            common.TASKS_MOCKER,
            mock_responses.TASKS,
            lambda instance: instance.tasks(),
            [lambda x: all([isinstance(item, models.Task) for item in x])],
            None,
            None,
            None,
            None,
        ],
        [
            common.TASKS_MOCKER,
            mock_responses.TASKS,
            lambda instance: instance.task_by_uuid(TEST_UUID),
            [lambda x: isinstance(x, models.Task)],
            TASK_BY_UUID_PARAMS,
            None,
            None,
            None,
        ],
        [
            common.TASKS_MOCKER,
            mock_responses.TASKS,
            lambda instance: instance.tasks_started_by_me(),
            [lambda x: all([isinstance(item, models.Task) for item in x])],
            {"is_owner": ["eq.true"]},
            None,
            None,
            None,
        ],
        [
            common.TASKS_MOCKER,
            mock_responses.RUNNING_TASK,
            lambda instance: instance.task_running(TEST_UUID),
            [lambda x: x is True],
            TASK_BY_UUID_PARAMS,
            None,
            None,
            None,
        ],
        [
            common.TASKS_MOCKER,
            mock_responses.EMPTY_LIST,
            lambda instance: instance.task_running(TEST_UUID),
            [],
            None,
            None,
            exceptions.NoTaskFound,
            f"No task was found with UUID '{TEST_UUID}'.",
        ],
        [
            common.TASKS_MOCKER,
            mock_responses.SUCCESSFUL_TASK,
            lambda instance: instance.task_succeeded(TEST_UUID),
            [lambda x: x is True],
            TASK_BY_UUID_PARAMS,
            None,
            None,
            None,
        ],
        [
            common.TASKS_MOCKER,
            mock_responses.FAILED_TASK,
            lambda instance: instance.task_succeeded(TEST_UUID),
            [lambda x: x is False],
            TASK_BY_UUID_PARAMS,
            None,
            None,
            None,
        ],
        [
            common.TASKS_MOCKER,
            mock_responses.RUNNING_TASK,
            lambda instance: instance.task_succeeded(TEST_UUID),
            [],
            None,
            None,
            exceptions.TaskStillRunning,
            f"Task with UUID '{TEST_UUID}' is still running.",
        ],
        [
            common.IMAGES_MOCKER,
            mock_responses.EMPTY_LIST,
            lambda instance: instance.start_task_async(TEST_NAME),
            [],
            None,
            None,
            exceptions.NoImageFound,
            f"There are no images delegated to your identity with the name '{TEST_NAME}'.",
        ],
        [
            common.TASKS_MOCKER,
            mock_responses.RUNNING_TASK,
            lambda instance: instance.wait_for_task(TEST_UUID, timeout=0.1, interval=0.1),
            [],
            None,
            None,
            exceptions.WaitTimeout,
            "Task has not finished after 0.1 seconds.",
        ],
        [
            common.CANCEL_TASK_MOCKER,
            mock_responses.EMPTY_STRING,
            lambda instance: instance.cancel_task(TEST_UUID),
            [],
            None,
            f'{{"uuid": "{TEST_UUID}"}}',
            None,
            None,
        ],
        [
            common.CANCEL_TASK_MOCKER,
            mock_responses.NOT_FOUND_JSON,
            lambda instance: instance.cancel_task(TEST_UUID),
            [],
            None,
            f'{{"uuid": "{TEST_UUID}"}}',
            exceptions.NoTaskFound,
            rf"Task with UUID '{TEST_UUID}' is either not running or does not exist\.",
        ],
        [
            common.TASK_RESULT_MOCKER,
            mock_responses.TASK_RESULT,
            lambda instance: instance.get_task_result(TEST_UUID),
            [],
            None,
            f'{{"uuid": "{TEST_UUID}"}}',
            None,
            None,
        ],
        [
            common.TASK_RESULT_MOCKER,
            mock_responses.NO_DATA,
            lambda instance: instance.get_task_result(TEST_UUID),
            [],
            None,
            None,
            exceptions.NoData,
            rf"No result data was saved by task with UUID '{TEST_UUID}'\.",
        ],
    ],
    ids=[
        "all_tasks",
        "task_by_uuid",
        "started_by_me",
        "task_running",
        "task_running_not_found",
        "task_succeeded_true",
        "task_succeeded_false",
        "task_succeeded_still_running",
        "start_task_async_not_found",
        "start_task_timeout",
        "cancel_task",
        "cancel_task_not_found",
        "task_result",
        "task_result_no_data",
    ],
)
def test_task_requests(
    mocker: Callable,
    mock_response: dict,
    instance_method: Callable,
    return_tests: List[Callable],
    query_string: Optional[dict],
    request_body: Optional[dict],
    expected_exception: Optional[Exception],
    exception_pattern: Optional[str],
):
    with mocker(mock_response) as mock_adapter:
        if expected_exception:
            raises_kwargs = {"match": exception_pattern} if exception_pattern else {}
            with pytest.raises(expected_exception, **raises_kwargs):
                instance_method(PPA)
        else:
            result = instance_method(PPA)
            assert all([test(result) for test in return_tests])
            if query_string:
                assert mock_adapter.request_history[0].qs == query_string
            if request_body:
                assert mock_adapter.request_history[0]._request.body.decode("utf-8") == request_body


def test_start_task():
    with common.mock_requests(
        [
            ("get", "images", mock_responses.IMAGES),
            ("get", "tasks", mock_responses.TASKS),
            ("post", "start_task", mock_responses.TASK_STARTED),
        ]
    ):
        PPA.start_task("Dummy Task", timeout=0)


def test_must_be_deployed():
    with common.mock_requests(
        [
            ("get", "images", mock_responses.TASKS),
            ("post", "start_task", mock_responses.TASK_MUST_BE_DEPLOYED),
        ]
    ):
        with pytest.raises(
            exceptions.ImageNotDeployed,
            match="The task cannot be started as image 'Dummy Task' is not deployed.",
        ):
            PPA.start_task_async("Dummy Task")

    # Test that a 400 error that isn't a deployment issue is raised with a generic exception.
    with common.mock_requests(
        [
            ("get", "images", mock_responses.TASKS),
            ("post", "start_task", mock_responses.REQUEST_ERROR),
        ]
    ):
        with pytest.raises(exceptions.RequestError):
            PPA.start_task_async("Dummy Task")


def test_wait_for_task():
    with common.mock_requests(
        [
            (
                "get",
                "tasks",
                [
                    mock_responses.RUNNING_TASK,  # First poll response
                    mock_responses.SUCCESSFUL_TASK,  # Second poll response
                ],
            )
        ]
    ):
        PPA.wait_for_task(TEST_UUID, interval=0)
