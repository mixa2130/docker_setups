from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql import SparkSession, Row
import re
import pyspark.sql.types as T
from pyspark.sql.functions import as F
from pyspark.ml.feature import NGram

# открываем сессию
spark = SparkSession.builder.appName("SparkSes").getOrCreate()
sc = spark.sparkContext


schema = StructType(fields=[
    StructField("id", IntegerType()),
    StructField("text", StringType())])

# преобразовываем стоп слова в список
rdd = sc.textFile("/data/wiki/stop_words_en-xpo6.txt")
stop = [i for i in rdd.take(100000000)]


def lower_case(x):
    res = []
    x = re.sub("^\W+|\W+$", "", x, flags=re.UNICODE)
    x = x.lower().split()
    for jj in x:
        jj = jj.strip()
        if jj not in stop and jj.isalnum():
            res.append(jj)
        else:
            continue
    return res


convert_to_lower = F.udf(lower_case, T.ArrayType(T.StringType()))

ngram = NGram(n=2, inputCol="text", outputCol="bigrams")

convert_to_lower = F.udf(lower_case, T.ArrayType(T.StringType()))
df = spark.read.format("csv") \
    .schema(schema) \
    .option("sep", "\t") \
    .load("/data/wiki/en_articles_part") \
    .select(F.regexp_replace(F.col("text"), "\p{P}", "").alias("text")) \
    .select(convert_to_lower(F.col("text")).alias("text"))

df1 = df.withColumn('word', F.explode(F.col('text'))) \
    .groupBy('word') \
    .count() \
    .sort('count', ascending=False)

total2 = df1.select(F.sum("count")).collect()

a = [i['sum(count)'] for i in total2]

df1 = df1.withColumn('word1', df1["count"] / a[0])

df = ngram.transform(df)

df = df.select(explode("bigrams").alias("bigrams")).groupBy("bigrams").count()

total1 = df.select(F.sum("count")).collect()

b = [i['sum(count)'] for i in total1]

df = df.withColumn('word12', df["count"] / b[0])

split_col = F.split(df['bigrams'], ' ')
df = df.withColumn('NAME1', split_col.getItem(0))
df = df.withColumn('NAME2', split_col.getItem(1))

df = df.join(df1, df["NAME1"] == df1["word"], 'left').select(df["bigrams"], df["count"], df["word12"], df["NAME1"],
                                                             df["NAME2"], df1["word"], df1["word1"])

df = df.withColumnRenamed("word", "newwordd1") \
    .withColumnRenamed("word1", "newwordd11")

df = df.join(df1, df["NAME2"] == df1["word"], 'left').select(df["bigrams"], df["count"], df["word12"], df["NAME1"],
                                                             df["NAME2"], df["newwordd1"], df["newwordd11"],
                                                             df1["word"], df1["word1"])

df = df.withColumn("Proizv", (-F.log(df["word12"] / (df["newwordd11"] * df["word1"])) / F.log(df["word12"])))

qstr = """SELECT bigrams from df where count>=500 order by proizv desc """
df.registerTempTable("df")

tt = spark.sql(qstr).take(39)
for i in tt:
    i = i[0].split()
    i = "_".join(i)
    print(i)
