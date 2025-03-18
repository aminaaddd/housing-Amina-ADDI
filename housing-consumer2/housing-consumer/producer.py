import time
import json
from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'broker1:9092'
}

# Create kafka producer
producer = Producer(conf)

# message
house_message = {
    "longitude": -122.23,
    "latitude": 37.88,
    "housing_median_age": 52,
    "total_rooms": 880,
    "total_bedrooms": 129,
    "population": 322,
    "households": 126,
    "median_income": 8.3252,
    "median_house_value": 358500,
    "ocean_proximity": "NEAR BAY"
}

# Fonction to report the delivery status of messages
def delivery_report(err, msg):
    if err is not None:
        print(f"Erreur lors de l'envoi: {err}")
    else:
        print(f"Message envoyé à {msg.topic()} [{msg.partition()}]")

while True: # Send a message every 10s 
    # send the message to the topic
    producer.produce('housing_topic', json.dumps(house_message).encode('utf-8'), callback=delivery_report)
    
    # Ensure that the message is devliverd
    producer.flush()
    print("Message envoyé, attente de 10 secondes...")
    
    
    time.sleep(10)

