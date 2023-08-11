USE example;

SET mapred.job.name="hive_task";

EXPLAIN
select avg(cnt) as avg_ip_address from 
(
select count(ip) as cnt, mask from subnets group by mask) 
as t ;