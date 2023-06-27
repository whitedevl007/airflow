from faker import Faker
from kafka import KafkaProducer
import time
fake=Faker()
import random
import json
from datetime import datetime


bootstrap_servers = ['localhost:9092']
topicName = 'test'
producer = KafkaProducer(bootstrap_servers = bootstrap_servers)
producer = KafkaProducer()

while True:

    data={"Personal_info": {"Name": "John mathew", "Age": "34", "DOB": "19-11-1989", "email": "john@gmail.com", "phone": "(91)7869569810"}, "location": {"address": "21734 broadway st", "postalCode": "CA 94115", "city": "Delhi", "countryCode": "IN"}, "education": {"area": "Software Development", "studyType": "Bachelor", "institution": "University", "startDate": "04-06-2009", "endDate": "03-05-2013", "score": "4.0"}, "skills": {"Softskills": [{"Englishspeaking": "", "Englishwriting": "", "Leadership": ""}], "Techskills": [{"python": "3"}, {"Hadoop": "5"}, {"HTML": "2"}, {"Nodejs": "4"}, {"Angular": "3"}]}, "work": {"name": "Company", "position": "Developer", "startDate": "13-05-2014", "endDate": "20-05-2020"}, "certificates": [{"name": "Experiencecertificate", "date": "06-07-2020", "issuer": "Company"}], "projects": [{"name": "Project", "description": "Description\u2026", "role": "Team Lead"}]}
    m=json.dumps(data)
    ack=producer.send(topicName, m.encode('utf-8'))
    metadata = ack.get()

    print(metadata.topic)
    print(metadata.partition)

    producer.flush()
    time.sleep(10)

    
