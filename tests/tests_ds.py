import pytest

from src.mastercolormixer.ds import DynamicArray, Stack, RingBufferQueue, HashSet

#-- Test DynamicArray --
def test_dynamic_array_append_getitem_setitem_pop_and_len():
    theDA = DynamicArray[int]()

    #insert items in the dynamic array
    for i in range(10):
        theDA.append(i) #uses the append method to assign values to each index
        assert len(theDA) == i + 1 #uses the __len__ method
        assert theDA[i] == i #uses the __getitem__ method

    theDA[5] = 99 #uses the __setitem__ method
    assert theDA[5] == 99

    #pop removes from the end, popping should happen in reverse order (LIFO)
    for expectedValue in reversed(range(10)): #we expect (9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
        value = theDA.pop() #uses the pop method to remove the last element
        if expectedValue == 5:
            assert value == 99 #originally this was 5, but was changed to 99, so this is actually the value popped
        else:
            assert value == expectedValue

    assert len(theDA) == 0 #uses the __len__ method to assert that after 10 pops, all items are gone
#--> edge cases covered: overwrite at an index, clearing the DynamicArray object


#-- Test Stack --

#push

#pop

#peek

#is_empty

#__len_


#-- Test RingBufferQueue --

#enqueue

#dequeue

#peek

#is_empty

#__len__


#-- Test HashSet --

#add

#remove

#contains

#__len__