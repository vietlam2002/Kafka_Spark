from pyspark.sql import SparkSession
print("hello airlfow")

spark = SparkSession.builder.appName("PythonWordCount").getOrCreate()
text = "Hello Spark Hello Python Hello Airflow Hello Docker Hello Lam"
words = spark.sparkContext.parallelize(text.split(" "))
wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b: a+b)

for wc in wordCounts.collect():
    print(wc[0], wc[1])

spark.stop()

#spark = SparkSession.builder \
#    .appName("E-commerce Transaction Analysis") \
#    .config("spark.mongodb.input.uri", "mongodb://root:password@172.18.0.13:27017/ecommerce.transactions") \
#    .config("spark.mongodb.output.uri", "mongodb://root:password@172.18.0.13:27017/ecommerce.transactions") \
#    .getOrCreate()

#transactions_df = spark.read.format("mongo").load()

#transactions_df.show()
