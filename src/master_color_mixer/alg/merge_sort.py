from typing import List, TypeVar

T = TypeVar("T")


def merge_sort(arr: List[T]) -> List[T]:
    # return a new sorted list using the merge sort algorithm.

    if len(arr) <= 1:
        return arr[:]  # shallow copy https://www.w3schools.com/python/python_lists_copy.asp 

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    sorted_left = merge_sort(left_half)
    sorted_right = merge_sort(right_half)

    return merge(sorted_left, sorted_right)


def merge(left: List[T], right: List[T]) -> List[T]:
    # merge the sorted lists and return a new sorted list.
    # value types must be comparable with <

    result: List[T] = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
