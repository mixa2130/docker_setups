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

## Фичи

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
JOIN LATERAL (subquery) AS alias ON condition;
~~~

Представьте, что у нас есть две таблицы:
	•	users (содержит пользователей)
	•	orders (содержит заказы, связанные с пользователями)

Если мы хотим получить самый последний заказ для каждого пользователя, без LATERAL это было бы сложнее:

~~~postgresql
SELECT u.*, o.*
FROM users u
JOIN (
    SELECT DISTINCT ON (user_id) *
    FROM orders
    ORDER BY user_id, created_at DESC
) o ON u.id = o.user_id;
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
	* Для каждой строки в users (alias u), подзапрос внутри LATERAL ищет заказы, принадлежащие конкретному пользователю (orders.user_id = u.id).
	* ORDER BY created_at DESC и LIMIT 1 обеспечивают выбор самого последнего заказа.
	* ON true используется, так как условие соединения уже реализовано внутри подзапроса.