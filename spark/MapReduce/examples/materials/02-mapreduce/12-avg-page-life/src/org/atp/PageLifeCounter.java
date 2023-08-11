package org.atp;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.map.InverseMapper;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.lib.partition.InputSampler;
import org.apache.hadoop.mapreduce.lib.partition.TotalOrderPartitioner;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.atp.customtypes.IntArrayWritable;

import java.io.IOException;
import java.util.Iterator;

public class PageLifeCounter extends Configured implements Tool {

    public static class ParseMapper extends Mapper<LongWritable, Text, Text, IntWritable>{
        private Text key = new Text();
        private IntWritable value = new IntWritable();

        public void map(LongWritable offset, Text line, Context context) throws IOException, InterruptedException {
            String[] parts = line.toString().split("\t");
            key.set(parts[2].replaceAll("(http://|https://)?(www\\\\.)?", ""));
            value.set(Integer.parseInt(parts[1]));
            context.write(key, value);
        }
    }

    public static class CntLifeReducer extends Reducer<Text, IntWritable, Text, IntWritable>{
        private IntWritable lifeTime = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            Iterator<IntWritable> it = values.iterator();
            int maxValue = Integer.MIN_VALUE;
            int minValue = Integer.MAX_VALUE;
            while (it.hasNext()){
                int currentVisit = it.next().get();
                maxValue = Math.max(maxValue, currentVisit);
                minValue = Math.min(minValue, currentVisit);
            }
            lifeTime.set(maxValue - minValue);
            context.write(key, lifeTime);
        }
    }

    public static class DomainMapper extends Mapper<Text, IntWritable, Text, IntArrayWritable>{
        private Text domain = new Text();
        private IntArrayWritable time = new IntArrayWritable();

        public void map(Text key, IntWritable value, Context context) throws IOException, InterruptedException {
            String url = key.toString();
            domain.set(url.substring(0, url.indexOf('/')));
            time.set(value.get(), 1);
            context.write(domain, time);
        }
    }

    public static class AvgCombiner extends Reducer<Text, IntArrayWritable, Text, IntArrayWritable>{
        private IntArrayWritable result = new IntArrayWritable();

        public void reduce(Text key, Iterable<IntArrayWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            int cnt = 0;

            Iterator<IntArrayWritable> it = values.iterator();
            while (it.hasNext()){
                IntWritable[] array = it.next().get();
                sum += array[0].get();
                cnt += array[1].get();
            }
            result.set(sum, cnt);
            context.write(key, result);
        }
    }

    public static class AvgReducer extends Reducer<Text, IntArrayWritable, IntWritable, Text>{
        private static final int SEC_IN_DAY = 86400;
        private IntWritable avg = new IntWritable();

        public void reduce(Text key, Iterable<IntArrayWritable> values, Context context) throws IOException, InterruptedException {
            float sum = 0;
            int cnt = 0;
            Iterator<IntArrayWritable> it = values.iterator();
            while (it.hasNext()){
                IntWritable[] array = it.next().get();
                sum += array[0].get();
                cnt += array[1].get();
            }
            avg.set(Math.round(sum / (cnt * SEC_IN_DAY)));
            context.write(avg, key);
        }
    }

    public static class InverseReducer extends Reducer<IntWritable, Text, Text, IntWritable>{
        public void reduce(IntWritable key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            for (Text word: values){
                context.write(word, key);
            }
        }
    }


    private static boolean deleteDirs(FileSystem fs, Path ... paths) throws IOException {
        for(Path path: paths){
            if(fs.exists(path)){
                fs.deleteOnExit(path);
                return true;
            }
        }
        return false;
    }

    @Override
    public int run(String[] strings) throws Exception {
        Path[] middlePaths = new Path[]{
                new Path(strings[1] + "_tmp"),
                new Path(strings[1] + "_tmp2")
        };
        Path partitions = new Path(strings[1] + "_parts");

        Configuration conf = getConf();
        FileSystem fs = FileSystem.get(conf);
        Job cntJob = Job.getInstance(conf);
        cntJob.setJarByClass(PageLifeCounter.class);
        cntJob.setJobName("PageLife, 1st job");

        cntJob.setMapperClass(ParseMapper.class);
        cntJob.setMapOutputKeyClass(Text.class);
        cntJob.setMapOutputValueClass(IntWritable.class);
        cntJob.setMaxMapAttempts(2);

        cntJob.setReducerClass(CntLifeReducer.class);
        cntJob.setOutputKeyClass(Text.class);
        cntJob.setOutputValueClass(IntWritable.class);
        cntJob.setMaxReduceAttempts(2);
        cntJob.setNumReduceTasks(9);

        cntJob.setInputFormatClass(TextInputFormat.class);
        cntJob.setOutputFormatClass(SequenceFileOutputFormat.class);

        TextInputFormat.addInputPath(cntJob, new Path(strings[0]));
        SequenceFileOutputFormat.setOutputPath(cntJob, middlePaths[0]);
        if (!cntJob.waitForCompletion(true)){
            deleteDirs(fs, middlePaths[0]);
            return 1;
        }

        Job job = Job.getInstance(getConf());
        job.setJarByClass(PageLifeCounter.class);
        job.setMapperClass(DomainMapper.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntArrayWritable.class);

        job.setCombinerClass(AvgCombiner.class);

        job.setReducerClass(AvgReducer.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(Text.class);
        job.setNumReduceTasks(9);

        job.setInputFormatClass(SequenceFileInputFormat.class);
        job.setOutputFormatClass(SequenceFileOutputFormat.class);
        SequenceFileInputFormat.addInputPath(job, middlePaths[0]);
        SequenceFileOutputFormat.setOutputPath(job, middlePaths[1]);
        return job.waitForCompletion(true)?0:1;
//        if (!job.waitForCompletion(true)){
//            deleteDirs(fs, middlePaths[0], middlePaths[1], partitions);
//            return 2;
//        }
    }

    public static void main(String[] args) throws Exception {
        ToolRunner.run(new PageLifeCounter(), args);
    }
}
