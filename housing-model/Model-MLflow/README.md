# Housing Price Prediction with Random Forest and MLflow

I used in this part a machine learning model built with Random Forest to predict housing prices. The model is trained on a dataset that includes various features such as the number of rooms, population, and income, and it is deployed using Flask and Docker for making predictions via an API.

## Features
* Data preprocessing (handling missing values, encoding categorical data, scaling numerical data)
* Random Forest model for regression
* MLflow integration for tracking the model and its metrics
* Flask API for serving predictions
* Docker Compose setup for easy containerization of the application

## Instructions

#### Clone the Repository
```bash
git clone https://github.com/aminaaddd/housing-Amina-ADDI.git
cd housing-Amina-ADDI/housing-model/Model-MLflow
```

### To create venv/env
```bash
python3 -m venv venv
```

### Activate venv/env
```bash
source venv/bin/activate
```

### Docker Compose Setup
```bash
docker-compose up --build
```


The Flask API will be running on http://localhost:6000
The MLflow tracking UI will be available at http://localhost:5000


### POST to (http://localhost:6000/predict)
```bash
curl -X POST http://localhost:6000/predict \
-H "Content-Type: application/json" \
-d '{
  "longitude": -122.23,
  "latitude": 37.88,
  "housing_median_age": 41,
  "total_rooms": 880,
  "total_bedrooms": 129,
  "population": 322,
  "households": 126,
  "median_income": 8.3252,
  "ocean_proximity": "NEAR BAY"
}'
```


## Structure
housing-model/
             ├── Model-MLflow/
                              │
                              ├── venv/
                              ├── Dockerfile                 # Dockerfile for the Flask app
                              ├── docker-compose.yml         # Docker Compose configuration
                              ├── requirements.txt           # Python dependencies
                              ├── housing.csv                # Dataset
                              ├── model.py                   # Flask app and model code
                              └── README.md                  


### Documentation
* https://mlflow.org/docs/latest/getting-started/index.html
* https://mlflow.org/docs/latest/tracking.html



