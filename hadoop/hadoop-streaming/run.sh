OUT_DIR="task1"
OUT_FILE_LOCAL="out.txt"
NUM_REDUCERS=5

hdfs dfs -rm -r -skipTrash $OUT_DIR*
rm -f ${OUT_FILE_LOCAL}
yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
  -D mapreduce.job.name="01-task-mapreduce" \
  -D mapreduce.partition.keycomparator.options='-nk2' \
  -files mapper.py,reducer.py \
  -mapper "python3 mapper.py" \
  -combiner "sort -nk2" \
  -reducer "python3 reducer.py" \
  -numReduceTasks ${NUM_REDUCERS} \
  -input "/data/ids/" \
  -output ${OUT_DIR}

# Checking result
for num in $(seq 0 $(($NUM_REDUCERS - 1))); do
  hdfs dfs -cat ${OUT_DIR}/part-0000$num | head -10 >> ${OUT_FILE_LOCAL}
done


file_lns=$(cat ${OUT_FILE_LOCAL} | wc -l)

if [[ ${file_lns} == 50 ]]; then
        cat out.txt;
else
        echo "${file_lns}"
        echo "FAILED";
fi
