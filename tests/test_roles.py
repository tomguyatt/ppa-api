import pytest

from typing import Callable, Optional, List

from ppa_api import models, exceptions

import common
import mock_responses


TEST_NAME = "dummy"
TEST_ID = 123
PPA = common.get_client("2.10.0")
OLD_PPA = common.get_client()


@pytest.mark.parametrize(
    "mocker, mock_response, instance_method, return_tests, query_string",
    [
        [
            common.ROLES_MOCKER,
            mock_responses.ROLES,
            lambda instance: instance.roles(),
            [lambda x: all([isinstance(item, models.Role) for item in x])],
            None,
        ],
        [
            common.ROLES_MOCKER,
            mock_responses.ROLES,
            lambda instance: instance.role_by_name(TEST_NAME),
            [lambda item: isinstance(item, models.Role)],
            {"name": [f"ilike.*\\{TEST_NAME}"]},
        ],
        [
            common.ROLES_MOCKER,
            mock_responses.ROLES,
            lambda instance: instance.role_by_id(TEST_ID),
            [lambda item: isinstance(item, models.Role)],
            {"id": [f"eq.{TEST_ID}"]},
        ],
        [
            common.ROLES_MOCKER,
            mock_responses.ROLES,
            lambda instance: instance.roles(),
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
        "roles",
        "role_by_name",
        "role_by_id",
        "user_record_modifier",
    ],
)
def test_role_requests(
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


def test_version_limit():
    with pytest.raises(exceptions.VersionError):
        OLD_PPA.roles()
