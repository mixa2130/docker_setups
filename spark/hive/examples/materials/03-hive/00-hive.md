### SQL over MapReduce. Hive

##### 1. Запуск оболочки Hive
Существует 3 основных вида запуска задач в Hive. Проверим их работу на команде `SHOW DATABASES` (показывает список существующих баз данных Hive).
* запуск с помощью интерактивной оболочки:

    ``` bash
    $ hive
    hive> SHOW DATABASES;
    ```
*  запуск внешней команды:
    ``` bash
    $ hive -e 'SHOW DATABASES'
    ```
* запуск внешнего файла:
    ``` bash
    $ echo 'SHOW DATABASES' > sh_db.sql # запись в файл
    hive -f sh_db.sql
    ```
Hive shell также позволяет запускать shell-команды внутри оболочки Hive. 
*После '__!__' не должно быть пробелов, после команды должна ставиться '__;__'*.
Попробуем получить кол-во виртуальных ядер на клиенте:
```bash
hive> !nproc;
```
Составные команды вроде `cat file | grep 'key' | tee new_file` hive shell не поддерживает.
Также можно из Hive shell работать с hdfs.
```bash
hive> dfs -ls;
```
##### 2. Создание базы данных
* Создадим тестовую БД.
    ``` bash
    hive> create database <YOUR_USER>_test location '/user/<YOUR_USER>/test_warehouse';
    ```
    При создании базы нужно указать **полный путь** к warehouse.
* Если вы указали неверное название базы или LOCATION, базу можно удалить:
    ``` bash
    hive> drop database if exists <YOUR_USER>_test cascade;
    ```
    Слово `CASCADE` отвечает за удаление базы вместе с её содержимым.
* Вывод информации о БД
    ``` bash
    hive> DESCRIBE DATABASE <YOUR_USER>_test
    ```
Выходим из Hive shell.

##### 3. Создание таблиц
Создадим таблицу в тестовой базе. Для исходных данных используем датасет "Подсети" (`/data/subnets/variant1`):
    * IP-адрес,
    * маска подсети, в которой он находится.

``` sql
USE <YOUR_USER>_test;
DROP TABLE IF EXISTS Subnets;

CREATE EXTERNAL TABLE Subnets (
    ip STRING,
    mask STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY  '\t'
STORED AS TEXTFILE
LOCATION '/data/subnets/variant1';
```
Пояснения
1. `USE ...` - подключение к базе данных. Без этой строки таблицы будут создаваться в базе "default". Также можно вместо `USE` использовать аргумент `--database` при запуске запроса.
2. `EXTERNAL` - существует 2 типа таблиц: managed и external. External-таблицы работают с внешними данными не изменяя их, а managed позволяют их изменять.
3. `STORED AS` здесь выбирается формат хранения таблицы. Для External-таблиц формат должен совпадать с форматом хранения данных. Для managed рекомендуется использовать сжатые форматы хранения (RCFile, AVRO и т.д.).

Записываем код в файл, сохраняемся и запускаем:
``` bash
hive -f my_query.hql
```
Проверим, как создалась таблица (выведем первые 10 строк):
```bash
hive --database <YOUR_USER>_test -e 'SELECT * FROM Subnets LIMIT 10'
```

Проверить список таблиц в базе:

```bash
hive --database <YOUR_USER>_test -e 'SHOW TABLES'
```

##### 4. Партиционирование
Создадим партиционированную таблицу из таблицы Subnets. Информация о каждой партиции хранится в отдельной HDFS-директории внутри metastore.
``` sql
SET hive.exec.dynamic.partition.mode=nonstrict;

USE <YOUR_USER>_test;
DROP TABLE IF EXISTS SubnetsPart;

CREATE EXTERNAL TABLE SubnetsPart (
    ip STRING
)
PARTITIONED BY (mask STRING)
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE SubnetsPart PARTITION (mask)
SELECT * FROM Subnets;
```

Уже здесь вы можете увидеть, что запрос транслируется в MapReduce-задачу. Чтоб убедиться в этом, можно зайти на ApplicationMaster UI: [http://sber-master.atp-fivt.org:8088] или в Job browser HUE.
Видим 1 MapReduce Job, в которой имеется только Map-стадия.

`set hive.exec.dynamic.partition=true;` - динамическое создание партиций. По умолчанию Hive партиционирует статически, т.е. создаётся фиксированное число партиций. Но в данном случае мы не знаем, сколько у нас уникальных значений маски, а значит не знаем сколько потребуется партиций. Эта опция стоит по умолчанию.
`SET hive.exec.dynamic.partition.mode=nonstrict;` - "нестрогое" партиционирование. При динамич. партиционировании, hive требует чтобы хотя бы 1 партиция была статическая. Снимаем это требование.

Подробние про динамич. партиционирование [здесь](https://datacadamia.com/db/hive/dp#mode).

Проверить получившиеся партиции:
```bash
hive --database <YOUR_USER>_test -e 'SHOW PARTITIONS SubnetsPart'
```

С помощью `SET` можно устанавливать и другие конфиги для job'ы. Например, так можно задать название всех job, которые сгенерируются в запросе: `SET mapred.job.name=my_query;`. Другой способ - с помощью аргумента `--hiveconf hive.session.id=my_query`.

Коды программ: `/home/velkerr/seminars/mcs17_hive1`.

##### 5. Парсинг входных данных с помощью регулярных выражений
1. Создаём новую таблицу.

    ``` sql
    add jar /opt/cloudera/parcels/CDH/lib/hive/lib/hive-serde.jar;
    USE <YOUR_USER>_test;
    DROP TABLE IF EXISTS SerDeExample;
    
    CREATE EXTERNAL TABLE SerDeExample (
        ip STRING
    )
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
    WITH SERDEPROPERTIES (
        "input.regex" = '^(\\S*)\\t.*$'
    )
    STORED AS TEXTFILE
    LOCATION '/data/user_logs/user_logs_M';
    
    select * from SerDeExample limit 10;
    ```
    Получаем на выходе:
    ```
    135.124.143.193
    247.182.249.253
    135.124.143.193
    222.131.187.37
     ...
    ```
    
    Группы в регулярке матчатся в поля. Матчинг по умолчанию происходит в том же порядке, в каком группы расположены в регулярке. Для изменения порядка матчинга можно задать `"output.format.string"`. Подробнее см. [здесь](https://cwiki.apache.org/confluence/display/Hive/UserGuide).
    
    Видим, что получилось «откусить» регуляркой первое поле. Остальные пока NULL'ы.
2. Пробуем откусить следующее поле. Меняем регулярное выражение (3 табуляции ставятся только в этом случае, все остальные поля разделены одной табуляцией).

    ```
    "input.regex" = '^(\\S*)\\t\\t\\t(\\S*)\\t.*$'
    ```
    Сохраняемся, запускаем: `$ hive –f myQuery.sql`
    Получаем:
    
    ```
    135.124.143.193	20150601013300
    247.182.249.253	20150601013354
    135.124.143.193	20150601013818
    222.131.187.37	20150601013957
     ...
    ```

Для отладки регулярок полезно пользоваться сервисом https://regex101.com/. При работе с сервисом '//' нужно заменять на '/'.

> **Задача.** Допишите рег. выражение. Добавьте его в запрос и выполните, чтоб убедиться, что данные распарсились правильно. Следите за типами данных.

<p>
<details>
<summary markdown="span"><h6> Ответ </h6></summary>

3. Чтобы данные распарсились правильно, нужно воспользоваться таким regex:
```
"input.regex" = '^(\\S*)\\t{3}(\\d{8})\\S*\\t(\\S*)\\t\\S+\\t(\\S*)\\t.*$'
```
Более сильный вариант (вместо `\S*` либо `\S+` либо `\d+` что позволяет не пропустить некорректные строки).
```
"input.regex" = '^(\\S+)\\t{3}(\\d{8})\\d+\\t(\\S+)\\t\\d+\\t(\\d+)\\t.*$
```
</details>
</p>

***Примечание для старых версий Hive*** Библиотека SerDe из `hive.contrib` имеет одну особенность. На выход после парсинга она выдаёт только строки тогда как в датасете имеются и числа. В случае, если в таблице есть числовые столбцы рекомендуется использовать `org.apache.hadoop.hive.serde2.RegexSerDe`. Эта реализация SerDe корректно парсит большинство типов данных Hive, но работает только для десериализации (т.е. для чтения данных). Синтаксис заросов при использовании этой версии SerDe почти не отличается. Единственное отличие - в пути к классу, который прописываем в `ROW FORMAT SERDE`.

В современной версии работает только `org.apache.hadoop.hive.serde2.RegexSerDe`, в обе стороны.

Вывод информации про таблицу:
``` bash
hive -S --database <YOUR_USER>_test -e 'DESCRIBE SerDeExample'
```
Аргумент: `-S` отключает логи, информацию о времени выполнения и т.д. Остаётся только результат запроса.
```
ip                  	string              	from deserializer   
date                	string              	from deserializer   
request             	string              	from deserializer   
responsecode        	string              	from deserializer
```
##### 6. Практика
> **Задача 0.** Посчитать кол-во различных масок подсети.

Решение.
```
USE <YOUR_USER>_test;

SELECT COUNT(DISTINCT mask)
FROM Subnets;
```
С помощью ключевого слова `EXPLAIN` можно вывести план запроса. Там будет показано в какие MapReduce-Job'ы будет транслироваться запрос.

```
STAGE DEPENDENCIES:
  Stage-1 is a root stage
  Stage-0 depends on stages: Stage-1

STAGE PLANS:
  Stage: Stage-1
    Map Reduce
      Map Operator Tree:
          TableScan
            ...
      Reduce Operator Tree:
        Group By Operator
          ...

  Stage: Stage-0
    Fetch Operator
      ...
```
Если зайти на ApplicationMaster Web UI [http://sber-master.atp-fivt.org:8088] можно увидеть, что запрос действительно транслируется в MapReduce-задачи.
> **Задача 1.** Посчитать кол-во адресов, имеющих маску 255.255.255.128.

В этой задачи видим фильтрацию, поэтому партиционирование, кот. мы сделали раньше, должно повлиять на скорость работы задачи. 
* Выполним запрос на таблице Subnets (без партиций) и SubnetsPart (с партициями). Что видим?
* Проверим размер исходных данных: `hdfs dfs -du -h /data/subnets/variant1`
* Пересоздадим таблицы Subnets и SubnetsPart на датасете `/data/subnets/big` (7 Gb) и повторим эксперимент. Как изменилась разница в быстродействии запросов?

> **Задача 2.** Посчитать среднее кол-во адресов по подсетям.
> По каждой задаче выведите план запроса и посчитайте по нему кол-во MapReduce Job.

### Оптимизации в Join'ах

Имеется 2 таблицы в базе `joins`

**Logs**
* ip (string)
* date (int)
* request (string)
* pagesize (smallint)
* statuscode (smallint)

**IpRegions**
* ip (string)
* region (string)

Сделаем JOIN 2 таблиц с отключенным MapJoin:

```sql
USE joins;
SET hive.auto.convert.join=false;

SELECT * FROM logs LEFT JOIN ipregions ON logs.ip = ipregions.ip
LIMIT 10;
```
* Видим, что wall time на незагруженном кластере 15+ секунд. 
* В Hue Job browser или YARN JobHistory видим, что сгенерировался редьюсер.

Исследуем размер таблицы IpRegions. `SELECT count(1) FROM ipregions;` выдает всего 10 строк, значит она поместится в память. Можем использовать MapJoin (Вспоминаем что такое Map-side join в Hadoop).

Есть 2 способа подсказать Hive что нужно использовать MapJoin.

```sql
USE joins;

SELECT /*+ MAPJOIN(ipregions) */ * FROM logs LEFT JOIN ipregions ON logs.ip = ipregions.ip
LIMIT 10;
```
*(может не сработать т.к. это рекомендация для Hive)*

```sql
USE joins;
SET hive.auto.convert.join=true;

SELECT * FROM logs LEFT JOIN ipregions ON logs.ip = ipregions.ip
LIMIT 10;
```
Видим, что редьюсер пропал и задача стала работать быстрее (~5 с. на незагруженном кластере). 

MapJoin нельзя использовать если маленькая таблица стоит слева при `LEFT JOIN` или справа при `RIGHT JOIN`.

[Подробнее про MapJoin в Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+JoinOptimization#LanguageManualJoinOptimization-PriorSupportforMAPJOIN).
