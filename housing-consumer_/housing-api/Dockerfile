FROM python:3.9-slim

WORKDIR /housing-api
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN pip install flask_sqlalchemy
RUN pip install flask_migrate

EXPOSE 5000

ENV FLASK_APP=api.py

CMD ["python", "app.py"]

