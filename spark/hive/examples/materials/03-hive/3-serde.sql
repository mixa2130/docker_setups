ADD JAR /opt/cloudera/parcels/CDH/lib/hive/lib/hive-serde.jar;

USE velkerr;

DROP TABLE IF EXISTS SerDeExample;

CREATE EXTERNAL TABLE SerDeExample (
    ip STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
    "input.regex" = '^((?:\\d{1,3}\\.){3}\\d{1,3})\\s+.*$'
)
STORED AS TEXTFILE
LOCATION '/data/user_logs/user_logs_M';

select * from SerDeExample limit 10;
