import json
from confluent_kafka import Consumer
from confluent__kafka import read_ccloud_config

props = read_ccloud_config("client.properties")
props["group.id"] = "python-group-1"
props["auto.offset.reset"] = "earliest"

consumer = Consumer(props)
topic = "Test"

consumer.subscribe([topic])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is not None and msg.error() is None:
            key = msg.key()
            value = msg.value()
            if key is not None and value is not None:
                try:
                    data = json.loads(value.decode('utf-8'))  # Parse the JSON message
                    # Process the data as needed
                    print("Received message:")
                    print(json.dumps(data, indent=2))  # Print the parsed JSON data
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON message: {str(e)}")
except KeyboardInterrupt:
    pass
