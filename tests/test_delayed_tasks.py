from typing import Callable, Optional, List

import pytest

from ppa_api import exceptions, models

import common
import mock_responses


# Delayed start is a 2.8.0 feature
PPA = common.get_client("2.8.0")


def test_unsupported_version():
    with pytest.raises(
        exceptions.VersionError,
        match="The delayed_tasks method requires PPA version 2.8.0 or later, but your version is 2.7.1.",
    ):
        # Make a client with default version 2.7.1.
        common.get_client().delayed_tasks()


# Tests that only need a single mocked endpoint are parametrized, everything else is tested further down.
@pytest.mark.parametrize(
    "mocker, mock_response, instance_method, return_tests, query_string",
    [
        [
            common.DELAYED_TASKS_MOCKER,
            mock_responses.DELAYED_TASKS,
            lambda instance: instance.delayed_tasks(),
            [lambda x: all([isinstance(item, models.DelayedTask) for item in x])],
            None,
        ],
        [
            common.DELAYED_TASKS_MOCKER,
            mock_responses.DELAYED_TASKS,
            lambda instance: instance.delayed_task_by_id(1),
            [lambda x: isinstance(x, models.DelayedTask)],
            {"id": ["eq.1"]},
        ],
        [
            common.DELAYED_TASKS_MOCKER,
            mock_responses.EMPTY_LIST,
            lambda instance: instance.delayed_task_by_id(1),
            [lambda x: x is None],
            {"id": ["eq.1"]},
        ],
        [
            common.DELAYED_TASKS_MOCKER,
            mock_responses.DELAYED_TASKS,
            lambda instance: instance.tasks_delayed_by_me(),
            [lambda x: all([isinstance(item, models.DelayedTask) for item in x])],
            {"is_owner": ["eq.true"]},
        ],
        [
            common.DELAYED_TASKS_MOCKER,
            mock_responses.DELAYED_TASKS,
            lambda instance: instance.pending_delayed_tasks(),
            [lambda x: all([isinstance(item, models.DelayedTask) for item in x])],
            {"is_pending": ["eq.true"]},
        ],
        [
            common.DELAYED_TASKS_MOCKER,
            mock_responses.DELAYED_TASKS,
            lambda instance: instance.processed_delayed_tasks(),
            [lambda x: all([isinstance(item, models.DelayedTask) for item in x])],
            {"is_pending": ["eq.false"]},
        ],
    ],
    ids=[
        "all_delayed_tasks",
        "delayed_task_by_id",
        "delayed_task_by_id_none",
        "tasks_delayed_by_me",
        "pending_delayed_tasks",
        "processed_delayed_tasks",
    ],
)
def test_delay_task_requests(
    mocker: Callable,
    mock_response: dict,
    instance_method: Callable,
    return_tests: List[Callable],
    query_string: Optional[dict],
):
    with mocker(mock_response) as mock_adapter:
        result = instance_method(PPA)
        assert all([test(result) for test in return_tests])
        if query_string:
            assert mock_adapter.request_history[0].qs == query_string


def test_delay_task():
    with common.mock_requests(
        [
            ("get", "images", mock_responses.IMAGES),
            ("get", "delayed_tasks", mock_responses.DELAYED_TASKS),
            ("post", "delay_task", mock_responses.TASK_DELAYED),
        ]
    ):
        PPA.delay_task("Dummy Task", delay=1, description="test")


def test_delay_not_found():
    with common.mock_requests([("get", "images", mock_responses.EMPTY_LIST)]):
        with pytest.raises(
            exceptions.NoImageFound,
            match="There are no images delegated to your identity with the name 'Dummy Task'.",
        ):
            PPA.delay_task("Dummy Task", delay=1, description="test")


def test_must_be_deployed():
    with common.mock_requests(
        [
            ("get", "images", mock_responses.TASKS),
            ("post", "delay_task", mock_responses.DELAY_MUST_BE_DEPLOYED),
        ]
    ):
        with pytest.raises(
            exceptions.ImageNotDeployed,
            match="The delayed task cannot be created as image 'Dummy Task' is not deployed.",
        ):
            PPA.delay_task("Dummy Task", delay=1, description="test")

    # Test that a 400 error that isn't a deployment issue is raised with a generic exception.
    with common.mock_requests(
        [
            ("get", "images", mock_responses.TASKS),
            ("post", "delay_task", mock_responses.REQUEST_ERROR),
        ]
    ):
        with pytest.raises(exceptions.RequestError):
            PPA.delay_task("Dummy Task", delay=1, description="test")
