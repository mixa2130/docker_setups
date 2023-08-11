--ADD JAR /opt/cloudera/parcels/CDH/lib/hive/lib/hive-contrib.jar;

SET hive.query.name="partitioning test";
SET hive.exec.dynamic.partition.mode=nonstrict;
USE velkerr;
DROP TABLE IF EXISTS SubnetsPart;

CREATE EXTERNAL TABLE SubnetsPart (
    ip STRING
)
PARTITIONED BY (mask STRING)
STORED AS TEXTFILE;

INSERT OVERWRITE TABLE SubnetsPart PARTITION (mask)
SELECT * FROM Subnets;
