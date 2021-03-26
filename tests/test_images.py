import pytest

from typing import Callable, Optional, List

from ppa_api import models

import common
import mock_responses


IMAGE_NAME = "Dummy Image"
IMAGE_ID = 1
PPA = common.get_client()


@pytest.mark.parametrize(
    "mocker, mock_response, instance_method, return_tests, query_string",
    [
        [
            common.REVISIONS_MOCKER,
            mock_responses.IMAGES,
            lambda instance: instance.images(),
            [lambda x: all([isinstance(item, models.Image) for item in x])],
            None,
        ],
        [
            common.IMAGES_MOCKER,
            mock_responses.IMAGES,
            lambda instance: instance.images(latest=True),
            [lambda x: all([isinstance(item, models.Image) for item in x])],
            None,
        ],
        [
            common.REVISIONS_MOCKER,
            mock_responses.IMAGES,
            lambda instance: instance.images_by_name(IMAGE_NAME),
            [lambda x: all([isinstance(item, models.Image) for item in x])],
            {"name": [f"eq.{IMAGE_NAME.lower()}"]}  # Gets lower-cased by requests-mock,
        ],
        [
            common.REVISIONS_MOCKER,
            mock_responses.EMPTY_LIST,
            lambda instance: instance.images_by_name(IMAGE_NAME),
            [lambda x: x == []],
            None,
        ],
        [
            common.IMAGES_MOCKER,
            mock_responses.IMAGES,
            lambda instance: instance.image_by_name(IMAGE_NAME),
            [lambda x: isinstance(x, models.Image)],
            {"name": [f"eq.{IMAGE_NAME.lower()}"]}  # Gets lower-cased by requests-mock,
        ],
        [
            common.IMAGES_MOCKER,
            mock_responses.EMPTY_LIST,
            lambda instance: instance.image_by_name(IMAGE_NAME),
            [lambda x: x is None],
            None,
        ],
        [
            common.REVISIONS_MOCKER,
            mock_responses.IMAGES,
            lambda instance: instance.image_by_id(IMAGE_ID),
            [lambda x: isinstance(x, models.Image)],
            {"id": [f"eq.{IMAGE_ID}"]},
        ],
        [
            common.REVISIONS_MOCKER,
            mock_responses.EMPTY_LIST,
            lambda instance: instance.image_by_id(IMAGE_ID),
            [lambda x: x is None],
            None,
        ],
    ],
    ids=[
        "all_images",
        "latest_images",
        "images_by_name",
        "images_by_name_none",
        "image_by_name",
        "image_by_name_none",
        "image_by_id",
        "image_by_id_none",
    ],
)
def test_image_requests(
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
