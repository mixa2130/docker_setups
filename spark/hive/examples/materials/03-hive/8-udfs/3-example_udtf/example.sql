ADD JAR CopyIp/jar/CopyIp.jar;

USE example;

CREATE TEMPORARY FUNCTION copyip as 'com.hobod.CopyIpUDTF';

select copyip(ip)
from subnets
LIMIT 10;
