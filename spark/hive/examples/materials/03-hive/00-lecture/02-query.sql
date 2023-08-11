USE example;

SET mapreduce.job.name=hive_task;
SET mapreduce.job.reduces=10;

--EXPLAIN EXTENDED
SELECT AVG(counts.cnt)
FROM (
    SELECT mask, count(1) as cnt
    FROM subnetspart TABLESAMPLE (1000000 ROWS)
    GROUP BY mask
) counts;

--    FROM SubnetsPart TABLESAMPLE (1000 ROWS)
