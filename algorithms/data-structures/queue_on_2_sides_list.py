from typing import Any


class TwoSideListItem:
    def __init__(self, value, prev=None, next=None):
        self.prev = prev
        self.next = next
        self.value = value


class Queue:
    def __init__(self):
        self.queue_size = 0
        self.head: None | TwoSideListItem = None
        self.tail: None | TwoSideListItem = None

    def put(self, x):
        self.queue_size += 1

        if self.head is None:
            self.head = TwoSideListItem(value=x)
            self.tail = self.head
        else:
            item = TwoSideListItem(value=x, prev=self.tail)
            self.tail.next = item
            self.tail = item

    def size(self):
        return self.queue_size

    def get(self) -> Any:
        if self.head is None:
            return None

        val = self.head.value
        self.queue_size -= 1

        if self.head.next is not None:
            next_to_head = self.head.next
            next_to_head.prev = None
            self.head = next_to_head
        else:
            self.head = None
            self.tail = None

        return val