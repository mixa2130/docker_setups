# Поиск

## Бинарный поиск

~~~python
def binary_search_iterative(arr, target):
    # Определить границы поиска
    left, right = 0, len(arr) - 1
    while left <= right:
        # Вычислить серединный индкс
        mid = left + (right - left) // 2
        # Если средний элемент является искомым, вернуть его индекс
        if arr[mid] == target:
            return mid
            # Если искомый элемент больше, сузить поиск до правой половины
        elif arr[mid] < target:
            left = mid + 1
            # Если искомый элемент меньше, сузить поиск до левой половины
        else:
            right = mid - 1
            # Вернуть -1, если цель не найдена
    return -1 
~~~

# Сортировка двух отсортированных массивов

## Сортировка слияниями (N logN)

https://habr.com/ru/articles/281675/
https://www.youtube.com/watch?v=wQMSowIS2FY&ab_channel=Фоксфорд

В общем виде:

1) делим массив пополам
2) сортируем половинки
3) методом слияния объединяем в единый `O(k+n)`

~~~python
res = []
i, j = 0, 0  # индексы массивов nums1 и nums2

while i < m and j < n:
    if nums1[i] == nums2[j]:
        res.append(nums1[i])
        res.append(nums2[j])

        i += 1
        j += 1
        continue

    if nums1[i] < nums2[j]:
        res.append(nums1[i])
        i += 1
    else:
        res.append(nums2[j])
        j += 1

if j < n:
    res += nums2[j:]
if i < m:
    res += nums1[i:m]
~~~

# Интересные задачи

##  Разложение на множители

Решается за О(sqrt(n)).

Пусть n = 36. Его делители по парам:
• 1 x 36
• 2 x 18
• 3 x 12
• 4 x 9
• 6 x 6

После 6, делители начинают повторяться в обратном порядке. То есть, если ты проверил делители до sqrt{n}, ты уже
фактически проверил всё.

~~~python
def Factor(n):
    Ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            Ans.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        Ans.append(n)
    return Ans
~~~