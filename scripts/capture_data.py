from kafka import KafkaConsumer
import json
import psycopg2

# Cấu hình kết nối PostgreSQL
conn_params = {
    'dbname': 'airflow',
    'user': 'airflow',
    'password': 'airflow',
    'host': 'localhost',
    'port': '4040'
}
conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()

# Tạo Kafka Consumer để lắng nghe topic
consumer = KafkaConsumer(
    'demo.public.users',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='unique_consumer_group_test',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x is not None else None
)

print("Listening to topic...")

# Hàm lưu dữ liệu vào PostgreSQL
def save_to_postgres(data, operation):
    try:
        if operation == 'c' or operation == 'u':  # Tạo mới hoặc cập nhật
            insert_query = """
            INSERT INTO airflow.users (id, col1) VALUES (%s, %s)
            ON CONFLICT (id) DO UPDATE SET col1 = EXCLUDED.col1;
            """
            cursor.execute(insert_query, (data["id"], data["col1"]))
        elif operation == 'd':  # Xóa
            delete_query = """
            DELETE FROM airflow.users WHERE id = %s;
            """
            cursor.execute(delete_query, (data["id"],))
        conn.commit()
        print(f"Saved data to Postgres: {data}")
    except Exception as e:
        print(f"Error saving to Postgres: {e}")
        conn.rollback()


# Lắng nghe và xử lý dữ liệu từ Kafka topic
for message in consumer:
    if message.value is not None:
        print(f"Received message: {message.value}")
        print(f"Partition: {message.partition}, Offset: {message.offset}, Timestamp: {message.timestamp}")
        
        operation = message.value.get('op')  # Lấy loại thao tác
        after_data = message.value.get('after')  # Dữ liệu sau thay đổi
        before_data = message.value.get('before')  # Dữ liệu trước thay đổi
        
        if operation in ['c', 'u'] and after_data:
            save_to_postgres(after_data, operation)  # Lưu dữ liệu mới hoặc cập nhật
        elif operation == 'd' and before_data:
            save_to_postgres(before_data, operation)  # Xóa bản ghi cũ

# Đóng kết nối khi hoàn thành
cursor.close()
conn.close()
