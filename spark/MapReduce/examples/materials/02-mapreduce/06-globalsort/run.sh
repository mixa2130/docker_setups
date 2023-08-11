#! /usr/bin/env bash

out_dir='globalsort_out'
reducers_count=3

# Build project
ant clean && ant
# Remove previous results
hadoop fs -rm -r -skipTrash $out_dir*
# Run task
hadoop jar jar/GlobalSort.jar ru.mipt.GlobalSorter /data/wiki/en_articles_part $out_dir "$out_dir"_tmp $reducers_count &&

# Check results
for num in `seq 0 $(($reducers_count - 1))`
do
    hdfs dfs -cat $out_dir/part-r-0000$num | head
done
