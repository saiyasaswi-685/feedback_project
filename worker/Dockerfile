FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Partner instructions prakaram NLTK data download cheyali
RUN python -m nltk.downloader vader_lexicon

COPY . .

CMD ["python", "worker.py"]