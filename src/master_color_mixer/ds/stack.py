# with push, pop, peek, is_empty (wrap python list)

class Stack:

    def __init__(self, items = None):

        if items is None:
            self._data = []
        else:
            self._data = list(items)