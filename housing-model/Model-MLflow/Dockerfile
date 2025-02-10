FROM python:3.9-slim

RUN pip install mlflow

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y git


# Expose on 6000
EXPOSE 6000

CMD ["python", "model.py"]

