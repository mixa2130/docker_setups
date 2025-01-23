* [Patroni](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#patroni)
* [SQL](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#sql)
    * [Работа с датами](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#работа-с-датами)
    * [Фичи](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#фичи)
        * [Record](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#record)
        * [Using](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#using)
        * [Unnest](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#unnest)
        * [Coalesce](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#coalesce)
        * [CASE WHEN](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#case-when)
        * [CTE](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#cte)
        * [Выбор из массива данных](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#выбор-из-массива-данных)
    * [Оконные функции](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#оконные-функции)
        * [ROWS BETWEEN](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#rows-between)
        * [Aggregate vs window functions](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#aggregate-vs-window-functions)
        * [Functions](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#functions)
            * [Rank vs Dense_rank](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#rank-vs-dense_rank)
            * [NTILE](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#ntile)
            * [LAG и LEAD](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#lag-и-lead)
        * [Rolling Sum](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#rolling-sum)
    * [Lateral Join](https://github.com/mixa2130/docker_setups/blob/master/postgresql/README.md#lateral-join)

# Patroni

[Создание кластера Patroni](https://www.linode.com/docs/guides/create-a-highly-available-postgresql-cluster-using-patroni-and-haproxy/)

<img src="images/patroni-etcd-pgbouncer-haproxy-schema.png" width="770" height="540" />

# SQL

## Работа с датами

~~~postgresql
SELECT *
FROM TABLE
WHERE EXTRACT(month from created_at) = 2
  AND EXTRACT(year from created_at) = 2020
~~~

~~~postgresql
SELECT *
FROM MovieRating
WHERE TO_CHAR(created_at, 'yyyy-mm') = '2020-02'
~~~

Сделает datetime: `+00:00:00`

~~~postgresql
SELECT created_at + interval '1' day
FROM smth
~~~

Просто добавить дни:

~~~postgresql
SELECT created_at + 6
FROM smth
~~~

## Фичи

### LEFT AND RIGHT

~~~sql
LEFT(string, number_of_characters)
RIGHT(string, number_of_characters)
~~~
* `string`: The text string whose leftmost or rightmost characters you want to extract. This can be a field name or a
literal string.
* `number_of_characters`: This is a positive integer that dictates how many characters from the start (left) or end (right)
of the text string will be extracted.

~~~postgresql
SELECT 
    LEFT('MARRY ANN', 1)
-- M
~~~


### Record

~~~
postgres=# SELECT table1 FROM table1;
 table1  
---------
 (1,2,3)
 (2,3,4)
~~~

Все строки, значения которых нету во второй таблице:

~~~postgresql
SELECT *
FROM table1
WHERE NOT EXISTS (SELECT *
                  FROM table2
                  WHERE table2 = table1)
~~~

### Using

~~~
JOIN Table2 b ON a.id = b.id
~~~

<=>

~~~
JOIN Table2 b USING(id)
~~~

### Unnest

Создаст атрибут из массива

~~~postgresql
INSERT INTO important_user_table
    (id, date_added, status_id)
SELECT unnest(array [100, 110, 153, 100500]),
       '2015-01-01',
       3;
~~~

что <=>

~~~postgresql
INSERT INTO important_user_table
    (id, date_added, status_id)
VALUES (100, '2015-01-01', 3),
       (110, '2015-01-01', 3),
       (153, '2015-01-01', 3),
       (100500, '2015-01-01', 3);
~~~

### Coalesce

The COALESCE() function accepts a list of arguments and returns the first non-null argument.

~~~postgresql
SELECT coalesce(
               ROUND(cnt * 1.0 / all_cnt, 2),
               0) 
~~~

Если ROUND вернёт NULL, то он заменится на 0.

### CASE WHEN

~~~sql
select sum(
               case
                   when student_id is not NULL THEN 1
                   when student_id != 'JAMES' THEN -1
                   ELSE 0
                   END)
           as attended_exams
~~~

### CTE

Use only at PostgreSQL 12+

[PostgreSQL 11 issue](https://hakibenita.com/be-careful-with-cte-in-postgre-sql)

~~~postgresql
WITH cte_products_wt_dates AS (SELECT product_id,
                                      MAX(change_date) as change_date
                               FROM Products
                               WHERE change_date <= '2019-08-17'
                               GROUP BY product_id),
     cte_default_prices AS (SELECT DISTINCT product_id,
                                            10 as price
                            FROM Products)
~~~

### Выбор из массива данных, а не из таблицы

~~~postgresql
SELECT *
FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three')) as t (digit_number, string_number);
~~~

~~~
 digit_number | string_number 
--------------+---------------
            1 | one
            2 | two
            3 | three
~~~

## Оконные функции

~~~sql
SELECT {columns}, 
       {window_func} OVER (
                    PARTITION BY {partition_key} 
                    ORDER BY {order_key}
                                       ROWS BETWEEN/ RANGE BETWEEN
                )
FROM table1;
~~~

Если у вас много одинаковых выражений после OVER, то можно дать им имя и вынести отдельно с ключевым словом WINDOW:

~~~postgresql
SELECT sum(salary) OVER w,
       avg(salary) OVER w
FROM empsalary
WINDOW w AS (PARTITION BY depname ORDER BY salary DESC);
~~~

### ROWS BETWEEN

While `PARTITION BY` divides the dataset into groups for separate calculations, while the `ROWS BETWEEN` clause enables
calculations over a moving window of rows that adjusts based on the position of the current row.

1. Все, что до текущей строки/диапазона и само значение текущей строки

   `BETWEEN UNBOUNDED PRECEDING`

   `BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`
2. Текущая строка/диапазон и все, что после нее

   `BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING`
3. С конкретным указанием сколько строк до и после включать (не поддерживается для RANGE)

   `BETWEEN N Preceding AND N Following`

   `BETWEEN CURRENT ROW AND N Following`

   `BETWEEN N Preceding AND CURRENT ROW`

<img src="images/rowsbetween.png" width="970" height="240" />

### Aggregate vs window functions

<img src="images/aggregateVsWindowFuncs.jpg" width="570" height="340" />

Оконные функции, как и агрегатные функции, работают с множеством строк, называемым рамкой окна.
В отличие от агрегатных функций, оконные функции возвращают единственное значение для каждой строки рассматриваемого
запроса.

Окно определяется с использованием предложения OVER(). Оно позволяет задать окно на основе конкретного столбца, подобно
GROUP BY в случае агрегатных функций.
Вы можете использовать агрегатные функции с оконными функциями, но вам нужно будет использовать их с предложением
OVER().

### Functions

| Function      | Explanation                                                                                                                                                 | 
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ранжирование  |                                                                                                                                                             |
| ROW_NUMBER()  | Assigns a unique sequential integer to each row within the partition.                                                                                       | 
| RANK()        | Также нумирует строки. В отличии от ROW_NUMBER строкам с одинаковыми значениям присваивает тот же номер. При этом сам номер продолжит расти автоинкрементом | 
| DENSE_RANK()  | Тоже самое что и RANK, только продолжает нумерацию                                                                                                          | 
| NTILE()       | Распределить что-то по группам                                                                                                                              | 
| Аналитические | Вычисляют значения на базе движущегося окна строк                                                                                                           | 
| LAG()         | Значение выражения, вычисленного для предыдущей строки. Если строки не существует - используется NULL. Можно поменять, с помощью 3го параметра              | 
| LEAD()        | Значение выражения, вычисленного для следующей строки. Если строки не существует - используется NULL. Можно поменять, с помощью 3го параметра               | 
| FIRST_VALUE() | Возвращает первое из упорядоченного набора значений                                                                                                         | 
| LAST_VALUE()  | Возвращает последнее из упорядоченного набора значений                                                                                                      | 

#### Rank vs Dense_rank

Rank:

~~~
1	1
5	2
6	3
6	3
6	3
13	6
~~~

Dense_Rank:

~~~
1	1
5	2
6	3
6	3
6	3
13	4
~~~

#### NTILE

<img src="images/ntile.png" width="770" height="570" />

#### LAG и LEAD

`FUNC(attr, n, default_val)`  где n - это шаг, определяющий количество строк назад

Просто берёт предыдущую строку:

<img src="images/lag_lead.png" width="770" height="570" />

Добавим различение по группам в виде гендера

<img src="images/lag_lead_group.png" width="770" height="570" />

### Rolling Sum

~~~sql
SELECT person_name,
       SUM(weight) OVER (
           ORDER BY turn
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as rolling_sum
FROM Queue
~~~

~~~
| person_name | weight | rolling_sum |
| ----------- | ------ | ----------- |
| Alice       | 250    | 250         |
| Alex        | 350    | 600         |
| John Cena   | 400    | 1000        |
| Marie       | 200    | 1200        |
| Bob         | 175    | 1375        |
| Winston     | 500    | 1875        |
~~~

~~~
+-------------+------+
| category | accounts_count|
+-------------+------+
| 1 | 0 |
| 2 | 0 |
+-------------+------+
~~~

## Lateral Join

Подзапрос, используемый с LATERAL, выполняется для каждой строки из таблицы, находящейся слева от LATERAL JOIN. Этот
подзапрос может использовать значения из текущей строки левой таблицы.

~~~postgresql
SELECT *
FROM left_table
         JOIN LATERAL ( subquery) AS alias
ON condition;
~~~

Представьте, что у нас есть две таблицы:
• users (содержит пользователей)
• orders (содержит заказы, связанные с пользователями)

Если мы хотим получить самый последний заказ для каждого пользователя, без LATERAL это было бы сложнее:

~~~postgresql
SELECT u.*, o.*
FROM users u
         JOIN (SELECT DISTINCT ON (user_id) *
               FROM orders
               ORDER BY user_id, created_at DESC) o ON u.id = o.user_id;
~~~

С помощью LATERAL мы можем упростить запрос:

~~~postgresql
SELECT u.*, o.*
FROM users u
         JOIN LATERAL (
    SELECT *
    FROM orders
    WHERE orders.user_id = u.id
    ORDER BY created_at DESC
    LIMIT 1
    ) o ON true;
~~~

Объяснение:

* Для каждой строки в users (alias u), подзапрос внутри LATERAL ищет заказы, принадлежащие конкретному пользователю (
  orders.user_id = u.id).
* ORDER BY created_at DESC и LIMIT 1 обеспечивают выбор самого последнего заказа.
* ON true используется, так как условие соединения уже реализовано внутри подзапроса.

# Интересные подходы к решению задач

## Скользящее окно без оконной функции

https://leetcode.com/problems/restaurant-growth/?envType=study-plan-v2&envId=top-sql-50

~~~
Input: 
Customer table:
+-------------+--------------+--------------+-------------+
| customer_id | name         | visited_on   | amount      |
+-------------+--------------+--------------+-------------+
| 1           | Jhon         | 2019-01-01   | 100         |
| 2           | Daniel       | 2019-01-02   | 110         |
| 3           | Jade         | 2019-01-03   | 120         |
| 4           | Khaled       | 2019-01-04   | 130         |
| 5           | Winston      | 2019-01-05   | 110         | 
| 6           | Elvis        | 2019-01-06   | 140         | 
| 7           | Anna         | 2019-01-07   | 150         |
| 8           | Maria        | 2019-01-08   | 80          |
| 9           | Jaze         | 2019-01-09   | 110         | 
| 1           | Jhon         | 2019-01-10   | 130         | 
| 3           | Jade         | 2019-01-10   | 150         | 
+-------------+--------------+--------------+-------------+
Output: 
+--------------+--------------+----------------+
| visited_on   | amount       | average_amount |
+--------------+--------------+----------------+
| 2019-01-07   | 860          | 122.86         |
| 2019-01-08   | 840          | 120            |
| 2019-01-09   | 840          | 120            |
| 2019-01-10   | 1000         | 142.86         |
+--------------+--------------+----------------+
~~~

Compute the moving average of how much the customer paid in a seven days window (i.e., current day + 6 days before).
average_amount should be rounded to two decimal places.

Чтобы собрать скользящее окно можно сделать:

1) через оконную функцию:

~~~postgresql
SELECT SUM(amount) OVER seven_days_window as amount,
       ROUND(
                       AVG(amount) OVER seven_days_window,
                       2)                 as average_amount
FROM cte_grouped_amount
WINDOW seven_days_window AS (ROWS BETWEEN CURRENT ROW AND 6 FOLLOWING)
~~~

2) Самому собрать окно

~~~postgresql
-- Интервал с конечными датами
WITH last_6_days AS (SELECT DISTINCT visited_on
                     FROM Customer
                     ORDER BY visited_on ASC
                     OFFSET 6)
-- +--------------+
-- | 2019-01-07   |
-- | 2019-01-08   |
-- | 2019-01-09   |
-- | 2019-01-10   |
-- +--------------+
SELECT *
FROM last_6_days c1
         JOIN Customer c2
              ON c2.visited_on
--                Интервал: [на 6 дней раньше от текущей конечной и текущей]
                  BETWEEN c1.visited_on - 6 AND c1.visited_on
ORDER BY c1.visited_on
-- +--------------+
-- | 2019-01-07 | 2019-01-01 |
-- | 2019-01-07 | 2019-01-02 |
-- | 2019-01-07 | 2019-01-03 |
-- | 2019-01-07 | 2019-01-04 |
-- | 2019-01-07 | 2019-01-05 |
-- | 2019-01-07 | 2019-01-06 |
-- | 2019-01-07 | 2019-01-07 |
-- | 2019-01-08 | 2019-01-02 |
~~~