### MapReduce

Стадии MapReduce:
![img.png](images/map_reduce.png)

1. **MAP**: Берём пары ключ, значение [(k1, v1), (k2, v2), ...] и независимо их обрабатываем
2. **SORT**: группировка по ключам k и сортировка
3. **REDUCE**: с этими группами проводим агрегацию и тд.

Пример:

~~~python
>> > reduce(lambda x, y: x + y, range(5))
>> > 10  # sum 0 to 4
~~~

![img.png](images/img_ex.png)

Hadoop - код к данным. Данные уже где-то есть и как-то разбиты:
![img.png](images/hadoop_mapreduce.png)

* f - map
* g - reduce

![img.png](images/hadoop_map_reduce_in_details.png)

Буфер лежит в ОЗУ и когда он переполнился - сбрасывается на диск. (Так происходит много раз)
После сброса происходит разбиение этих маленьких файлов на группы(partitioning).
Далее они сливаются в файл побольше с сохранением ранее размеченных групп.
К группам применяется hash и по результатам функции уже распределяем группы на reducer-ы.

![img.png](images/bet_map_n_reduce.png)

![img.png](images/mapreduce_summer.png)

![img.png](images/mapreduce_wt_master.png)

**На mapper-е мы ничего в ОЗУ не храним, так как памяти даже на выход в буфер может не хватить**

Если нужно мини объединение - используем combiner

![img.png](images/combiner.png)

![img.png](images/mapreduce_on_hive.png)


