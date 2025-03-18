import time
from confluent_kafka import Consumer, KafkaError
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

# Wait 15s to ensure that kafka is fully started
time.sleep(15)

# Connection to broker1 on port 9092,
conf = {
    'bootstrap.servers': 'broker1:9092',
    'group.id': 'housing-consumer-group',
    'auto.offset.reset': 'earliest'
}

# Create kafka consumer with conf
consumer = Consumer(conf)

# I make a loop until the topic appears
topic_found = False
max_attempts = 10
attempt = 0

while not topic_found and attempt < max_attempts:
    md = consumer.list_topics(timeout=10) # consumer retrieve messages from the broker
    if 'housing_topic' in md.topics: # if the topic is listed in md
        topic_found = True
        logging.info("Topic 'housing_topic' détecté après %d tentatives.", attempt+1)
    else:
        logging.info("Topic 'housing_topic' non détecté, nouvelle tentative dans 10 secondes...")
        attempt += 1
        time.sleep(10)

if not topic_found:
    logging.error("Le topic 'housing_topic' n'a pas été détecté après plusieurs essais.")
    consumer.close()
    exit(1)
    

# If the topic is found, subscribe the consumer to the topic
consumer.subscribe(['housing_topic'])

# URLs for API and model
API_URL = "http://housing-api:5000/houses"
MODEL_URL = "http://housing-model:5001/predict"
MODEL_MLflow_URL = "http://housing-model:5001/predict"

try:
    while True:
        msg = consumer.poll(1.0)
        
        if msg is None:
            # no message received, continue ...
            continue

        if msg.error():
            # if reveive error
            if msg.error().code() == KafkaError._PARTITION_EOF: # is just the consumer has read all messages, so there is no new message
                continue
            else:
                # For other errors
                logging.error("Erreur lors de la consommation: %s", msg.error())
                time.sleep(5)
                continue


        try:
            house_data = json.loads(msg.value().decode('utf-8'))
        except Exception as e:
            logging.error("Erreur de décodage JSON: %s", e)
            continue
            
            
        payload = {
            "dataframe_split": {
            "columns": [
                "longitude", "latitude", "housing_median_age", "total_rooms",
                "total_bedrooms", "population", "households", "median_income"
            ],
            "data": [[
                house_data["longitude"],
                house_data["latitude"],
                house_data["housing_median_age"],
                house_data["total_rooms"],
                house_data["total_bedrooms"],
                house_data["population"],
                house_data["households"],
                house_data["median_income"]
            ]]
            }
        }


        # Send the received data to API 
        try:
            response_api = requests.post(API_URL, json=house_data)
            if response_api.status_code == 201:
                logging.info("House added successfully via API.")
                
            else:
                logging.error("Failed to add house via API. Status: %s", response_api.status_code)
                
                
        except Exception as e:
            logging.error("Erreur lors de l'appel à l'API: %s", e)



        # Send the received data to the model for prediction
        #try:
            #response_model = requests.post(MODEL_URL, json=house_data)
            #if response_model.ok:
             #   prediction = response_model.json()
              #  logging.info("Prediction from model: %s", prediction)
                
            #else:
             #   logging.error("Failed to get prediction from model. Status: %s", response_model.status_code)
                
       # except Exception as e:
        #    logging.error("Erreur lors de l'appel au modèle: %s", e)
        # Wait 1s before polling for the next message
        #time.sleep(1)
        
        
        
        try:
            response_mlflow = requests.post(MODEL_MLflow_URL, json=payload)
            if response_mlflow.ok:
                prediction_mlflow = response_mlflow.json()
                predict_val = prediction_mlflow[0] if isinstance(prediction_mlflow, list) else prediction_mlflow.get("median_house_value")
                logging.info("Prediction (mlflow) from model: %s", predict_val)
            else:
                logging.error("Failed to get prediction (mlflow). Status: %s", response_mlflow.status_code)
                continue
        except Exception as e:
            logging.error("Erreur lors de l'appel au modèle: %s", e)
            continue
            
        house_data["predicted_median_house"] = predict_val
        
        

except KeyboardInterrupt:
    logging.info("Consumer interrupted")
finally:
    consumer.close()

