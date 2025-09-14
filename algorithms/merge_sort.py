def merge_sort(array):
    if len(array) == 1:  # базовый случай рекурсии
        return array

    # запускаем сортировку рекурсивно на левой половине
    left = merge_sort(array[0: len(array) // 2])

    # запускаем сортировку рекурсивно на правой половине
    right = merge_sort(array[len(array) // 2: len(array)])

    # заводим массив для результата сортировки
    result = [0] * len(array)

    # сливаем результаты
    l, r, k = 0, 0, 0
    while l < len(left) and r < len(right):
        # выбираем, из какого массива забрать минимальный элемент
        if left[l] <= right[r]:
            result[k] = left[l]
            l += 1
        else:
            result[k] = right[r]
            r += 1
        k += 1

    # Если один массив закончился раньше, чем второй, то
    # переносим оставшиеся элементы второго массива в результирующий
    while l < len(left):
        result[k] = left[l]  # перенеси оставшиеся элементы left в result
        l += 1
        k += 1
    while r < len(right):
        result[k] = right[r]  # перенеси оставшиеся элементы right в result
        r += 1
        k += 1

    return result


def merge(arr, lf, mid, rg):
    res: list[int] = []
    idx_1: int = lf
    idx_2: int = mid

    while idx_1 < mid and idx_2 < rg:
        if arr[idx_1] < arr[idx_2]:
            res.append(arr[idx_1])
            idx_1 += 1
        else:
            res.append(arr[idx_2])
            idx_2 += 1

    if idx_2 < rg:
        res += arr[idx_2:rg]
    elif idx_1 < mid:
        res += arr[idx_1: mid]

    return res


def merge_sort(arr, lf, rg):
    if rg - lf >= 2:
        mid = (lf + rg) // 2
        merge_sort(arr, lf, mid)
        merge_sort(arr, mid, rg)
        arr[lf:rg] = merge(arr, lf, mid, rg)
