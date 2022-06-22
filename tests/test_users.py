import pytest

from typing import Callable, Optional, List

from ppa_api import models

import common
import mock_responses


TEST_NAME = "dummy"
TEST_ID = 1
SELECT_PARAMS = [
    "id,username,name,email,authenticated_at,active,deleted_at,groups,permissions,roles_count"
]
PPA = common.get_client()


@pytest.mark.parametrize(
    "mocker, mock_response, instance_method, return_tests, query_string",
    [
        [
            common.USERS_MOCKER,
            mock_responses.USERS,
            lambda instance: instance.users(),
            [lambda x: all([isinstance(item, models.User) for item in x])],
            {"select": SELECT_PARAMS, "deleted_at": ["is.null"]},
        ],
        [
            common.USERS_MOCKER,
            mock_responses.USERS,
            lambda instance: instance.deleted_users(),
            [lambda x: all([isinstance(item, models.User) for item in x])],
            {"select": SELECT_PARAMS, "deleted_at": ["not.is.null"]},
        ],
        [
            common.USERS_MOCKER,
            mock_responses.USERS,
            lambda instance: instance.licensed_users(),
            [lambda x: all([isinstance(item, models.User) for item in x])],
            {"select": SELECT_PARAMS, "deleted_at": ["is.null"], "active": ["eq.true"]},
        ],
        [
            common.USERS_MOCKER,
            mock_responses.USERS,
            lambda instance: instance.user_by_username(TEST_NAME),
            [lambda x: isinstance(x, models.User)],
            {"username": [f"ilike.*\\{TEST_NAME}"], "select": SELECT_PARAMS},
        ],
        [
            common.USERS_MOCKER,
            mock_responses.EMPTY_LIST,
            lambda instance: instance.user_by_username(TEST_NAME),
            [lambda x: x is None],
            {"username": [f"ilike.*\\{TEST_NAME}"], "select": SELECT_PARAMS},
        ],
        [
            common.USERS_MOCKER,
            mock_responses.USERS,
            lambda instance: instance.user_by_id(TEST_ID),
            [lambda x: isinstance(x, models.User)],
            {"id": [f"eq.{TEST_ID}"], "select": SELECT_PARAMS},
        ],
        [
            common.USERS_MOCKER,
            mock_responses.EMPTY_LIST,
            lambda instance: instance.user_by_id(TEST_ID),
            [lambda x: x is None],
            {"id": [f"eq.{TEST_ID}"], "select": SELECT_PARAMS},
        ],
        [
            common.USERS_MOCKER,
            mock_responses.USERS,
            lambda instance: instance.users(),
            [
                lambda items: all(
                    [
                        not group.startswith("ad:domain.net:")
                        for item in items
                        for group in item.groups
                    ]
                )
            ],
            None,
        ],
    ],
    ids=[
        "current_users",
        "deleted_users",
        "licensed_users",
        "user_by_name",
        "user_by_name_none",
        "user_by_id",
        "user_by_id_none",
        "user_record_modifier",
    ],
)
def test_user_requests(
    mocker: Callable,
    mock_response: dict,
    instance_method: Callable,
    return_tests: List[Callable],
    query_string: Optional[str],
):
    with mocker(mock_response) as mock_adapter:
        result = instance_method(PPA)
        assert all([test(result) for test in return_tests])
        if query_string:
            assert mock_adapter.request_history[0].qs == query_string
