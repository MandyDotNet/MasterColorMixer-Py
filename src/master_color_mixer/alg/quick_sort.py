from typing import List, TypeVar

T = TypeVar("T")

# In the workplace, we would normally have 
# a public wrapper function + a private helper function 
# but that seems silly to implement for this project right now. 

def quick_sort(arr: List[T]) -> List[T]:

    # base case: already sorted
    if len(arr) <= 1:
        return arr[:] # shallow copy https://www.w3schools.com/python/python_lists_copy.asp 
    
    pivot_index = len(arr) // 2 # choose middle index as pivot
    pivot = arr[pivot_index]

    # partition elements into three groups
    less: List[T] = []
    equal: List[T] = []
    greater: List[T] = []

    for item in arr:
        if item < pivot:
            less.append(item)
        elif item > pivot:
            greater.append(item)
        else:
            equal.append(item)

    # recursively sort left and right sides
    return quick_sort(less) + equal + quick_sort(greater)

