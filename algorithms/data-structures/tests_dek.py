import pytest

from dek import Deque, DequeIsEmpty, DequeIsFull


def test_push_front():
    dek = Deque(dek_size=5)

    dek.push_front(5)
    dek.push_front(7)
    dek.push_front(8)
    dek.push_front(12)
    dek.push_front(11)

    assert dek._items == [11, 12, 8, 7, 5]
    assert dek.size == 5

    # Пришли в начало дека с конца
    assert dek.head == 4
    # хвост без изменений, мы с него не двигались
    assert dek.tail == 0


def test_pop_front():
    # С начала
    dek = Deque(dek_size=5)

    with pytest.raises(DequeIsEmpty) as exc_info:
        dek.pop_front()
    assert "Deque is empty" in str(exc_info.value)

    dek.push_front(5)
    dek.push_front(7)
    dek.push_front(8)
    dek.push_front(12)
    dek.push_front(11)

    assert dek.pop_front() == 11
    assert dek._items == [None, 12, 8, 7, 5]
    assert dek.tail == 0
    assert dek.head == 0

    assert dek.pop_front() == 12
    assert dek.head == 1
    dek.pop_front()
    dek.pop_front()
    assert dek.pop_front() == 5
    assert dek.tail == 0
    assert dek.head == 4


def test_push_back():
    dek = Deque(dek_size=5)

    dek.push_back(11)
    dek.push_back(12)
    dek.push_back(8)
    dek.push_back(7)
    dek.push_back(5)

    assert dek._items == [11, 12, 8, 7, 5]
    assert dek.size == 5

    # Начало без изменений
    assert dek.head == 4
    # Пришли в конец списка
    assert dek.tail == 0


def test_pop_back():
    # с конца
    dek = Deque(dek_size=5)

    with pytest.raises(DequeIsEmpty) as exc_info:
        dek.pop_back()
    assert "Deque is empty" in str(exc_info.value)

    dek.push_back(11)
    dek.push_back(12)
    dek.push_back(8)
    dek.push_back(7)
    dek.push_back(5)

    assert dek.pop_back() == 5
    assert dek._items == [11, 12, 8, 7, None]
    assert dek.head == 4
    assert dek.tail == 4

    dek.pop_back()
    dek.pop_back()
    dek.pop_back()
    assert dek.pop_back() == 11

    assert dek.head == 4
    assert dek.tail == 0
    with pytest.raises(DequeIsEmpty) as exc_info:
        dek.pop_back()
    assert "Deque is empty" in str(exc_info.value)


def test_first():
    dek = Deque(4)
    dek.push_front(861)
    dek.push_front(-819)
    assert dek.pop_back() == 861
    assert dek.pop_back() == -819


def test_second():
    dek = Deque(10)
    dek.push_front(-855)
    dek.push_front(0)
    assert dek.pop_back() == -855
    assert dek.pop_back() == 0
    dek.push_back(844)
    assert dek.pop_back() == 844
    assert dek.push_back(823) is True

def test_third():
    dek = Deque(6)

    dek.push_front(-201)
    dek.push_back(959)
    dek.push_back(102)
    dek.push_front(20)

    assert dek.pop_front() == 20
    assert dek.pop_back() == 102


def test_push():
    dek = Deque(dek_size=5)

    dek.push_back(8)
    dek.push_back(12)
    dek.push_back(11)

    assert dek.size == 3
    assert dek.head == 4
    assert dek.tail == 3
    assert dek._items == [8, 12, 11, None, None]

    dek.push_front(7)
    dek.push_front(5)
    assert dek.size == 5
    assert dek._items == [8, 12, 11, 5, 7]

    assert dek.head == 2
    assert dek.tail == 3

    with pytest.raises(DequeIsFull) as exc_info:
        dek.push_back(13)
    assert "Deque is full" in str(exc_info.value)

    with pytest.raises(DequeIsFull) as exc_info:
        dek.push_front(13)
    assert "Deque is full" in str(exc_info.value)


def test_pop_back_till_the_end():
    dek = Deque(dek_size=5)
    dek.push_back(8)
    dek.push_back(12)
    dek.push_back(11)
    dek.push_front(7)
    dek.push_front(5)

    assert dek.pop_back() == 11
    assert dek._items == [8, 12, None, 5, 7]
    assert dek.head == 2
    assert dek.tail == 2

    dek.pop_back()
    dek.pop_back()
    assert dek._items == [None, None, None, 5, 7]
    assert dek.head == 2
    assert dek.tail == 0

    assert dek.pop_back() == 7
    assert dek.pop_back() == 5

    assert dek._items == [None] * 5
    assert dek.head == 2
    assert dek.tail == 3

    # 2nd iteration
    dek.push_back(8)
    dek.push_back(12)
    dek.push_back(11)
    dek.push_front(7)
    dek.push_front(5)
    assert dek._items == [11, 5, 7, 8, 12]
    assert dek.pop_back() == 11
