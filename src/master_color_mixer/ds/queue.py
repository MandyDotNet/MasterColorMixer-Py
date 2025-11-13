# with enqueue, dequeue, peek, is_empty, __len__ (fixed-growth: 8 then double on overflow)

class RingBufferQueue:

    def __init__(self, capacity = 8):

        # validate
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")

        # create class list with placeholders
        self._data = [None] * capacity

        # ensure head, tail, and number of elements initialized
        self._head = 0 #next dequeue
        self._tail = 0 #next enqueue
        self._size = 0 #valid elements

# helper method for resize will double capacity and re-order elements so order is preserved