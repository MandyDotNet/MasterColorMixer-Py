from master_color_mixer.adapters.alg import (
    binary_search,
    merge_sort,
    quick_sort,
)


def test_merge_sort_numbers_does_not_mutate():
    data = [5, 3, 8, 1, 2]
    result = merge_sort(data)

    assert result == [1, 2, 3, 5, 8] # should return a sorted copy
    assert data == [5, 3, 8, 1, 2] # original list should change


def test_quick_sort_numbers_does_not_mutate():
    data = [7, 4, 9, 1, 0, 4]
    result = quick_sort(data)

    assert result == sorted(data)
    assert data == [7, 4, 9, 1, 0, 4] # original list should change


def test_merge_sort_strings():
    colors = ["yellow", "red", "blue", "green"]
    result = merge_sort(colors)

    assert result == ["blue", "green", "red", "yellow"]


def test_quick_sort_strings():
    colors = ["yellow", "red", "blue", "green"]
    result = quick_sort(colors)

    assert result == sorted(colors) # should match Python's sort


def test_binary_search_found_middle():
    #case: target is in middle
    data = [1, 3, 5, 7, 9]
    idx = binary_search(data, 5)

    assert idx == 2 # correct position
    assert data[idx] == 5 # correct value


def test_binary_search_found_edges():
    #case: target is on either end of list (confirms correct conditional checks)
    data = [2, 4, 6, 8]

    assert binary_search(data, 2) == 0
    assert binary_search(data, 8) == 3


def test_binary_search_not_found():
    #case: target is not in list
    data = [10, 20, 30, 40]
    idx = binary_search(data, 25)

    assert idx == -1    #-1 means not found