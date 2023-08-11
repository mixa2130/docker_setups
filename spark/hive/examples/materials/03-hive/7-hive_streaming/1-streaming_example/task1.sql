USE example;

SELECT TRANSFORM(ip, mask)
USING 'cut -d . -f 1' AS ip
FROM Subnets
LIMIT 10;
