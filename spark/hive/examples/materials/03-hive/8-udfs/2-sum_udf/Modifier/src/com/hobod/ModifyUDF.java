package com.hobod;

import org.apache.hadoop.hive.ql.exec.Description;
import org.apache.hadoop.hive.ql.exec.UDF;

/**
 * Created by velkerr on 26.03.17.
 */
@Description(
        name = "SampleUDF",
        value = "Returns sum of octets in IPs"
)
public class ModifyUDF extends UDF {

    public int evaluate(String str){
        int sum = 0;
        for(String octet: str.split("\\.")){
            sum += Integer.parseInt(octet);
        }
        return sum;
    }
}
