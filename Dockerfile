FROM python:3.9-slim

RUN pip install mlflow

# Copier les fichiers du projet dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y git


# Expose le port 6000
EXPOSE 6000

# Lance le serveur MLflow
CMD ["python", "model.py"]

