### 1. Clone the repository

```bash
git clone https://github.com/aminaaddd/housing-Amina-ADDI.git
cd housing-Amina-ADDI/housing-model
```
### 2. Install dependencies

#### Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

##### Run the following command to build and start the containers

```bash
docker-compose up --build
```

#### To test
```bash
curl -X POST http://localhost:6000/predict \
-H "Content-Type: application/json" \
-d '{
  "longitude": -122.23,
  "latitude": 37.88,
  "housing_median_age": 41.0,
  "total_rooms": 880,
  "total_bedrooms": 129,
  "population": 322,
  "households": 126,
  "median_income": 8.3252,
  "ocean_proximity": "NEAR BAY"
}'
```

* http://localhost:6000/predict > The URL where the API is running
