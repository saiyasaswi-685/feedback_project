from flask import Flask, request, jsonify
from kafka import KafkaProducer
import uuid, json, os, time, pymysql
from datetime import datetime

app = Flask(__name__)

# Kafka Setup with Retry
producer = None
while not producer:
    try:
        producer = KafkaProducer(
            bootstrap_servers=os.getenv('KAFKA_BROKER', 'kafka:9092'),
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("API connected to Kafka successfully!")
    except Exception:
        print("Kafka not ready... waiting 5 seconds...")
        time.sleep(5)

# Helper function for DB connection
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'mysql'),
        user='root',
        password='root_password',
        db='feedback_db',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/feedback', methods=['POST'])
def submit():
    data = request.get_json()
    if not all(k in data for k in ['customer_id', 'feedback_text', 'timestamp']):
        return jsonify({'error': 'Missing fields'}), 400
    
    message_id = str(uuid.uuid4())
    payload = {
        'message_id': message_id,
        'customer_id': data['customer_id'],
        'feedback_text': data['feedback_text'],
        'feedback_timestamp': data['timestamp']
    }
    producer.send('customer_feedback_events', payload)
    producer.flush()
    return jsonify({'message': 'Success', 'id': message_id}), 202

# New GET endpoint: Get specific feedback by ID
@app.route('/feedback/<message_id>', methods=['GET'])
def get_feedback_by_id(message_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM feedback_analysis WHERE message_id = %s", (message_id,))
        result = cur.fetchone()
    conn.close()
    if result:
        return jsonify(result), 200
    return jsonify({'error': 'Feedback not found'}), 404

# New GET endpoint: Filter by sentiment
@app.route('/feedback', methods=['GET'])
def get_all_feedback():
    sentiment = request.args.get('sentiment')
    conn = get_db_connection()
    with conn.cursor() as cur:
        if sentiment:
            cur.execute("SELECT * FROM feedback_analysis WHERE sentiment_score = %s", (sentiment,))
        else:
            cur.execute("SELECT * FROM feedback_analysis")
        results = cur.fetchall()
    conn.close()
    return jsonify(results), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)