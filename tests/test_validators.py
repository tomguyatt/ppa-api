import uuid

from typing import Callable, Optional, Union

import pytest

from ppa_api import exceptions, _client


VALID_UUID = str(uuid.uuid4())
VALID_PAYLOAD = {"cat": "dog"}


@pytest.mark.parametrize(
    "validator, expected_output, expected_exception, exception_pattern",
    [
        [
            lambda: _client.validate_uuid("dummy"),
            None,
            exceptions.ParameterError,
            "The format of the supplied UUID is invalid.",
        ],
        [lambda: _client.validate_uuid(VALID_UUID), VALID_UUID, None, None],
        [lambda: _client.validate_payload(VALID_PAYLOAD), VALID_PAYLOAD, None, None],
        [
            lambda: _client.validate_payload(range(0, 0)),
            None,
            exceptions.ParameterError,
            "The supplied payload cannot be converted to JSON.",
        ],
    ],
    ids=["valid_payload", "invalid_payload", "valid_uuid", "invalid_uuid"],
)
def test_validators(
    validator: Callable,
    expected_output: Union[str, _client.AnyJson],
    expected_exception: Exception,
    exception_pattern: Optional[str],
):
    if expected_exception:
        raises_kwargs = {"match": exception_pattern} if exception_pattern else {}
        with pytest.raises(expected_exception, **raises_kwargs):
            validator()
    else:
        assert validator() == expected_output
