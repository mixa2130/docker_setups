USE velkerr;

--EXPLAIN
SELECT COUNT(ip)
FROM subnetspart
WHERE mask like "255.255.255.128";
