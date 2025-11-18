# with add, remove, contains, __len__ (compose Python set)

from typing import Generic, Iterable, Set,TypeVar

T = TypeVar("T")

class HashSet(Generic[T]): # I like to implement with Type saftey, to prevent bugs. Mirrors how we use HashSeT<T> in C#

    # can be any iterable type like list or set / stored as set(T) or an empty set()
    def __init__(self, initial: Iterable[T] | None = None) -> None:
        self._set: Set[T] = set(initial) if initial is not None else set()

    def add(self, item: T) -> None:
        self._set.add(item)

    def remove(self, item: T) -> None:
        self._set.remove(item)

    def contains(self, item: T) -> bool:
        return item in self._set

    def __len__(self) -> int:
        return len(self._set)