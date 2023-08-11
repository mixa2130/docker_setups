USE velkerr;

SET mapreduce.job.name="task3_non_partitioned";
--EXPLAIN
SELECT COUNT(DISTINCT mask)
FROM Subnets;
