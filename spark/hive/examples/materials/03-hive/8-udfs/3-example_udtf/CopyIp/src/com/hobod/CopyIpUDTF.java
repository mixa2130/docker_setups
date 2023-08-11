package com.hobod;

import org.apache.hadoop.hive.ql.exec.UDFArgumentException;
import org.apache.hadoop.hive.ql.metadata.HiveException;
import org.apache.hadoop.hive.ql.udf.generic.GenericUDTF;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspectorFactory;
import org.apache.hadoop.hive.serde2.objectinspector.StructObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.primitive.PrimitiveObjectInspectorFactory;
import org.apache.hadoop.hive.serde2.objectinspector.primitive.StringObjectInspector;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by velkerr on 26.03.17.
 */
public class CopyIpUDTF extends GenericUDTF {
    public static final String DELIMITER = "-----";
    public static final int COPIES_CNT = 2;

    private StringObjectInspector address;
    /**
     * Since the processing of 1 record may give us a full table, Hive uses an array for its storage.
     * However, in this example we have a single field in each record.
     * Therefore our array will always have 1 element.
     */
    private Object[] forwardObjArray = new Object[1];

    @Override
    public StructObjectInspector initialize(ObjectInspector[] args) throws UDFArgumentException {
        // Parsing an input data
        if(args.length != 1){  //Checking the quantity of arguments
            throw new UDFArgumentException(getClass().getSimpleName() + " takes only 1 argument!");
        }
        address = (StringObjectInspector) args[0]; // IP is a String, so use StringObjectInspector

        // Describing the structure for output
        final List<String> fieldNames = new ArrayList<String>(){{
            add("Ips");}}; //Setting a collumn name. Output table will have a single collumn
        final List<ObjectInspector> fieldInspectors = new ArrayList<ObjectInspector>(){{
            add(PrimitiveObjectInspectorFactory.javaStringObjectInspector);
        }}; //Inspector to check that each field is String
        return ObjectInspectorFactory.getStandardStructObjectInspector(fieldNames, fieldInspectors);
    }

    @Override
    public void process(Object[] objects) throws HiveException {
        // UDTF has 1 argument, hence `objects` has a single element too
        String currentAddr = address.getPrimitiveJavaObject(objects[0]);
        forwardObjArray[0] = currentAddr;
        // repeat IP twice
        for(int i = 0; i< COPIES_CNT; i++){
            forward(forwardObjArray);
        }
        // Add a delimiter
        forwardObjArray[0] = DELIMITER;
        forward(forwardObjArray);
    }

    @Override
    public void close() throws HiveException {
    }
}
