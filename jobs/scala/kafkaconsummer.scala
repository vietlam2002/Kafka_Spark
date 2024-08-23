import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.streaming.Trigger

object KafkaConsumer {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder
      .appName("KafkaConsumerExample")
      .master("local[*]")
      .getOrCreate()
    
    val kafkaDF = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "kafka1:29092, kafka2:29092, kafka3:29092").option("subcribe", "users_created").option("startingOffsets", "earliest").load()
    val dataDF = kafkaDF.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    val query = dataDF.writeStream.outputMode("append").format("console").trigger(Trigger.ProcessingTime("5 seconds")).start()
    query.awaitTermination()
  }
}
