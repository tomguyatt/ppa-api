import pytest

from typing import Callable, Optional, List

from ppa_api import models, exceptions

import common
import mock_responses


TEST_NAME = "dummy"
TEST_ID = 1
PPA = common.get_client("2.10.0")
OLD_PPA = common.get_client()


@pytest.mark.parametrize(
    "mocker, mock_response, instance_method, return_tests, query_string",
    [
        [
            common.GROUPS_MOCKER,
            mock_responses.GROUPS,
            lambda instance: instance.groups(),
            [lambda x: all([isinstance(item, models.Group) for item in x])],
            None,
        ],
        [
            common.GROUPS_MOCKER,
            mock_responses.GROUPS,
            lambda instance: instance.group_by_name(TEST_NAME),
            [lambda item: isinstance(item, models.Group)],
            {"name": [f"ilike.*\\{TEST_NAME}"]},
        ],
    ],
    ids=[
        "groups",
        "group_by_name",
    ],
)
def test_group_requests(
    mocker: Callable,
    mock_response: dict,
    instance_method: Callable,
    return_tests: List[Callable],
    query_string: Optional[str],
):
    with mocker(mock_response) as mock_adapter:
        result = instance_method(PPA)
        print(result)
        assert all([test(result) for test in return_tests])
        if query_string:
            assert mock_adapter.request_history[0].qs == query_string


def test_version_limit():
    with pytest.raises(exceptions.VersionError):
        OLD_PPA.groups()
