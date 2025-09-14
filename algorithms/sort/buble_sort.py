
def buble_sort(arr: list[int], n: int):

    for i in range(n):
        swapped = False

        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True

        if not swapped:
            # значит массив уже отсортирован
            break

    return arr


if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split(' ')))

    buble_sort(arr, n)