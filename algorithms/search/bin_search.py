def binary_search(arr: list[int], search_el: int) -> int:
    low = 0
    high = len(arr) - 1
    mid = high // 2

    while low <= high:

        if arr[mid] == search_el:
            return mid

        if arr[mid] < search_el:
            low = mid + 1
        else:
            high = mid - 1

        mid = (low + high) // 2

    return -1


def binarySearch(arr, x, left, right):
    if right <= left:  # промежуток пуст
        return -1
    # промежуток не пуст
    mid = (left + right) // 2
    if arr[mid] == x:  # центральный элемент — искомый
        return mid
    elif x < arr[mid]:  # искомый элемент меньше центрального значит следует искать в левой половине
        return binarySearch(arr, x, left, mid)
    else:  # иначе следует искать в правой половине
        return binarySearch(arr, x, mid + 1, right)




def test_binary_search(func):
    # Test case 1: Element is present in the array
    assert func([1, 3, 5, 7, 9], 5) == 2  # Element 5 should be at index 2

    # Test case 2: Element is not present in the array
    assert func([1, 2, 4, 6, 8], 3) == -1  # Element 3 not in the array

    # Test case 3: Empty array
    assert func([], 1) == -1  # Searching in an empty array should return -1

    # Test case 4: Single element present
    assert func([10], 10) == 0  # The single element matches the target

    # Test case 5: Single element absent
    assert func([20], 10) == -1  # The single element doesn't match the target

    # Test case 6: Element in the left half of the array
    assert func([10, 20, 30, 40, 50], 20) == 1  # Element in the left side

    # Test case 7: Element in the right half of the array
    assert func([10, 20, 30, 40, 50], 40) == 3  # Element in the right half

    # Test case 8: Element is the first in the array
    assert func([5, 10, 15, 20, 25], 5) == 0  # Target is the first element

    # Test case 9: Element is the last in the array
    assert func([5, 10, 15, 20, 25], 25) == 4  # Target is the last element
    # assert func([5, 10, 15, 20, 25], 0) == -1  # Target is the last element


test_binary_search(binary_search)
