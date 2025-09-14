"""
https://contest.yandex.ru/contest/22781/run-report/138202173/

-- ПРИНЦИП РАБОТЫ --
Класс `Dek` реализует структуру данных ДЕК на базе кольцевого двустороннего буфера фиксированного размера с поддержкой операций добавления и удаления элементов
как спереди (push_front, pop_front), так и сзади (push_back, pop_back).
Для реализации используется список фиксированного размера `_items` и два указателя: `head` (указывает на начало дека) и `tail`
(указывает на конец). Операции добавления/удаления зациклены в рамках длины буфера, что позволяет эффективно
перемещаться по внутреннему списку, не выходя за его границы.

-- ДОКАЗАТЕЛЬСТВО КОРРЕКТНОСТИ --
!! Есть тесты в `tests_dek.py` !!

1. Все операции корректно обрабатывают случаи переполнения и опустошения дека, через проверку размера дека (`_actual_size`).
2. Индексы `head` и `tail` обновляются с использованием операции взятия остатка по модулю, что обеспечивает циклическую работу
на фиксированном числе позиций.
3. Элементы добавляются только в свободное место, а удаляются только если дек содержит хотя бы один элемент.

-- ВРЕМЕННАЯ СЛОЖНОСТЬ --
Все операции `push_back`, `pop_back`, `push_front`, `pop_front` выполняются за O(1), так как затраты на добавление элементов
или удаление заключаются только в обновлении указателей `head`/`tail` и модификации фиксированного списка.

-- ПРОСТРАНСТВЕННАЯ СЛОЖНОСТЬ --
Пространственная сложность составляет O(N), где N — максимальный размер дека (`max_size`).
Память выделяется один раз при создании экземпляра класса, равная фиксированному размеру дека. Дополнительно используются
несколько переменных для хранения текущего размера `_actual_size`, указателей `head` и `tail`, а также значения по умолчанию `default_value`.
"""

from typing import Any


class DequeError(Exception):
    def __init__(self, description: str):
        super().__init__(description)


class DequeIsEmpty(DequeError):
    def __init__(self):
        super().__init__(description="Deque is empty")


class DequeIsFull(DequeError):
    def __init__(self):
        super().__init__(description="Deque is full")


class Deque:

    @property
    def size(self):
        return self._actual_size

    def __init__(self, dek_size: int):
        self.max_size = dek_size

        self.head = self.max_size - 1
        self.tail = 0

        self._actual_size = 0
        self._items = [None] * self.max_size

    def is_full(self):
        if self._actual_size == self.max_size:
            return True
        return False

    def is_empty(self):
        if self._actual_size == 0:
            return True
        return False

    def push_back(self, val: Any) -> bool:
        """
        При вставке tail идёт на +1 позицию (позицию возможной вставки)
        """
        if self.is_full():
            raise DequeIsFull

        self._actual_size += 1
        self._items[self.tail] = val

        # следующий для вставки элемент
        self.tail = (self.tail + 1) % self.max_size

        return True

    def pop_back(self) -> Any:
        """
        Так как tail идёт на +1 позицию, спускаемся до актуальной.
        После удаления не меняем позицию, так как теперь она свободная для вставки
        """
        if self.is_empty():
            raise DequeIsEmpty

        # элемент удаления
        self.tail = (self.tail - 1) % self.max_size

        val = self._items[self.tail]
        self._actual_size -= 1
        self._items[self.tail] = None

        return val

    def push_front(self, val: Any) -> bool:
        if self.is_full():
            raise DequeIsFull

        self._actual_size += 1
        self._items[self.head] = val

        # следующий для вставки элемент
        self.head = (self.head - 1) % self.max_size

        return True

    def pop_front(self) -> Any:
        if self.is_empty():
            raise DequeIsEmpty

        # элемент удаления
        self.head = (self.head + 1) % self.max_size

        val = self._items[self.head]
        self._actual_size -= 1
        self._items[self.head] = None

        return val

def process_command(dek: Deque, cmd: str):
    if cmd.find('pop') != -1:
        try:
            if cmd == 'pop_back':
                print(dek.pop_back())
            if cmd == 'pop_front':
                print(dek.pop_front())
        except DequeIsEmpty:
            print("error")
    else:
        push_cmd, value = cmd.split(' ')

        try:
            if push_cmd == 'push_back':
                dek.push_back(value)
            if push_cmd == 'push_front':
                dek.push_front(value)
        except DequeIsFull:
            print("error")

def main():
    n, m = int(input()), int(input())

    dek = Deque(m)

    for _ in range(n):
        cmd = input()
        process_command(dek, cmd)



if __name__ == '__main__':
    main()
