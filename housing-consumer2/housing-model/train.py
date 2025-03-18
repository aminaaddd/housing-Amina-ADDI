import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os
import mlflow
import mlflow.sklearn
import mlflow.models.signature


# ------------------------------------------
# Data loading and preparation
# ------------------------------------------

data = pd.read_csv("housing.csv")
data.dropna(inplace=True) # Drop rows with missing values

# numerical features
features = ['longitude', 'latitude', 'housing_median_age', 'total_rooms',
            'total_bedrooms', 'population', 'households', 'median_income']
            
X = data[features]
y = data["median_house_value"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# ------------------------------------------
# Model training and evaluation
# ------------------------------------------

# Linear regression model
model = LinearRegression()
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print("Model score:", score)


# ------------------------------------------
# MLflow 
# ------------------------------------------

input_example = X_train.iloc[0:1]  # input example: df with same columns as training data

signature = mlflow.models.signature.infer_signature(X_train, model.predict(X_train))

mlflow.set_experiment("Housing Price Prediction")
with mlflow.start_run():
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_metric("score", score)
    mlflow.sklearn.log_model(model, "model", input_example=input_example, signature=signature)

# save the trained model locally (joblib)
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/model.joblib")

