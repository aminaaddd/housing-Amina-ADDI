from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)

# Database configuration 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://amina:23012006@db:5432/housing_db' # Connection to my db called housing_db hosted at db:5432
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Initialize database and migration tools
db = SQLAlchemy(app) # to interact with db, it translates the model House into a table in db
migrate = Migrate(app, db) # To manage db changes

# Define the House model
class House(db.Model): # House table
    id = db.Column(db.Integer, primary_key=True) # Primary key
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    housing_median_age = db.Column(db.Integer, nullable=False)
    total_rooms = db.Column(db.Integer, nullable=False)
    total_bedrooms = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    households = db.Column(db.Integer, nullable=False)
    median_income = db.Column(db.Float, nullable=False)
    median_house_value = db.Column(db.Float, nullable=False)
    ocean_proximity = db.Column(db.String(100), nullable=False)

# API Routes (Get and Post)
@app.route("/houses", methods=["GET", "POST"])
def houses():
    if request.method == "GET":
        # Get all houses from the database
        houses = House.query.all()
        results = [
            {
                "longitude": house.longitude,
                "latitude": house.latitude,
                "housing_median_age": house.housing_median_age,
                "total_rooms": house.total_rooms,
                "total_bedrooms": house.total_bedrooms,
                "population": house.population,
                "households": house.households,
                "median_income": house.median_income,
                "median_house_value": house.median_house_value,
                "ocean_proximity": house.ocean_proximity,
            }
            for house in houses
        ]
        return jsonify(results), 200

    elif request.method == "POST":
        # Get the data from the request body
        data = request.json
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
        db.session.add(new_house) # Add new house to db
        db.session.commit() # Save changes
        return jsonify({"message": "House added successfully"}), 201

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
