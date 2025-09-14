class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def dfs(root):
    """
    Здесь нужно будет реализовать обход в глубину (DFS).
    На вход подаётся корень бинарного дерева.
    Вернуть список значений в порядке обхода (например, pre-order).
    """
    stack = []
    visited = []
    if root is not None:
        stack.append(root)

    while stack:
        node = stack.pop()
        visited.append(node.value)

        if node.right is not None:
            stack.append(node.right)

        if node.left is not None:
            stack.append(node.left)

    return visited

# --- Тесты ---

def run_tests():
    # Тест 1: обычное дерево
    #        1
    #       / \
    #      2   3
    #     / \   \
    #    4   5   6
    t1 = Node(1,
              Node(2, Node(4), Node(5)),
              Node(3, None, Node(6)))

    assert dfs(t1) == [1, 2, 4, 5, 3, 6]  # ожидаем pre-order

    # Тест 2: только корень
    t2 = Node(10)
    assert dfs(t2) == [10]

    # Тест 3: цепочка влево
    # 1 -> 2 -> 3 -> 4
    t3 = Node(1, Node(2, Node(3, Node(4))))
    assert dfs(t3) == [1, 2, 3, 4]

    # Тест 4: широкий уровень
    #        7
    #      /   \
    #     8     9
    #    / \   /
    #   10 11 12
    t4 = Node(7,
              Node(8, Node(10), Node(11)),
              Node(9, Node(12)))
    assert dfs(t4) == [7, 8, 10, 11, 9, 12]

    # Тест 5: пустое дерево
    t5 = None
    assert dfs(t5) == []


if __name__ == "__main__":
    run_tests()
    print("✅ Все тесты пройдены!")