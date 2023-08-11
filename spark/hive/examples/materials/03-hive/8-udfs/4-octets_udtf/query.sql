ADD JAR Octets/jar/Octets.jar;

USE velkerr;

CREATE TEMPORARY FUNCTION octets as 'com.hobod.OctetsUDTF';

select octets(ip)
from serdeexample
LIMIT 10;
