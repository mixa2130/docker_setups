ADD FILE ./task4.sh;

USE velkerr;

SELECT TRANSFORM(ip, `date`, request, page_size)
USING './task4.sh' AS ip, `date`, request, responseCode
FROM SerDeExample
LIMIT 10;
