ADD JAR /opt/cloudera/parcels/CDH/lib/hive/lib/hive-serde.jar;

SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;
SET hive.mapred.mode = nonstrict;
SET hive.exec.max.dynamic.partitions=116;
SET hive.exec.max.dynamic.partitions.pernode=116;


USE stupakmi;

CREATE EXTERNAL TABLE raw_user_logs
(
    ip              STRING,
    creation_date   INT,
    http_url        STRING,
    page_size       INT,
    http_status     INT,
    client_app_info STRING
)
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
        WITH SERDEPROPERTIES (
        "input.regex" =
                '^((?:\\d{1,3}\\.){3}\\d{1,3})\\s+(\\d{8})\\d+\\s+((?:ht|f)tps?://(?:www)?\\S+)\\s+(\\d+)\\s+((?:\\d{1,3}){3})\\s+(?:(\\S+\\s[\\S \\t]+)).*$',
        "output.format.string" = '%2$s %1$s %3$s'
        )
    STORED AS textfile
    LOCATION '/data/user_logs/user_logs_M';



CREATE EXTERNAL TABLE logs
(
    ip              STRING,
    http_url        STRING,
    page_size       INT,
    http_status     INT,
    client_app_info STRING
)
    PARTITIONED BY (creation_date INT)
    STORED AS textfile;

INSERT OVERWRITE TABLE logs PARTITION (creation_date)
SELECT ip, http_url, page_size, http_status, client_app_info, creation_date
FROM raw_user_logs;

SELECT *
FROM logs
LIMIT 10;

CREATE EXTERNAL TABLE users
(
    ip           STRING,
    browser_info STRING,
    gender       STRING,
    age          INT
)
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
        WITH SERDEPROPERTIES (
        "input.regex" =
                '^((?:\\d{1,3}\\.){3}\\d{1,3})\\s+(\\S+)\\s+(male|female)\\s+(\\d{1,3}).*$'
        )
    STORED AS textfile
    LOCATION '/data/user_logs/user_data_M';

SELECT *
FROM users
LIMIT 10;


CREATE EXTERNAL TABLE ipregions
(
    ip     STRING,
    region STRING
)
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
        WITH SERDEPROPERTIES (
        "input.regex" =
                '^((?:\\d{1,3}\\.){3}\\d{1,3})\\s+([\\S ]+).*$'
        )
    STORED AS textfile
    LOCATION '/data/user_logs/ip_data_M';

SELECT *
FROM ipregions
LIMIT 10;

CREATE EXTERNAL TABLE subnets
(
    ip   STRING,
    mask STRING
)
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
        WITH SERDEPROPERTIES (
        "input.regex" =
                '^((?:\\d{1,3}\\.){3}\\d{1,3})\\s+((?:\\d{1,3}\\.){3}\\d{1,3}).*$'
        )
    STORED AS textfile
    LOCATION '/data/subnets/variant1';

SELECT *
FROM subnets
LIMIT 10;