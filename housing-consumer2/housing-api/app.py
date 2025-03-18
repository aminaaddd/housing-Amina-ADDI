from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Create the Flask application
app = Flask(__name__)

from flask_migrate import Migrate





# Configure the db
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/housing_db")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # SQLAlchemy

class House(db.Model): # model for houses
    __tablename__ = "houses" # the table name
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    housing_median_age = db.Column(db.Integer, nullable=False)
    total_rooms = db.Column(db.Integer, nullable=False)
    total_bedrooms = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    households = db.Column(db.Integer, nullable=False)
    median_income = db.Column(db.Float, nullable=False)
    median_house_value = db.Column(db.Float, nullable=False)
    ocean_proximity = db.Column(db.String, nullable=False)

@app.route('/houses', methods=['GET'])
def get_houses():
    houses = House.query.all() # Retrieve all house records from db
    result = []
    for house in houses:
        # Build a list of dict containing houses data
        result.append({
            'id': house.id,
            'longitude': house.longitude,
            'latitude': house.latitude,
            'housing_median_age': house.housing_median_age,
            'total_rooms': house.total_rooms,
            'total_bedrooms': house.total_bedrooms,
            'population': house.population,
            'households': house.households,
            'median_income': house.median_income,
            'median_house_value': house.median_house_value,
            'ocean_proximity': house.ocean_proximity
        })
    return jsonify(result)

@app.route('/houses', methods=['POST'])
def add_house():
    data = request.get_json() 
    # Create a new house 
    new_house = House(
        longitude=data['longitude'],
        latitude=data['latitude'],
        housing_median_age=data['housing_median_age'],
        total_rooms=data['total_rooms'],
        total_bedrooms=data['total_bedrooms'],
        population=data['population'],
        households=data['households'],
        median_income=data['median_income'],
        median_house_value=data['median_house_value'],
        ocean_proximity=data['ocean_proximity']
    )
    db.session.add(new_house) # add new house record to the session
    db.session.commit() # commit the session
    return jsonify({'id': new_house.id}), 201

if __name__ == '__main__':
    with app.app_context(): # Create db table if it does not exist
        db.create_all()
    app.run(host="0.0.0.0", port=5000)

