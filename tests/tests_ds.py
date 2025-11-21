import pytest

from src.master_color_mixer.ds import DynamicArray, Stack, RingBufferQueue, HashSet

#-- Test DynamicArray --
def test_dynamic_array_append_getitem_setitem_pop_len():
    theDA = DynamicArray[int]()

    #insert items in the dynamic array
    for i in range(10):
        theDA.append(i) # uses the append method to assign values to each index
        assert len(theDA) == i + 1 # uses the __len__ method
        assert theDA[i] == i # uses the __getitem__ method

    theDA[5] = 99 # uses the __setitem__ method
    assert theDA[5] == 99

    #pop removes from the end, popping should happen in reverse order (LIFO)
    for expectedValue in reversed(range(10)): # we expect (9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
        value = theDA.pop() # uses the pop method to remove the last element
        if expectedValue == 5:
            assert value == 99 # originally this was 5, but was changed to 99, so this is actually the value popped
        else:
            assert value == expectedValue

    assert len(theDA) == 0 # uses the __len__ method to assert that after 10 pops, all items are gone
#--> edge cases covered: overwrite at an index, clearing the DynamicArray object

def test_dynamic_array_pop_empty_IndexError():
    da = DynamicArray[int]()
    with pytest.raises(IndexError): # assert what error should occur
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
        assert len(stak) == i + 1
        assert stak.peek() == i # top of stack should be the last one pushed

    #pop in LIFO order, verify pop method
    for expectedStack in reversed(range(5)):
        assert stak.peek() == expectedStack
        x = stak.pop() # pop and return popped item
        assert x == expectedStack

    assert stak.is_empty()
    assert len(stak) == 0
#--> edge case covered: clear Stack

def test_stack_pop_peek_empty_IndexError():
    stak = Stack[int]()
    with pytest.raises(IndexError):
        stak.pop()
    with pytest.raises(IndexError):
        stak.peek()
#--> edge case covered : 


#-- Test RingBufferQueue --
def test_queue_enqueue_dequeue_isEmpty_len_():
    que = RingBufferQueue[int]()  # default capacity is 8

    #enqueue items over 8 
    values = list(range(20))
    for v in values:
        que.enqueue(v)  # when v = 8, resize makes capacity 16; when v = 16 -> capacity is 32

    assert len(que) == 20   # verify the number of stored elements
    assert not que.is_empty() # redundant assert
    # I did not write a capacity helper, so we cannot test that the internal array capacity is 32.

    #dequeue first 10, should be in FIFO order
    first_batch = [que.dequeue() for _ in range(10)]
    assert first_batch == values[:10] # verify up to index 10 that values match
    assert len(que) == 10   #check that we drained half the queue

    #drain the rest
    remaining = [que.dequeue() for _ in range(len(que))]
    assert remaining == values[10:] # verify the last 10 values
    assert que.is_empty()

def test_queue_empty_dequeue_peek_IndexError():
    q = RingBufferQueue[int]()
    with pytest.raises(IndexError):
        q.dequeue()
    with pytest.raises(IndexError):
        q.peek()

#-- Test HashSet --
def test_hashset_add_contains_remove_len():
    hashs = HashSet[int]()

    for x in [1, 2, 3, 3, 2]:
        hashs.add(x)

    assert len(hashs) == 3  # confirm that duplicates did not increase length
    for y in [1, 2, 3]:
        assert hashs.contains(y)

    hashs.remove(2)
    assert len(hashs) == 2
    assert not hashs.contains(2)

    with pytest.raises(KeyError):  # calling with a non-valid Key should throw a KeyError
        hashs.remove(999)