#! /usr/bin/env bash

OUT_DIR="pi_result"
NUM_REDUCERS=4

hdfs dfs -rm -r -skipTrash $OUT_DIR*

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
	-D mapreduce.job.reduces=4 \
	-files mapper.py,reducer.py,combiner.py \
	-mapper './mapper.py' \
	-combiner './combiner.py' \
	-reducer './reducer.py' \
	-input pi_points \
	-output $OUT_DIR

hdfs dfs -ls $OUT_DIR
