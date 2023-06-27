import pymongo
from kafka import KafkaProducer
import json
import time

# MongoDB connection details
database_name = 'username'
collection_name = 'userdemo'

# Kafka connection details

# Connect to MongoDB
client = pymongo.MongoClient('mongodb+srv://ansarafitha:root@cluster0.vgtdfso.mongodb.net/test')
db = client[database_name]
collection = db[collection_name]

# Kafka connection details
bootstrap_servers = ['localhost:9092']
topicName = 'test'
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Retrieve documents from MongoDB
cursor = collection.find({})

   
while True:
    # Retrieve documents with a processed_message_id value of None
    cursor = collection.find({'processed_message_id': None})

    for document in cursor:
        # Remove the _id field from the document
        document_dict = {key: value for key, value in document.items() if key != '_id'}

        # Convert MongoDB document to a string
        message = json.dumps(document_dict)

        # Send data to Kafka topic
        producer.send(topicName, message.encode('utf-8'))

        # Update the processed_message_id field in MongoDB
        collection.update_one({'_id': document['_id']}, {'$set': {'processed_message_id': document['_id']}})

    producer.flush()

    # Wait for 1 second before checking for new data
    time.sleep(1)
