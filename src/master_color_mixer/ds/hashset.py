# with add, remove, contains, __len__ (compose Python set)

class HashSet:

    def __init__(self, items = None):

        #class set
        if items is None:
            self._set = set()
        else:
            self._set = set(items) #dedicated class structure to call methods