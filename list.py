import mlflow

# List all registered models using search_registered_models
models = mlflow.search_registered_models()
for model in models:
    print(model.name)
