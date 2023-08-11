ADD FILE ./script2.py;

USE example;

SELECT TRANSFORM(ip, mask)
USING 'python3 ./script2.py' AS (ip, mask)
FROM Subnets
LIMIT 10;
