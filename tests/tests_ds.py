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

def test_dynamic_array_pop_empty_error():
    da = DynamicArray[int]()
    with pytest.raises(IndexError): #assert what error should occur
        da.pop()
#--> edge case covered: attempting pop of empty DynamicArray


#-- Test Stack --
def test_stack_push_pop_peek_len_isEmpty():
    stak = Stack[int]()
    assert stak.is_empty()
    
    #fill the stack and use push, is_empty, __len__ and peek methods
    for i in range(5):
        stak.push(i)
        assert not stak.is_empty()
        assert len(stak) == 1 + 1
        assert stak.peek() == i #top of stack should be the last one pushed

    #pop in LIFO order, verify pop method
    for expectedStack in reversed(range(5)):
        assert stak.peek() == expectedStack
        x = stak.pop() #pop and return popped item
        assert x == expectedStack

    assert stak.is_empty()
    assert len(stak) == 0
#--> edge case covered: clear Stack

def test_stack_pop_and_peek_empty_raises():
    stak = Stack[int]()
    with pytest.raises(IndexError):
        stak.pop()
    with pytest.raises(IndexError):
        stak.peek()
#--> edge case covered : 


#-- Test RingBufferQueue --


#-- Test HashSet --

#add

#remove

#contains

#__len__