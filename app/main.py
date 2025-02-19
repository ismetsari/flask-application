from flask import Flask, jsonify # type: ignore
import uuid
import json
import threading
import time
from datetime import datetime
import random
from pymongo import MongoClient # type: ignore
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
client = MongoClient(mongo_uri)
db = client['events_db']
events_collection = db['events']

def generate_random_event():
    event_types = ['user_signup', 'order_created', 'payment_processed', 'item_viewed']
    payload_data = {
        'user_id': random.randint(1000, 9999),
        'amount': round(random.uniform(10.0, 1000.0), 2),
        'product_id': str(random.randint(1, 100))
    }
    
    event = {
        'eventId': str(uuid.uuid4()),
        'eventType': random.choice(event_types),
        'timestamp': datetime.utcnow().isoformat(),
        'payload': payload_data
    }
    return event

def publish_events():
    while True:
        event = generate_random_event()
        
        # Log to stdout
        print(json.dumps(event, indent=2))
        
        # Store in MongoDB
        events_collection.insert_one(event)
        
        time.sleep(10)

# Start the event publishing thread
event_thread = threading.Thread(target=publish_events, daemon=True)
event_thread.start()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/message', methods=['GET'])
def message():
    return jsonify({"message": "Hello from DevOps case study v6"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
