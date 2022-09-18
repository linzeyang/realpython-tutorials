"""This is a hashtable"""

from typing import Any, Hashable

BLANK = object()


class HashTable:
    """A hashtable implementation"""

    def __init__(self, capacity: int) -> None:
        self._values = [BLANK] * capacity

    def __len__(self) -> int:
        return len(self._values)

    @property
    def values(self) -> list[Any]:
        return self._values

    def _index(self, key: Hashable) -> int:
        return hash(key) % len(self)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.values[self._index(key)] = value

    def __getitem__(self, key: Hashable) -> Any:
        if (value := self.values[self._index(key)]) is BLANK:
            raise KeyError("missing_key")

        return value

    def __delitem__(self, key: Hashable) -> None:
        if key not in self:
            raise KeyError("missing_key")

        self[key] = BLANK

    def __contains__(self, key: Hashable) -> bool:
        try:
            self[key]
        except KeyError:
            return False
        return True

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default
