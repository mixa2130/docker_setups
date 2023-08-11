add jar Identity/jar/Identity.jar;
--ADD JAR Identity/target/Identity-1.0-SNAPSHOT.jar;

USE velkerr;

create temporary function identity as 'com.hobod.IdentityUDF';

select identity(ip)
from SerDeExample
limit 10;
