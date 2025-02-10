from mlflow.tracking import MlflowClient

model_name = "RandomForestHousing"
client = MlflowClient()

# This returns a list of the latest versions for the given model.
versions = client.get_latest_versions(model_name)

for v in versions:
    print(f"Model: {v.name}, Version: {v.version}, Status: {v.status}")
