# Housing API
RESTful API built with Flask.

Follow these steps to set up and run the project on your local machine.

## Prerequisites
Docker installed on your system (Install Docker).
Docker Compose installed (Install Docker Compose).

## Setup Instructions
git clone https://github.com/aminaaddd/housing-Amina-ADDI.git
docker-compose up --build

## Pull images
* https://hub.docker.com/repository/docker/amina444/postgres  # postgresql image
* https://hub.docker.com/repository/docker/amina444/house     # api image

## Migration
rm -rf migrations                                             # if migrations directory exists
docker exec -it venv-db-1 psql -U amina -d housing_db
  > DROP TABLE IF EXISTS alembic_version;                     # if the table exists

## Create migrations
docker exec -it venv-house-api-1 /bin/bash
  > flask db init
  > flask db migrate -m "Create houses table"
  > flask db upgrade

## Show the database
docker exec -it venv-db-1 psql -U amina -d housing_db
	> \dt

## Test
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

## To check
* http://localhost:5000/houses
