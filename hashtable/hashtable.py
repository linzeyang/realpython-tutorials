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

    def __setitem__(self, key: Hashable, value: Any) -> None:
        idx = hash(key) % len(self)
        self._values[idx] = value

    def __getitem__(self, key: Hashable) -> Any:
        idx = hash(key) % len(self)

        if (value := self._values[idx]) is BLANK:
            raise KeyError("missing_key")

        return value

    def __delitem__(self, key: Hashable) -> None:
        idx = hash(key) % len(self)

        if self._values[idx] is BLANK:
            raise KeyError("missing_key")

        self._values[idx] = BLANK

    def __contains__(self, key: Hashable) -> bool:
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def get(self, key, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default
