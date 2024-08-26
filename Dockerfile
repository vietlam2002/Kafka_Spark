FROM apache/airflow:2.7.1-python3.10

USER root
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
# Set environment variables for Spark
ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${PATH}"

# Download and install Scala 2.12
RUN curl -o scala-2.12.18.deb https://downloads.lightbend.com/scala/2.12.18/scala-2.12.18.deb && \
    dpkg -i scala-2.12.18.deb && \
    rm scala-2.12.18.deb

# Install Spark (optional: you can choose the version you need)
RUN curl -sL "https://downloads.apache.org/spark/spark-3.5.2/spark-3.5.2-bin-hadoop3.tgz" | tar xz -C /opt \
    && mv /opt/spark-3.5.2-bin-hadoop3 /opt/spark

# Copy .vimrc file into the correct path
COPY vim/.vimrc /opt/airflow/.vimrc

USER airflow

RUN pip install apache-airflow apache-airflow-providers-apache-spark pyspark kafka-python cassandra-driver

USER root
# Download and add Kafka and Cassandra connectors
#RUN mkdir -p /opt/spark/jars/ && \
#    chmod -R 777 /opt/spark/jars/ && \
#    curl -o /opt/spark/jars/spark-sql-kafka-0-10_2.13-3.4.1.jar https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.13/3.4.1/spark-sql-kafka-0-10_2.13-3.4.1.jar && \
#    curl -o /opt/spark/jars/kafka-clients-3.4.0.jar https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.0/kafka-clients-3.4.0.jar && \
#    curl -o /opt/spark/jars/spark-cassandra-connector_2.13-3.4.1.jar https://repo1.maven.org/maven2/com/datastax/spark/spark-cassandra-connector_2.13/3.4.1/spark-cassandra-connector_2.13-3.4.1.jar


RUN mkdir -p /opt/spark/jars/ && \
    chmod -R 777 /opt/spark/jars/ && \
    curl -o /opt/spark/jars/spark-sql-kafka-0-10_2.12-3.5.2.jar https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.2/spark-sql-kafka-0-10_2.12-3.5.2.jar && \
    curl -o /opt/spark/jars/kafka-clients-2.8.1.jar https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.8.1/kafka-clients-2.8.1.jar && \
    curl -o /opt/spark/jars/spark-cassandra-connector_2.12-3.5.0.jar https://repo1.maven.org/maven2/com/datastax/spark/spark-cassandra-connector_2.12/3.5.0/spark-cassandra-connector_2.12-3.5.0.jar && \
    curl -o /opt/spark/jars/spark-streaming_2.12-3.5.2.jar https://repo1.maven.org/maven2/org/apache/spark/spark-streaming_2.12/3.5.2/spark-streaming_2.12-3.5.2.jar

USER airflow