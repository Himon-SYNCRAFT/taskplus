import pytest

from taskplus.core.shared.repository import (Repository, InvalidOperatorError,
                                             Filter)


def test_repository_parse_valid_filters():
    repository = Repository()
    filters = {
        'filter1__eq': 1,
        'filter2__lt': 1,
        'filter3__le': 1,
        'filter4__ne': 1,
        'filter5__ge': 1,
        'filter6__gt': 1,
        'filter7': 1,
    }
    result = repository._parse_filters(filters)

    assert Filter('filter1', '__eq__', 1) in result
    assert Filter('filter2', '__lt__', 1) in result
    assert Filter('filter3', '__le__', 1) in result
    assert Filter('filter4', '__ne__', 1) in result
    assert Filter('filter5', '__ge__', 1) in result
    assert Filter('filter6', '__gt__', 1) in result
    assert Filter('filter7', '__eq__', 1) in result


def test_repository_parse_filters_raise_exception_with_invalid_data():
    repository = Repository()
    filters = {
        'filter__or': 1,
    }

    with pytest.raises(InvalidOperatorError) as exc:
        repository._parse_filters(filters)

    assert str(exc.value) == 'Operator or is not supported'


def test_repository_parse_filters_return_none_if_empty_filters():
    repository = Repository()
    filters = {}
    result = repository._parse_filters(filters)

    assert result is None

    filters = None
    result = repository._parse_filters(filters)

    assert result is None
