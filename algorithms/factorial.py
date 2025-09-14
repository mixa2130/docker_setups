from functools import lru_cache


@lru_cache(maxsize=128)  # прихранить результаты функций в словарик
def factorial(n):
    if n == 1 or n == 0:
        return 1
    return n * factorial(n - 1)


assert factorial(5) == 5 * 4 * 3 * 2

# (Fn)       = (1 1) * (Fn-1)
# (Fn-1)       (1 0) * (Fn-2)
#           ^
#           =
# (1 1) ^ n  =  (Fn+1 Fn)
# (1 0)         (Fn Fn-1)


E_matrix = [[1, 0], [0, 1]]
BASE_matrix = [[1, 1], [1, 0]]


def matrix_multiply(A, B):
    """
    C[i][j] += A[i][k] * B[k][j]
    C[0][0] = A[0][0] * B[0][0] + A[0][1] * B[1][0]

    [1 1] * [1 1]
    [1 0]   [1 0]
    """

    # Нужно трансформировать B, чтобы в строке была колонка
    # zip([1, 2, 3], [4, 5, 6]) -> (1, 4), (2, 5), (3, 6)
    BT = list(zip(*B))
    C = []
    for row_a in A:
        c_row = []

        for col_b in BT:
            val = sum(a * b for a, b in zip(row_a, col_b))
            c_row.append(val)
        C.append(c_row)
    return C

def pow_matrix(mtrx, n):
    """
    Быстрое возведение матрицы в степень за O(log n)
    """
    if n == 0:
        return E_matrix
    if n == 1:
        return mtrx

    # Вычисляем половинную степень один раз
    half_pow = pow_matrix(mtrx, n // 2)

    if n % 2 == 0:
        # A^(2k) = (A^k)^2
        return matrix_multiply(half_pow, half_pow)
    else:
        # A^(2k+1) = A * (A^k)^2
        return matrix_multiply(mtrx, matrix_multiply(half_pow, half_pow))

res = pow_matrix(BASE_matrix, 10)
print(res)
print(res[0][1])