"""This is a hashtable"""

from collections import deque
from typing import Any, Hashable, NamedTuple

DUMMY_STATE = -1
LOAD_THRESHOLD = 0.66


class Pair(NamedTuple):
    key: Hashable
    value: Any


class HashTable:
    """A hashtable implementation"""

    def __init__(self, capacity: int = 8) -> None:
        if capacity <= 0:
            raise ValueError("capacity should be positive integer")

        self._buckets: list[deque[Pair]] = [deque() for _ in range(capacity)]
        self._key_insertion_order: list[Hashable] = []

    def __len__(self) -> int:
        return len(self.pairs)

    @property
    def capacity(self) -> int:
        return len(self._buckets)

    @property
    def pairs(self) -> list[Pair]:
        return [Pair(key, self[key]) for key in self._key_insertion_order]

    @property
    def keys(self) -> list[Hashable]:
        return [pair.key for pair in self.pairs]

    @property
    def values(self) -> list[Any]:
        return [pair.value for pair in self.pairs]

    @property
    def load_factor(self) -> float:
        return len(self) / self.capacity

    def _index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        queue = self._buckets[self._index(key)]

        for idx, pair in enumerate(queue):
            if hash(pair.key) == hash(key):
                queue[idx] = Pair(key, value)
                return

        queue.append(Pair(key, value))
        self._key_insertion_order.append(key)

    def __getitem__(self, key: Hashable) -> Any:
        for pair in self._buckets[self._index(key)]:
            if hash(key) == hash(pair.key):
                return pair.value

        raise KeyError(key)

    def __delitem__(self, key: Hashable) -> None:
        queue = self._buckets[self._index(key)]

        for pair in queue:
            if hash(pair.key) == hash(key):
                queue.remove(pair)
                self._key_insertion_order.remove(key)
                return

        raise KeyError(key)

    def __contains__(self, key: Hashable) -> bool:
        try:
            self[key]
        except KeyError:
            return False
        return True

    def __iter__(self):
        yield from iter(self._key_insertion_order)

    def __str__(self) -> str:
        return f"{{{', '.join(f'{key!r}: {value!r}' for key, value in self.pairs)}}}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.from_dict({str(self)})"

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True

        if isinstance(other, dict):
            return set(self.pairs) == set(other.items())

        if isinstance(other, self.__class__):
            return set(self.pairs) == set(other.pairs)

        return False

    # def _probe(self, key: Hashable):
    #     """A helper method"""
    #     index = self._index(key)

    #     for _ in range(self.capacity):
    #         yield index, self._slots[index]
    #         index = (index + 1) % self.capacity

    # def _resize_and_rehash(self) -> None:
    #     if len(self) == self.capacity:
    #         new_capacity = self.capacity + (self.capacity >> 3)

    #         if new_capacity == self.capacity:
    #             new_capacity += 1
    #     elif self._slots.count(DUMMY_STATE) > (self.capacity >> 1):
    #         new_capacity = max(8, self.capacity >> 1)

    #         if new_capacity == self.capacity:
    #             return
    #     else:
    #         return

    #     old_slots = self._slots
    #     self._slots = [None] * new_capacity

    #     for slot in old_slots:
    #         if isinstance(slot, Pair):
    #             self[slot.key] = slot.value

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    @classmethod
    def from_dict(cls, source: dict, capacity: int | None = None):
        new = cls(capacity or len(source))

        for key, value in source.items():
            new[key] = value

        return new

    def copy(self):
        return self.__class__.from_dict(dict(self.pairs), self.capacity)

    def clear(self) -> None:
        for idx in range(self.capacity):
            self._buckets[idx] = deque()

        self._key_insertion_order.clear()

    def update(self, other: object = None, /, **kwargs) -> None:
        # only consider kwargs if other is not given
        if other is None:
            for k, v in kwargs.items():
                self[k] = v
            return

        # other and kwargs can not be both empty
        if kwargs:
            raise ValueError()

        if isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
            return

        if isinstance(other, self.__class__):
            for key, value in other.pairs:
                self[key] = value
            return

        raise TypeError("incompatible object")

    def setdefault(self, key: Hashable, default: Any, /) -> Any:
        if key not in self:
            self[key] = default

        return self[key]

    def pop(self, key: Hashable, /, default: Any = None) -> Any:
        if key not in self:
            if default is None:
                raise KeyError(key)
            return default

        value = self[key]
        del self[key]

        return value

    # my own impremetation!
    def iteritems(self):
        for queue in self._buckets:
            for pair in queue:
                yield pair.key, pair.value

    def iterkeys(self):
        for queue in self._buckets:
            for pair in queue:
                yield pair.key

    def itervalues(self):
        for queue in self._buckets:
            for pair in queue:
                yield pair.value
    # ...
