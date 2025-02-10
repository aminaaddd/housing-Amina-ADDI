import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from flask import Flask, jsonify, request
import mlflow
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error, r2_score
from mlflow.tracking import MlflowClient

classification_problem = False

df = pd.read_csv('housing.csv')

# Data cleaning
print(df.info())
print(df.isnull().sum()) # see null values
df = df.drop_duplicates()
print(df) # if there is duplicated values

df['total_bedrooms'].fillna(df['total_bedrooms'].mean(), inplace=True) # Replace missed values by calculating the mean
#print(df['total_bedrooms'])

print(df.isnull().sum()) # Check if there is no Null values

# Reset index after cleaning
df = df.reset_index(drop=True)

# Encoder (for categorical variables)
encoder = LabelEncoder()
df['ocean_proximity'] = encoder.fit_transform(df['ocean_proximity'])

# Numeric features
features = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 
            'total_bedrooms', 'population', 'households', 'median_income']

scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])

# Remove outliers
#def remove_outliers(df, column):
#    Q1 = df[column].quantile(0.25)
#    Q3 = df[column].quantile(0.75)
#    IQR = Q3 - Q1
#    lower_bound = Q1 - 1.5 * IQR
#    upper_bound = Q3 + 1.5 * IQR
#    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

#for col in ['housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 
#            'households', 'median_income', 'median_house_value'
#]:
#    housing_data = remove_outliers(df, col)

#housing_data.fillna(housing_data.mean(), inplace=True)


# Feautures and target
X = df.drop(columns='median_house_value')
y = df['median_house_value']

X.fillna(X.mean(), inplace=True)
y.fillna(y.mean(), inplace=True)

# Split data into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Vérification finale des NaN dans X_train:")
print(X_train.isnull().sum().sum())  # Devrait afficher 0

print("Vérification finale des NaN dans X_test:")
print(X_test.isnull().sum().sum())  # Devrait afficher 0


params = {
    "n_estimators": 100,
    "max_depth": 6,
    "min_samples_split": 10,
    "min_samples_leaf": 4,
    "bootstrap": True,
    "oob_score": False,
    "random_state": 888,
}
# Train the model
model = RandomForestRegressor(**params)
model = model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# MSE
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)                                                                     
r2 = r2_score(y_test, y_pred)
# accuracy
if classification_problem:
    accuracy = accuracy_score(y_test, y_pred)
print(f"MSE: {mse}")
print(f"MAE: {mae}")
print(f"R²: {r2}")                                                     
if classification_problem:
    print(f"Accuracy: {accuracy}")

# MLflow

# Configurer l'URI de tracking MLflow
mlflow.set_tracking_uri("http://mlflow-tracking:5000")

client = MlflowClient()

# Démarrer une nouvelle exécution MLflow
run_name = "Random_Forest_Model"

with mlflow.start_run(run_name=run_name) as run:

    # Log des paramètres et métriques
    mlflow.log_params(params)
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("r2", r2)

    if classification_problem:
        mlflow.log_metric("accuracy", accuracy)

    # Enregistrer directement dans le registre MLflow
    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="RandomForestHousing"  # Enregistrement direct
    )

    print(f"Modèle enregistré : {model_info.model_uri}")

# Vérifier les versions disponibles du modèle
versions = client.get_latest_versions("RandomForestHousing")

if not versions:
    print("Aucun modèle enregistré sous le nom 'RandomForestHousing'.")
else:
    for v in versions:
        print(f"Version: {v.version}, Status: {v.current_stage}")

    # Prendre la dernière version enregistrée automatiquement
    latest_version = versions[-1].version
    print(f"Utilisation de la version {latest_version} du modèle.")

    # Définir model_uri dynamiquement
    model_uri = f"models:/RandomForestHousing/{latest_version}"
    print(f"Chargement du modèle depuis : {model_uri}")

    # Charger le modèle avec la bonne version
    model = mlflow.sklearn.load_model(model_uri)

# API Flask
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.is_json:
            json_ = request.json
            df = pd.DataFrame(json_)
            
            # Appliquer la transformation sur les données envoyées
            df[features] = scaler.transform(df[features])
            df['ocean_proximity'] = encoder.transform(df['ocean_proximity'])

            # Effectuer la prédiction
            prediction = model.predict(df)   
            return jsonify({'prediction': prediction.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000, debug=True)
