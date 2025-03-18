from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# load the trained model
model = joblib.load("models/model.joblib")

# Features that were used during training
TRAINING_FEATURES = ['longitude', 'latitude', 'housing_median_age', 'total_rooms',
                     'total_bedrooms', 'population', 'households', 'median_income']

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    
    if request.method == 'GET':
        return jsonify({
            "message": "Please send a POST request with the JSON payload in the 'dataframe_split' format."
        })
        
        
    data = request.get_json()
    #df = pd.DataFrame([data])
    
    if 'dataframe_split' in data:
        # Create a DataFrame 
        df = pd.DataFrame(
            data['dataframe_split']['data'],
            columns=data['dataframe_split']['columns']
        )
    else:
        df = pd.DataFrame([data])
    
    # Filter df
    #df = df[TRAINING_FEATURES]
    
    try:
        df = df[TRAINING_FEATURES]
    except KeyError as e:
        return jsonify({"error": f"Missing expected features: {e}"}), 400
    
    prediction = model.predict(df)
    return jsonify({"median_house_value": prediction[0]})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

