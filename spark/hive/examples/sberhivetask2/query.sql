USE stupakmi;

SELECT creation_date,
       COUNT(1) as cnt
FROM logs
GROUP BY creation_date
ORDER BY cnt DESC;
