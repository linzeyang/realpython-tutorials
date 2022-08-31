"""Unit tests for hashtable"""

import pytest

from hashtable import BLANK, HashTable


@pytest.fixture
def hash_table():
    sample = HashTable(capacity=100)
    sample["hola"] = "hello"
    sample[98.6] = 37
    sample[False] = True

    return sample


def test_should_create_hashtable():
    assert HashTable(capacity=100) is not None


@pytest.mark.parametrize("num", (10, 100))
def test_should_report_capacity(num: int):
    assert len(HashTable(capacity=num)) == num


@pytest.mark.parametrize("num", (5, 10))
def test_should_create_empty_value_slots(num: int):
    assert HashTable(capacity=num).values == [BLANK] * num


def test_should_insert_key_value_pairs(hash_table: HashTable):
    hash_table = HashTable(capacity=100)

    hash_table["hola"] = "hello"
    hash_table[98.6] = 37
    hash_table[False] = True

    assert "hello" in hash_table.values
    assert 37 in hash_table.values
    assert True in hash_table.values

    assert len(hash_table) == 100


def test_should_not_contain_none_value_when_created():
    assert None not in HashTable(capacity=100).values


def test_should_insert_none_value():
    local_hash_table = HashTable(capacity=100)

    local_hash_table["key"] = None

    assert None in local_hash_table.values


def test_should_find_value_by_key(hash_table: HashTable):
    assert hash_table["hola"] == "hello"
    assert hash_table[98.6] == 37
    assert hash_table[False] is True


def test_should_raise_error_on_missing_key():
    local_hash_table = HashTable(capacity=100)

    with pytest.raises(KeyError) as exception_info:
        local_hash_table["missing_key"]

    assert exception_info.value.args[0] == "missing_key"


def test_should_not_shrink_when_removing_elements(hash_table: HashTable):
    del hash_table["hola"]
    del hash_table[98.6]
    del hash_table[False]

    assert len(hash_table) == 100


def test_should_find_key(hash_table):
    assert "hola" in hash_table


def test_should_not_find_key(hash_table):
    assert "missing_key" not in hash_table


def test_should_get_value(hash_table):
    assert hash_table.get("hola") == "hello"


def test_should_get_none_when_missing_key(hash_table):
    assert hash_table.get("missing_key") is None


def test_should_get_default_value_when_missing_key(hash_table):
    assert hash_table.get("missing_key", "default") == "default"


def test_should_get_value_with_default(hash_table):
    assert hash_table.get("hola", "default") == "hello"
