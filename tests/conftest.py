import logging
import sys

import pytest

from ppa_api import client

import mock_responses
import common


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s %(module)s.%(funcName)s:%(lineno)d %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


ADDRESS = "127.0.0.1"
API_KEY = "dummy"


@pytest.fixture
def ppa():
    with common.mock_request("get", "version", mock_responses.VERSIONS["2.7.1"]):
        return client.PPAClient(ADDRESS, api_key=API_KEY)


@pytest.fixture
def ppa_unknown_version():
    with common.mock_request("get", "version", mock_responses.NOT_FOUND_TEXT):
        return client.PPAClient(ADDRESS, api_key=API_KEY)
