import json, os, pymysql, nltk, time
from kafka import KafkaConsumer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime

nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()

# Retry logic for Kafka connection
consumer = None
while not consumer:
    try:
        consumer = KafkaConsumer(
            'customer_feedback_events',
            bootstrap_servers=os.getenv('KAFKA_BROKER', 'kafka:9092'),
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            group_id='sentiment_group'
        )
        print("Worker connected to Kafka successfully!")
    except Exception:
        print("Kafka not ready... waiting 5 seconds...")
        time.sleep(5)

for message in consumer:
    fb = message.value
    score = analyzer.polarity_scores(fb['feedback_text'])['compound']
    sentiment = 'positive' if score >= 0.05 else 'negative' if score <= -0.05 else 'neutral'
    
    try:
        conn = pymysql.connect(
            host=os.getenv('MYSQL_HOST'),
            user='root',
            password='root_password',
            db='feedback_db'
        )
        with conn.cursor() as cur:
            sql = "INSERT IGNORE INTO feedback_analysis VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (fb['message_id'], fb['customer_id'], fb['feedback_text'], sentiment, fb['feedback_timestamp'], datetime.now()))
        conn.commit()
        conn.close()
        print(f"Processed: {fb['message_id']} - {sentiment}")
    except Exception as e:
        print(f"DB Error: {e}")