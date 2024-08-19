from pymongo import MongoClient
from uuid import uuid4
from random import randint, uniform
from datetime import datetime, timedelta

#connect to MongoDB
client = MongoClient('mongodb://root:password@localhost:27017/')
db = client['ecommerce']
collection = db['transactions']

#Create fake data
def generate_fake_data(n = 1000):
    data = []
    for i in range(n):
        record = {
            "transaction_id": str(uuid4()),
            "customer_id": str(uuid4()),
            "product_id": str(uuid4()),
            "quantity": randint(1, 10),
            "price": round(uniform(5.0, 100.0), 2),
            "timestamp": datetime.now() - timedelta(days=randint(0, 30))
        }
        data.append(record)
    return data

#Insret data into colections transactions
fake_data = generate_fake_data(1000)
collection.insert_many(fake_data)
print("Data inserted successfully.")

#Close connect
client.close()