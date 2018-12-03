import pytest

import examples
from stories.exceptions import FailureError, FailureProtocolError


def test_reasons_defined_with_list():
    """We can use list of strings to define story failure protocol."""

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleWithList().x()
    assert exc_info.value.reason == "foo"
    assert repr(exc_info.value) == "FailureError('foo')"

    result = examples.failure_reasons.SimpleWithList().x.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason == "foo"
    assert result.failed_because("foo")


def test_reasons_defined_with_enum():
    """We can use enum class to define story failure protocol."""

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().x()
    assert (
        exc_info.value.reason is examples.failure_reasons.SimpleWithEnum.x.failures.foo
    )
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = examples.failure_reasons.SimpleWithEnum().x.run()
    assert not result.is_success
    assert result.is_failure
    assert (
        result.failure_reason is examples.failure_reasons.SimpleWithEnum.x.failures.foo
    )
    assert result.failed_because(examples.failure_reasons.SimpleWithEnum.x.failures.foo)


def test_wrong_reason_with_list():
    """
    We deny to use wrong reason in stories defined with list of
    strings as its failure protocol.
    """

    expected = """
"'foo' is too big" failure reason is not allowed by current protocol

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleWithList.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithList().y()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithList().y.run()
    assert str(exc_info.value) == expected


def test_wrong_reason_with_enum():
    """
    We deny to use wrong reason in stories defined with enum class as
    its failure protocol.
    """

    expected = """
"'foo' is too big" failure reason is not allowed by current protocol

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleWithEnum.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().y()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().y.run()
    assert str(exc_info.value) == expected


def test_null_reason_with_list():
    """
    We deny to use Failure() in stories defined with list of strings
    as its failure protocol.
    """

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleWithList.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithList().z()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithList().z.run()
    assert str(exc_info.value) == expected


def test_null_reason_with_enum():
    """
    We deny to use Failure() in stories defined with enum class as its
    failure protocol.
    """

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleWithEnum.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().z()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().z.run()
    assert str(exc_info.value) == expected
