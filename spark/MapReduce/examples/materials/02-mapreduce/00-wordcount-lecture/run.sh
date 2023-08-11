#! /usr/bin/env bash

OUT_DIR="wordcount_result"
NUM_REDUCERS=6

hdfs dfs -rm -r -skipTrash ${OUT_DIR}*

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name="Streaming wordCount" \
    -D mapreduce.job.reduces=${NUM_REDUCERS} \
    -files mapper.py,reducer.py \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input "/data/silmarillion" \
    -output ${OUT_DIR} > /dev/null

hdfs dfs -ls ${OUT_DIR}
hdfs dfs -cat ${OUT_DIR}/part-0000* | sort -k2nr | head
