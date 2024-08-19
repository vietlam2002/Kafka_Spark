from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("E-commerce Transaction Analysis") \
    .config("spark.mongodb.input.uri", "mongodb://root:password@172.18.0.13:27017/ecommerce.transactions") \
    .config("spark.mongodb.output.uri", "mongodb://root:password@172.18.0.13:27017/ecommerce.transactions") \
    .getOrCreate()

transactions_df = spark.read.format("mongo").load()

transactions_df.show()