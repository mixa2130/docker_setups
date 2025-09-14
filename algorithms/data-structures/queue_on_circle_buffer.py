class MyQueueSize:

    def __init__(self, max_size: int):
        self.max_n = max_size
        self.queue = [None] * self.max_n
        self.head = 0
        self.tail = 0
        self.size = 0

    def push(self, x) -> bool:
        if self.size == self.max_n:
            return False

        self.queue[self.tail] = x
        self.tail = (self.tail + 1) % self.max_n
        self.size += 1
        return True

    def pop(self):
        if self.size == 0:
            return None

        val = self.queue[self.head]
        self.queue[self.head] = None
        self.head = (self.head + 1) % self.max_n
        self.size -= 1
        return val

    def peek(self):
        return self.queue[self.head]

    def queue_size(self):
        return self.size