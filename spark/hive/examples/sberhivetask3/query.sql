SET hive.auto.convert.join = false;

USE stupakmi;

SELECT reg.region,
       sum(case when u.gender = 'male' then 1 else 0 end)   as cnt_male,
       sum(case when u.gender = 'female' then 1 else 0 end) as cnt_female
FROM ipregions reg
         INNER JOIN users u ON reg.ip = u.ip
GROUP BY reg.region;