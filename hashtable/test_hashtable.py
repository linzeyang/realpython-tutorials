"""Unit tests for hashtable"""

import pytest

from collections import deque
from hashtable import HashTable


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
def test_should_report_capacity_of_empty_hashtable(num: int):
    assert HashTable(capacity=num).capacity == num


def test_should_report_capacity(hash_table: HashTable):
    assert hash_table.capacity == 100


@pytest.mark.parametrize("num", (10, 100))
def test_should_report_length_of_empty_hashtable(num: int):
    assert len(HashTable(capacity=num)) == 0


def test_should_report_length(hash_table: HashTable):
    assert len(hash_table) == 3


@pytest.mark.parametrize("num", (5, 10))
def test_should_create_empty_pair_slots(num: int):
    assert HashTable(capacity=num)._buckets == [deque()] * num


def test_should_insert_key_value_pairs(hash_table: HashTable):
    hash_table = HashTable(capacity=100)

    hash_table["hola"] = "hello"
    hash_table[98.6] = 37
    hash_table[False] = True

    assert ("hola", "hello") in hash_table.pairs
    assert (98.6, 37) in hash_table.pairs
    assert (False, True) in hash_table.pairs

    assert len(hash_table) == 3


def test_should_not_contain_none_value_when_created():
    assert None not in HashTable(capacity=100).values


def test_should_insert_none_value():
    local_hash_table = HashTable(capacity=100)

    local_hash_table["key"] = None

    assert ("key", None) in local_hash_table.pairs


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

    assert hash_table.capacity == 100


def test_should_find_key(hash_table: HashTable):
    assert "hola" in hash_table


def test_should_not_find_key(hash_table: HashTable):
    assert "missing_key" not in hash_table


def test_should_get_value(hash_table: HashTable):
    assert hash_table.get("hola") == "hello"


def test_should_get_none_when_missing_key(hash_table: HashTable):
    assert hash_table.get("missing_key") is None


def test_should_get_default_value_when_missing_key(hash_table: HashTable):
    assert hash_table.get("missing_key", "default") == "default"


def test_should_get_value_with_default(hash_table: HashTable):
    assert hash_table.get("hola", "default") == "hello"


def test_should_delete_key_value_pair(hash_table: HashTable):
    assert "hola" in hash_table
    assert ("hola", "hello") in hash_table.pairs
    assert len(hash_table) == 3

    del hash_table["hola"]

    assert "hola" not in hash_table
    assert ("hola", "hello") not in hash_table.pairs
    assert len(hash_table) == 2


def test_should_raise_key_error_when_deleting(hash_table: HashTable):
    with pytest.raises(KeyError) as exception_info:
        del hash_table["fake_key"]

    assert exception_info.value.args[0] == "fake_key"


def test_should_update_value(hash_table: HashTable):
    assert hash_table["hola"] == "hello"

    hash_table["hola"] = "hallo"

    assert hash_table["hola"] == "hallo"
    assert hash_table[98.6] == 37
    assert hash_table[False] is True
    assert len(hash_table) == 3


def test_should_return_pairs(hash_table: HashTable):
    assert ("hola", "hello") in hash_table.pairs
    assert (98.6, 37) in hash_table.pairs
    assert (False, True) in hash_table.pairs


def test_should_return_copy_of_pairs(hash_table: HashTable):
    assert hash_table.pairs is not hash_table.pairs


def test_should_not_include_blank_pairs(hash_table: HashTable):
    assert None not in hash_table.pairs


def test_should_return_duplicate_values():
    table = HashTable(capacity=100)
    table["Alice"] = 24
    table["Bob"] = 42
    table["Joe"] = 42

    assert sorted(table.values) == [24, 42, 42]


def test_should_get_values_of_empty_hashtable():
    assert HashTable(100).values == []


def test_should_return_copy_of_values(hash_table: HashTable):
    assert hash_table.values is not hash_table.values


def test_should_return_keys():
    table = HashTable(capacity=100)
    table["Alice"] = 24
    table["Bob"] = 42
    table["Joe"] = 42

    assert sorted(table.keys) == ["Alice", "Bob", "Joe"]  # type: ignore


def test_should_get_keys(hash_table: HashTable):
    assert set(hash_table.keys) == {"hola", 98.6, False}


def test_should_get_keys_of_empty_hashtable():
    assert HashTable(100).keys == []


def test_should_return_copy_of_keys(hash_table: HashTable):
    assert hash_table.keys is not hash_table.keys


def test_should_convert_to_dict(hash_table: HashTable):
    dic = dict(hash_table.pairs)

    assert set(dic.keys()) == set(hash_table.keys)
    assert set(dic.items()) == set(hash_table.pairs)
    assert list(dic.values()) == hash_table.values


def test_should_not_create_hashtable_with_zero_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=0)


def test_should_not_create_hashtable_with_negative_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=-1)


def test_should_iterate_over_keys(hash_table: HashTable):
    for key in hash_table.keys:
        assert key in {"hola", 98.6, False}


def test_should_iterate_over_values(hash_table: HashTable):
    for value in hash_table.values:
        assert value in {"hello", 37, True}


def test_should_iterate_over_pairs(hash_table: HashTable):
    for key, value in hash_table.pairs:
        assert key in hash_table.keys
        assert value in hash_table.values


def test_should_iterate_over_instance(hash_table: HashTable):
    for key in hash_table:
        assert key in {"hola", 98.6, False}


def test_should_use_dict_literal_for_str(hash_table: HashTable):
    assert str(hash_table) in {
        "{'hola': 'hello', 98.6: 37, False: True}",
        "{'hola': 'hello', False: True, 98.6: 37}",
        "{98.6: 37, 'hola': 'hello', False: True}",
        "{98.6: 37, False: True, 'hola': 'hello'}",
        "{False: True, 'hola': 'hello', 98.6: 37}",
        "{False: True, 98.6: 37, 'hola': 'hello'}",
    }


def test_should_create_hashtable_from_dict():
    dictionary = {"hola": "hello", 98.6: 37, False: True}

    table = HashTable.from_dict(dictionary)

    assert table.capacity == len(dictionary)
    assert set(table.keys) == set(dictionary.keys())
    assert set(table.pairs) == set(dictionary.items())
    assert sorted(table.values, key=hash) == sorted(dictionary.values(), key=hash)


def test_should_create_hashtable_from_dict_with_custom_capacity():
    dictionary = {"hola": "hello", 98.6: 37, False: True}

    table = HashTable.from_dict(dictionary, capacity=20)

    assert table.capacity == 20
    assert set(table.keys) == set(dictionary.keys())
    assert set(table.pairs) == set(dictionary.items())
    assert sorted(table.values, key=hash) == sorted(dictionary.values(), key=hash)


def test_should_have_canonical_string_representation(hash_table: HashTable):
    assert repr(hash_table) in {
        "HashTable.from_dict({'hola': 'hello', 98.6: 37, False: True})",
        "HashTable.from_dict({'hola': 'hello', False: True, 98.6: 37})",
        "HashTable.from_dict({98.6: 37, 'hola': 'hello', False: True})",
        "HashTable.from_dict({98.6: 37, False: True, 'hola': 'hello'})",
        "HashTable.from_dict({False: True, 'hola': 'hello', 98.6: 37})",
        "HashTable.from_dict({False: True, 98.6: 37, 'hola': 'hello'})",
    }


def test_equality_against_repr_and_str(hash_table: HashTable):
    assert eval(repr(hash_table)) == hash_table
    assert eval(str(hash_table)) == hash_table


def test_should_compare_equal_to_itself(hash_table: HashTable):
    assert hash_table == hash_table


def test_should_compare_equal_to_copy(hash_table: HashTable):
    assert hash_table == hash_table.copy()
    assert hash_table is not hash_table.copy()


def test_should_compare_equal_different_key_value_order():
    h1 = HashTable.from_dict({"a": 1, "b": 2, "c": 3})
    h2 = HashTable.from_dict({"b": 2, "a": 1, "c": 3})
    assert h1 == h2


def test_should_compare_unequal(hash_table: HashTable):
    other = HashTable.from_dict({"different": "value"})
    assert hash_table != other


def test_should_compare_unequal_another_data_type(hash_table: HashTable):
    assert hash_table != 42


def test_should_copy_keys_values_pairs_capacity(hash_table: HashTable):
    new = hash_table.copy()

    assert new is not hash_table
    assert set(hash_table.keys) == set(new.keys)
    assert hash_table.values == new.values
    assert set(hash_table.pairs) == set(new.pairs)
    assert hash_table.capacity == new.capacity


def test_should_compare_equal_different_capacity():
    data = {"a": 1, "b": 2, "c": 3}

    table1 = HashTable.from_dict(data, capacity=50)
    table2 = HashTable.from_dict(data, capacity=100)

    assert table1 == table2


def test_should_clear(hash_table: HashTable):
    assert len(hash_table)

    hash_table.clear()

    assert not len(hash_table)
    assert hash_table.capacity


def test_should_update_from_keyword_argument(hash_table: HashTable):
    hash_table.update(year=2022)

    assert hash_table["year"] == 2022


def test_should_overwrite_value_from_keyword_argument(hash_table: HashTable):
    hash_table.update(hola="Ni Hao")

    assert hash_table["hola"] == "Ni Hao"


def test_should_update_from_another_dictionary(hash_table: HashTable):
    hash_table.update({"year": 2022})

    assert hash_table["year"] == 2022


def test_should_update_from_another_hashtable(hash_table: HashTable):
    other = HashTable.from_dict({"name": "bob"})

    hash_table.update(other)

    assert hash_table["name"] == "bob"


def test_should_setdefault_work(hash_table: HashTable):
    assert hash_table["hola"] == "hello"

    value = hash_table.setdefault("hola", "whatever")

    assert value == "hello"
    assert hash_table["hola"] == "hello"

    value = hash_table.setdefault("year", 2022)

    assert value == 2022
    assert hash_table["year"] == 2022


def test_should_pop_pair(hash_table: HashTable):
    assert "hola" in hash_table
    assert len(hash_table) == 3

    value = hash_table.pop("hola")

    assert value == "hello"
    assert "hola" not in hash_table
    assert len(hash_table) == 2


def test_should_not_raise_if_default_is_given_to_pop(hash_table: HashTable):
    value = hash_table.pop("fake_key", "FakeKey")

    assert value == "FakeKey"
    assert len(hash_table) == 3


def test_should_raise_if_default_is_not_given_to_pop(hash_table: HashTable):
    with pytest.raises(KeyError):
        hash_table.pop("fake_key")

    assert len(hash_table) == 3


def test_itervalues_should_iterate_values(hash_table: HashTable):
    values = list(hash_table.itervalues())

    assert len(values) == 3
    assert sorted(values, key=hash) == sorted([True, "hello", 37], key=hash)


def test_should_deal_with_hash_collision():
    table = HashTable(capacity=8)
    table[1] = 1
    table[9] = 9
    table[17] = 17

    assert 1 in table
    assert table[1] == 1
    assert 9 in table
    assert table[9] == 9
    assert 17 in table
    assert table[17] == 17
    assert len(table) == 3


def test_should_raise_keyerror_retrieving_key():
    table = HashTable(capacity=8)

    for i in range(8):
        table[i] = i

    with pytest.raises(KeyError):
        table[9]


def test_should_raise_keyerror_deleting_key():
    table = HashTable(capacity=8)

    for i in range(8):
        table[i] = i

    with pytest.raises(KeyError):
        del table[9]


@pytest.mark.skipif(
    not hasattr(HashTable, "_resize_and_rehash"),
    reason="Testable only when resizing is implemented",
)
def test_should_resize_up():
    table = HashTable(capacity=16)

    for i in range(16):
        table[i] = i

    assert len(table) == 16
    assert table.capacity == 16

    table[16] = 16

    assert len(table) == 17
    assert table.capacity == 18
    for i in range(17):
        assert table[i] == i

    table[17] = 17

    assert len(table) == 18
    assert table.capacity == 18
    for i in range(18):
        assert table[i] == i


@pytest.mark.skipif(
    not hasattr(HashTable, "_resize_and_rehash"),
    reason="Testable only when resizing is implemented",
)
def test_should_resize_down():
    table = HashTable(capacity=16)

    for i in range(16):
        table[i] = i

    for i in range(9):
        del table[i]

    assert len(table) == 7
    assert table.capacity == 8
    for i in range(9, 16):
        assert table[i] == i


@pytest.mark.skipif(
    not hasattr(HashTable, "_resize_and_rehash"),
    reason="Testable only when resizing is implemented",
)
def test_should_not_resize_under_certain_condition():
    table = HashTable(capacity=8)

    for i in range(8):
        table[i] = i

    assert len(table) == 8
    assert table.capacity == 8

    del table[7]
    table[7] = 7

    assert table[7] == 7
    assert len(table) == 8
    assert table.capacity == 8

    del table[7]
    table[15] = 15

    assert table[15] == 15
    assert len(table) == 8
    assert table.capacity == 8

    for i in range(5):
        del table[i]

    assert len(table) == 3
    assert table.capacity == 8
