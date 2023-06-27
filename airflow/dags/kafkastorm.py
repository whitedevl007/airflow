# from datetime import datetime, timedelta
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from pymongo import MongoClient
# from bson import ObjectId
# from kafka import KafkaProducer
# import json
# import time
# from airflow.operators.bash import BashOperator
# import subprocess

# default_args = {
#     'owner': 'airflow',
#     'start_date': datetime(2023, 5, 16),
#     'max_active_runs': 100
# }

# dag = DAG('storm_topology1', default_args=default_args, schedule_interval=timedelta(minutes=1))


# def read_from_mongodb_and_send_to_kafka():
#     try:
#         # Connect to MongoDB
#         mongo_uri = 'mongodb+srv://ansarafitha:root@cluster0.vgtdfso.mongodb.net/test'
#         client = MongoClient(mongo_uri)
#         db = client['username']
#         collection = db['userdemo']

#         # Connect to Kafka producer
#         kafka_bootstrap_servers = 'localhost:9092'
#         topic_name = 'test'
#         producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

#         # Retrieve documents from MongoDB
#         document_count = collection.count_documents({})
#         if document_count == 0:
#             print("No data to consume")
#             return False

#         cursor = collection.find({'processed_message_id': None})
#         for document in cursor:
#             try:
#                 # Remove the _id field from the document
#                 document_dict = {key: value for key, value in document.items() if key != '_id'}

#                 # Convert MongoDB document to a string
#                 message = json.dumps(document_dict)

#                 # Send data to Kafka topic
#                 producer.send(topic_name, message.encode('utf-8'))

#                 # Update the processed_message_id field in MongoDB
#                 collection.update_one({'_id': document['_id']}, {'$set': {'processed_message_id': document['_id']}})

#             except Exception as e:
#                 print(f"Error occurred while processing document: {str(e)}")

#         producer.flush()
#         time.sleep(1)

#     except Exception as e:
#         print(f"Error occurred in read_from_mongodb_and_send_to_kafka: {str(e)}")
#         return False


# def submit_topology():
#     bash_command = 'cd /home/nizam/project/Kafka-Storm && sparse run --name first_topology'
#     subprocess.run(bash_command, shell=True)


# read_task = PythonOperator(
#     task_id='read_task',
#     python_callable=read_from_mongodb_and_send_to_kafka,
#     dag=dag,
# )

# submit_task = PythonOperator(
#     task_id='submit_task',
#     python_callable=submit_topology,
#     dag=dag,
# )

# read_task >> submit_task

################################################################





# from datetime import datetime
# from airflow import DAG
# from airflow.operators.trigger_dagrun import TriggerDagRunOperator
# from airflow.operators.bash import BashOperator

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2023, 5, 16),
# }

# dag = DAG('trigger_dags', default_args=default_args, schedule=None)

# trigger_mongodb_kafka = TriggerDagRunOperator(
#     task_id='trigger_mongodb_kafka',
#     trigger_dag_id='mongodb_to_kafka_and_consumer',
#     dag=dag,
# )

# trigger_storm_topology1 = TriggerDagRunOperator(
#     task_id='trigger_storm_topology1',
#     trigger_dag_id='storm_topology1',
#     dag=dag,
# )

# submit_topology = BashOperator(
#     task_id='submit_topology',
#     bash_command='cd /home/nizam/project/Kafka-Storm && sparse run --name first_topology',
#     dag=dag
# )

# trigger_mongodb_kafka >> trigger_storm_topology1 >> submit_topology



###########################################################################



from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import MongoClient
from airflow.operators.bash import BashOperator
from bson import ObjectId
from kafka import KafkaProducer, KafkaConsumer
import json
import time
import subprocess

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 18),
}

dag = DAG('storm_topology1', default_args=default_args, schedule_interval=timedelta(minutes=1))


def read_from_mongodb_and_send_to_kafka():
    # Connect to MongoDB
    mongo_uri = 'mongodb+srv://ansarafitha:root@cluster0.vgtdfso.mongodb.net/test'
    client = MongoClient(mongo_uri)
    db = client['username']
    collection = db['userdemo']

    # Connect to Kafka producer
    kafka_bootstrap_servers = 'localhost:9092'
    topicName = 'test'
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

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


    
read_task = PythonOperator(
    task_id='read_task',
    python_callable=read_from_mongodb_and_send_to_kafka,
    dag=dag,
)



# Run the tasks concurrently
read_task 







