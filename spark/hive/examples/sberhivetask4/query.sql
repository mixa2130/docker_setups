ADD file ./handler.py;
USE stupakmi;

SELECT TRANSFORM (*)
 USING 'python3 ./handler.py'
 AS (ip, http_url, page_size, http_status, client_app_info, creation_date)
FROM logs
LIMIT 10;
