ADD FILE ./task5.py;

USE example;

--EXPLAIN
SELECT TRANSFORM(ip, mask)
USING './task5.py' AS ip, mask
FROM Subnets
LIMIT 20;
