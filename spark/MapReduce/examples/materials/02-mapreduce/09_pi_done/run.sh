#! /usr/bin/env bash

OUT_DIR="pi_result"
NUM_REDUCERS=0

hdfs dfs -rm -r -skipTrash $OUT_DIR*

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
	-D mapreduce.job.reduces=${NUM_REDUCERS} \
	-files mapper.py,reducer.py \
	-mapper './mapper.py' \
	-input pi_points \
	-output $OUT_DIR

hdfs dfs -ls $OUT_DIR
