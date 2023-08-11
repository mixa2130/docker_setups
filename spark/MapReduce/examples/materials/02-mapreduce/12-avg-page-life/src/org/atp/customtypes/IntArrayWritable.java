package org.atp.customtypes;

import org.apache.hadoop.io.ArrayWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Writable;

public class IntArrayWritable extends ArrayWritable {
    public IntArrayWritable(){
        super(IntWritable.class);
    }

    public IntArrayWritable(int... values){
        super(IntWritable.class);
        this.set(values);
    }

    public void set(int... values){
        IntWritable[] intermediateValues = new IntWritable[values.length];
        for(int i=0; i<values.length; i++){
            intermediateValues[i] = new IntWritable(values[i]);
        }
        super.set(intermediateValues);
    }

    public IntWritable[] get(){
        Writable[] rawArray = super.get();
        IntWritable[] castedArray = new IntWritable[rawArray.length];
        for(int i=0; i<rawArray.length; i++){
            castedArray[i] = (IntWritable) rawArray[i];
        }
        return castedArray;
    }
}
