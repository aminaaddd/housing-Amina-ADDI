# Housing API
RESTful API built with Flask.

Follow these steps to set up and run the project on your local machine.

## Prerequisites
Docker installed on your system - https://docs.docker.com/get-started/introduction/get-docker-desktop/.

Docker Compose installed.

## Setup Instructions
```bash
git clone https://github.com/aminaaddd/housing-Amina-ADDI.git
```
```bash
cd housing-Amina-ADDI
```
```bash
docker-compose up --build
```

## Pull images
* https://hub.docker.com/repository/docker/amina444/postgres  # postgresql image
* https://hub.docker.com/repository/docker/amina444/house     # api image

## Migration
```bash
cd app
```
```bash
rm -rf migrations                                             # if migrations directory exists
```
```bash
docker exec -it venv-db-1 psql -U amina -d housing_db
```
```bash
   DROP TABLE IF EXISTS alembic_version;                     # if the table exists
```

## To see the names of containers
```bash
docker ps
```
## Create migrations
```bash
docker exec -it name-api-container /bin/bash
```
In my machine:
```bash
docker exec -it venv-house-api-1 /bin/bash
```
```bash
  flask db init
  flask db migrate -m "Create houses table"
  flask db upgrade
```

## Show the database
```bash
docker exec -it name-db-container psql -U amina -d housing_db
```
In my machine:
```bash
docker exec -it venv-db-1 psql -U amina -d housing_db
```
```bash
\dt
```

['!WARNING']
The names of containers in my machine could not be the same at your machine.

## Test
```bash
curl -X POST http://localhost:5000/houses \
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
  "median_house_value": 452600.0,
  "ocean_proximity": "NEAR BAY"
}'
```

## To check
* http://localhost:5000/houses
