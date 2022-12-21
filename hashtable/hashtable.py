"""This is a hashtable"""

from typing import Any, Hashable, NamedTuple


class Pair(NamedTuple):
    key: Any
    value: Any


class HashTable:
    """A hashtable implementation"""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity should be positive integer")

        self._slots = [None] * capacity

    def __len__(self) -> int:
        return len(self.pairs)

    @property
    def capacity(self) -> int:
        return len(self._slots)

    @property
    def pairs(self) -> list[Any]:
        return [slot for slot in self._slots if slot]

    @property
    def keys(self) -> list[Any]:
        return [pair.key for pair in self.pairs]

    @property
    def values(self) -> list[Any]:
        return [pair.value for pair in self.pairs]

    def _index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self._slots[self._index(key)] = Pair(key, value)  # type: ignore

    def __getitem__(self, key: Hashable) -> Any:
        if (pair := self._slots[self._index(key)]) is None:
            raise KeyError(key)

        return pair.value

    def __delitem__(self, key: Hashable) -> None:
        if key not in self:
            raise KeyError(key)

        self._slots[self._index(key)] = None

    def __contains__(self, key: Hashable) -> bool:
        try:
            self[key]
        except KeyError:
            return False
        return True

    def __iter__(self):
        yield from self.iterkeys()

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

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    @classmethod
    def from_dict(cls, source: dict, capacity: int | None = None):
        new = cls(capacity or len(source) * 10)

        for key, value in source.items():
            new[key] = value

        return new

    def copy(self):
        return self.__class__.from_dict(dict(self.pairs), self.capacity)
        # new = HashTable(self.capacity)
        # new._slots = self._slots.copy()
        # return new

    def clear(self) -> None:
        for idx, slot in enumerate(self._slots):
            if slot is not None:
                self._slots[idx] = None

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

    def setdefault(self, key: Any, default: Any, /) -> Any:
        if key not in self:
            self[key] = default

        return self[key]

    def pop(self, key: Any, /, default: Any = None) -> Any:
        if key not in self:
            if default is None:
                raise KeyError(key)
            return default

        value = self[key]

        del self[key]

        return value

    # my own impremetation!
    def iteritems(self):
        for slot in self._slots:
            if slot is not None:
                yield slot.key, slot.value

    def iterkeys(self):
        for slot in self._slots:
            if slot is not None:
                yield slot.key

    def itervalues(self):
        for slot in self._slots:
            if slot is not None:
                yield slot.value

    # ...
