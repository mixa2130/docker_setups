add jar Modifier/jar/Modifier.jar;

USE example;

create temporary function modify as 'com.hobod.ModifyUDF';

select modify(ip)
from Subnets
limit 10;
