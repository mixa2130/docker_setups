from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql import SparkSession


def parse_edge(s):
    user, follower = s.split("\t")
    return int(user), int(follower)

spark = SparkSession.builder \
    .appName("S2pac_bigrams") \
    .master('yarn') \
    .getOrCreate()

n = 100  # number of partitions
start_vertex = 12
finish_vertex = 34
cur_distance = 0

edges_schema = StructType([StructField('user_id', IntegerType(), False),
                           StructField('follower_id', IntegerType(), False)])
distances_schema = StructType([StructField('user_id', IntegerType(), False),
                               StructField('distance', IntegerType(), False),
                               StructField('route', StringType(), False)])
udf = F.UserDefinedFunction(lambda prev_dist: prev_dist + 1, IntegerType())

edges = spark.sparkContext.textFile("/data/twitter/twitter_sample.txt").map(parse_edge)
_edges_rdd = edges.map(lambda e: (e[1], e[0])).partitionBy(n)
edges_df = spark.createDataFrame(_edges_rdd, edges_schema)

_distances_rdd = spark.sparkContext.parallelize([(start_vertex, cur_distance, '')])
distances_df = spark.createDataFrame(_distances_rdd, distances_schema).repartition(n)

while True:
    candidates_df = distances_df.alias('a'). \
        join(F.broadcast(edges_df.alias('b')), F.col("a.user_id") == F.col("b.user_id")). \
        select(F.col('follower_id').alias('user_id'),
               udf('distance').alias('distance'),
               F.concat(F.col('route'), F.lit(','), F.col("a.user_id")).alias('route'))

    distances_df = distances_df.union(candidates_df).distinct().repartition(100).cache()
    final_route = distances_df. \
        where(distances_df.user_id == finish_vertex). \
        select(distances_df.distance, distances_df.route)

    if final_route.count() > 0:
        res = final_route.sort(F.asc('distance')).head()
        print(res['route'][1:] + f',{finish_vertex}')
        break
