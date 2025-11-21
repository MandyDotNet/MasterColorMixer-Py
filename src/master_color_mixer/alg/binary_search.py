from typing import List, TypeVar

T = TypeVar("T")


def binary_search(items: List[T], target: T) -> int:
    # returns the index of target if found
    
    low = 0
    high = len(items) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_value = items[mid]

        if mid_value == target:
            return mid
        elif mid_value < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1
