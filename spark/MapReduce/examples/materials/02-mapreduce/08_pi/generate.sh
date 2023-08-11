#!/usr/bin/env bash

echo '1000000' > sample.txt

hdfs dfs -rm -r -skipTrash pi_numbers
hdfs dfs -mkdir pi_numbers

for i in $(seq 10)
do
    hdfs dfs -put sample.txt pi_numbers/${i}.txt
done
