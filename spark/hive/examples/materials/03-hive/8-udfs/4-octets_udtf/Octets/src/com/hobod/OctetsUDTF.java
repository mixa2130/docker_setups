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
public class OctetsUDTF extends GenericUDTF {
    public static final int DELIMITER = Integer.MAX_VALUE;
    private StringObjectInspector address;
    private Object[] forwardObjArray = new Object[1];

    @Override
    public StructObjectInspector initialize(ObjectInspector[] args) throws UDFArgumentException {
        address = (StringObjectInspector) args[0];

        final List<String> fieldNames = new ArrayList<String>(){{
            add("Octets");}}; //collumn name
        final List<ObjectInspector> fieldInspectors = new ArrayList<ObjectInspector>(){{
            add(PrimitiveObjectInspectorFactory.javaIntObjectInspector);
        }}; //inspector to check that each field is Integer
        return ObjectInspectorFactory.getStandardStructObjectInspector(fieldNames, fieldInspectors);
    }

    @Override
    public void process(Object[] objects) throws HiveException {
        for(String octet: address.getPrimitiveJavaObject(objects[0]).split("\\.")){
            forwardObjArray[0] = Integer.parseInt(octet);
            forward(forwardObjArray);
        }
        forwardObjArray[0] = DELIMITER;
        forward(forwardObjArray);
    }

    @Override
    public void close() throws HiveException {
    }
}
