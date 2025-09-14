class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def dfs_preorder(root):
    """
    Pre-order: корень -> левое -> правое.
    Верни список значений в порядке обхода.
    """
    visited = []

    if root is None:
        return visited

    visited.append(root.value)

    visited += dfs_preorder(root.left)
    visited += dfs_preorder(root.right)

    return visited


def dfs_inorder(root):
    """
    In-order: левое -> корень -> правое.
    Верни список значений в порядке обхода.
    """
    #        1
    #       / \
    #      2   3
    #     / \   \
    #    4   5   6

    visited = []

    if root is None:
        return visited

    visited += dfs_inorder(root.left)

    visited.append(root.value)

    visited += dfs_inorder(root.right)

    return visited


def dfs_postorder(root):
    """
    Post-order: левое -> правое -> корень.
    Верни список значений в порядке обхода.
    """
    visited = []

    if root is None:
        return visited

    visited += dfs_postorder(root.left)
    visited += dfs_postorder(root.right)

    visited.append(root.value)
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
    assert dfs_preorder(t1) == [1, 2, 4, 5, 3, 6]
    assert dfs_inorder(t1) == [4, 2, 5, 1, 3, 6]
    assert dfs_postorder(t1) == [4, 5, 2, 6, 3, 1]

    # Тест 2: только корень
    t2 = Node(10)
    assert dfs_preorder(t2) == [10]
    assert dfs_inorder(t2) == [10]
    assert dfs_postorder(t2) == [10]

    # Тест 3: цепочка влево (несбалансированное)
    # 1 -> 2 -> 3 -> 4
    t3 = Node(1, Node(2, Node(3, Node(4))))
    assert dfs_preorder(t3) == [1, 2, 3, 4]
    assert dfs_inorder(t3) == [4, 3, 2, 1]
    assert dfs_postorder(t3) == [4, 3, 2, 1]

    # Тест 4: широкий уровень
    #        7
    #      /   \
    #     8     9
    #    / \   /
    #   10 11 12
    t4 = Node(7,
              Node(8, Node(10), Node(11)),
              Node(9, Node(12)))
    assert dfs_preorder(t4) == [7, 8, 10, 11, 9, 12]
    assert dfs_inorder(t4) == [10, 8, 11, 7, 12, 9]
    assert dfs_postorder(t4) == [10, 11, 8, 12, 9, 7]

    # Тест 5: пустое дерево
    t5 = None
    assert dfs_preorder(t5) == []
    assert dfs_inorder(t5) == []
    assert dfs_postorder(t5) == []


if __name__ == "__main__":
    run_tests()
    print("✅ Все тесты пройдены!")
