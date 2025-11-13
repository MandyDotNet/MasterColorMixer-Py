# with push, pop, peek, is_empty (wrap python list)

from typing import Generic, Iterable, List, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    # implement a custom stack class: LIFO stack by Python list
    def __init__(self, initial: Iterable[T] | None = None) -> None:
        self._data: List[T] = list(initial) if initial is not None else []