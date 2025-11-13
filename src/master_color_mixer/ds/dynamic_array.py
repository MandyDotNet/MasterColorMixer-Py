# with append, pop, __getitem__, __setitem__, __len__ (wrap python list)
# to support API

class DynamicArray():

    # initializer (constructor)
    def __init__(self, initial = None): #if given make a copy as list, otherwise start empty list
        
        if initial is None:
            self._data = []
        else:
            self._data = list(initial)
