from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# load the trained model
model = joblib.load("models/model.joblib")

# Features that were used during training
TRAINING_FEATURES = ['longitude', 'latitude', 'housing_median_age', 'total_rooms',
                     'total_bedrooms', 'population', 'households', 'median_income']

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])
    
    # Filter df
    df = df[TRAINING_FEATURES]
    prediction = model.predict(df)
    return jsonify({"median_house_value": prediction[0]})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

