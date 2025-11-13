# with push, pop, peek, is_empty (wrap python list)

from typing import Generic, Iterable, List, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):    # I like to implement with Type saftey, to prevent bugs.
    # implement a custom stack class: LIFO stack by composing a Python list
    def __init__(self, initial: Iterable[T] | None = None) -> None:
        self._data: List[T] = list(initial) if initial is not None else []

    def push(self, item: T) -> None:
        self._data.append(item)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("Cannot pop from empty Stack")
        return self._data.pop()

    def peek(self) -> T:
        if not self._data:
            raise IndexError("Cannot peek from empty Stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return not self._data

    def __len__(self) -> int:
        return len(self._data)