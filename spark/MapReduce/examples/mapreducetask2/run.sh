IN_DIR="/data/wiki/en_articles"
OUT_DIR="s2pac_mapreduce_2"

# Remove previous results
hdfs dfs -rm -r -skipTrash ${OUT_DIR}.tmp >/dev/null

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
  -D mapreduce.job.name="02-task-mapreduce-1" \
  -files mapper.py,reducer.py,combiner.py \
  -numReduceTasks 7 \
  -mapper "python3 mapper.py" \
  -combiner "python3 combiner.py" \
  -reducer "python3 reducer.py" \
  -input ${IN_DIR} \
  -output ${OUT_DIR}.tmp >/dev/null

hdfs dfs -rm -r -skipTrash ${OUT_DIR} >/dev/null

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
  -D mapreduce.job.name="02-task-mapreduce-2" \
  -D stream.num.map.output.key.fields=3 \
  -D mapreduce.job.reduces=1 \
  -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
  -D mapreduce.partition.keycomparator.options='-k2,2nr -k1' \
  -mapper cat \
  -reducer cat \
  -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
  -input ${OUT_DIR}.tmp \
  -output ${OUT_DIR} >/dev/null

hdfs dfs -cat ${OUT_DIR}/part-00000 | head -10

