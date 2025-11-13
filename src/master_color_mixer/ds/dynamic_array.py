# with append, pop, __getitem__, __setitem__, __len__ (wrap python list)
# to support API

from typing import TypeVar

T = TypeVar("T")

class DynamicArray():

    # initializer (constructor)
    def __init__(self, initial = None): #if given make a copy as list, otherwise start empty list
        
        if initial is None:
            self._data = []
        else:
            self._data = list(initial)

    # -> methods below use a shorthand (pattern called early return) 
    # to avoid nested if blocks, but also because of habbit

    def append(self, item: T) -> None:
        self._data.append(item)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("cannot pop from empty DynamicArray")
        return self._data.pop()

    def __getitem__(self, index: int) -> T:
        return self._data[index]

    def __setitem__(self, index: int, value: T) -> None:
        self._data[index] = value

    def __len__(self) -> int:   # O(1): constant
        return len(self._data)

    # nice to have for future:
    # list comprehensions - 
    #   when a goal is to create a new list from an existing iterable, 
    #   using list comprehensions allows for loop logic, transformations, and filtering in compact code.
    #   this offers performance boosts, and encapsulated logic
    # not asked for in this assignment, but I may add it to my final program.
    # I would use it on 
    #   an __iter__ method for [x for x in dataArray] and 
    #   an __repr__ method for DynamicArray([1, 2, 3]) to help with debugging.
    # and would need to be careful with test coverage on debugging methods (pragma: no cover)