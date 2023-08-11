USE velkerr;

DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS ipregions;

CREATE EXTERNAL TABLE logs (
    ip STRING,
    `date` INT,
    request STRING,
    page_size SMALLINT,
    response SMALLINT,
    browser STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
    "input.regex" = '^(\\S+)\\t{3}(\\d{8})\\S+\\t(\\S+)\\t(\\S+)\\t(\\d{1,})\\t(\\S+).*$'
)
STORED AS TEXTFILE
LOCATION '/data/user_logs/user_logs_M';

SELECT * FROM logs LIMIT 10;

CREATE EXTERNAL TABLE Users(
    ip STRING,
    browser STRING,
    gender STRING,
    age tinyint
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY  '\t'
STORED AS TEXTFILE
LOCATION '/data/user_logs/user_data_M';

SELECT * FROM users LIMIT 10;

CREATE EXTERNAL TABLE IpRegions(
    ip STRING,
    region STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '/data/user_logs/ip_data_M/';

SELECT * FROM IpRegions LIMIT 10;

SHOW TABLES;
