from collections import deque

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def bfs(root):
    """
    Здесь нужно будет реализовать BFS.
    На вход подаётся корень бинарного дерева.
    Возвращает список значений в порядке обхода.
    """
    queue = deque()
    queue.append(root)
    bfs_queue = []


    while queue:
        node = queue.popleft()
        bfs_queue.append(node.value)

        if node.left is not None:
            queue.append(node.left)

        if node.right is not None:
            queue.append(node.right)

    return bfs_queue

# --- Тесты ---

def run_tests():
    # Тест 1: обычное дерево
    #        1
    #       / \
    #      2   3
    #     / \   \
    #    4   5   6
    tree1 = Node(1,
                 Node(2, Node(4), Node(5)),
                 Node(3, None, Node(6)))
    assert bfs(tree1) == [1, 2, 3, 4, 5, 6]

    # Тест 2: только корень
    tree2 = Node(10)
    assert bfs(tree2) == [10]

    # Тест 3: цепочка (несбалансированное дерево)
    # 1 -> 2 -> 3 -> 4
    tree3 = Node(1, Node(2, Node(3, Node(4))))
    assert bfs(tree3) == [1, 2, 3, 4]

    # Тест 4: более широкий уровень
    #        7
    #      /   \
    #     8     9
    #    / \   /
    #   10 11 12
    tree4 = Node(7,
                 Node(8, Node(10), Node(11)),
                 Node(9, Node(12)))
    assert bfs(tree4) == [7, 8, 9, 10, 11, 12]


if __name__ == "__main__":
    run_tests()
    print("✅ Все тесты пройдены!")