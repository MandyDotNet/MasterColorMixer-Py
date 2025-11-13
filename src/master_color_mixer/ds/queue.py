# with enqueue, dequeue, peek, is_empty, __len__ (fixed-growth: 8 then double on overflow)

from typing import Generic, List, TypeVar

T = TypeVar("T")

class RingBufferQueue:
    # FIFO queue, a circular buffer that doubles on overflow
    # Source: https://runestone.academy/ns/books/published/pythonds/BasicDS/toctree.html
    # FIFO and queue - 4.10, 4.11
    # enqueue and dequeue and things to avoid - 4.12
    # circular logic - 4.15, 4.16, 4.17
    # resizing, doubling, and copying - 4.19

    # reuse the same list, wrapping instead of shifting
    # _size is never negative and never bigger than capacity

    def __init__(self, capacity = 8):

        # validate
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")

        # create class list with empty placeholders
        self._data = [None] * capacity

        # ensure head, tail, and number of elements initialized
        self._head = 0 #next dequeue/peek
        self._tail = 0 #next enqueue
        self._size = 0 #valid elements

# I like to place functional methods at the top of the class
    
    def enqueue(self, item: T) -> None:
        # if the number of items equals capacity, buffer full
        if self._size == len(self._data):
            self._resize(len(self._data) * 2) #double and copy

        self._data[self._tail] = item
        self._tail = (self._tail + 1) % len(self._data)
        self._size += 1
        # no return needed as we already know the queue upon request

    def dequeue(self) -> T:
        if self._size == 0:
            raise IndexError("Cannot dequeue from empty RingBufferQueue")
        item = self._data[self._head] #current front element

        self._data[self._head] = None #clear current front element
        self._head = (self._head + 1) % len(self._data) #move head forward, wrapping at the end
        self._size -= 1
        #return the removed element - a primary operation standard for Queue Abstract Data Type
        return item

# I like to place helper methods after functional methods
    
    #double capacity and re-order elements so order is preserved
    def _resize(self, new_cap: int) -> None:
        assert new_cap >= self._size
        new_data = [None] * new_cap

        # preserve FIFO order (loop front to back)
        for i in range(self._size):
            new_data[i] = self._data[(self._head + i) % len(self._data)]

        self._data = new_data
        self._head = 0
        self._tail = self._size