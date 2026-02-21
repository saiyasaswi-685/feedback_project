FROM python:3.9-slim

# OS dependencies for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Flask port 5000 lo run avthundi
EXPOSE 5000

CMD ["python", "app.py"]