FROM python:3.11-slim

WORKDIR app

# Installer les dépendances système
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY api.py .
COPY requirements.txt .

RUN pip install flask_sqlalchemy
RUN pip install flask_migrate
RUN pip install -r requirements.txt

EXPOSE 8000

ENV FLASK_APP=api.py

CMD ["python", "api.py"]
