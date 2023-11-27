from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import threading
import api
import os
from dotenv import load_dotenv


app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

load_dotenv()

Tiltify_HOOK = os.getenv('TI_HOOK')
Fourthwall_HOOK = os.getenv('FW_HOOK')
Sheets_HOOK = os.getenv('GS_HOOK')
# Shared data storage
global_data_storage = {
    "tiltify": None,
    "fourthwall": None,
    "sheets": None
}

# Lock for thread-safe operations
lock = threading.Lock()

# Flag to check if initialization has already occurred
initialized = False
# Dummy functions to fetch data from APIs - replace these with your actual functions
def fetch_tiltify_data():
    data = api.get_tiltify()
    return data  # Removed the unnecessary set wrapping

def fetch_fourthwall_data():
    data = api.get_fourthwall()
    return data  # Removed the unnecessary set wrapping

def fetch_sheets_data():
    # Your logic to fetch and return data from Google Sheets API
    return {}

# Update functions that use the API fetching functions
def update_tiltify_data():
    data = fetch_tiltify_data()
    with lock:
        global_data_storage["tiltify"] = data
    print("Tiltify Data Updated:", data)

def update_fourthwall_data():
    data = fetch_fourthwall_data()
    with lock:
        global_data_storage["fourthwall"] = data
    print("Fourthwall Data Updated:", data)

def update_sheets_data():
    data = fetch_sheets_data()
    with lock:
        global_data_storage["sheets"] = data
    print("Sheets Data Updated:", data)

# Function to run on server startup to initialize base values
def initialize_base_values():
    global initialized
    if not initialized:
        update_tiltify_data()
        update_fourthwall_data()
        update_sheets_data()
        initialized = True
        print(global_data_storage)

# Webhook endpoints
@app.route(Tiltify_HOOK, methods=['POST'])
@limiter.limit("1 per  seconds")
def tiltify_webhook():
    threading.Thread(target=update_tiltify_data).start()
    return 'Tiltify Webhook received', 200

@app.route(Fourthwall_HOOK, methods=['POST'])
@limiter.limit("1 per 3 seconds")
def fourthwall_webhook():
    threading.Thread(target=update_fourthwall_data).start()
    return 'Fourthwall Webhook received', 200

@app.route(Sheets_HOOK, methods=['POST'])
@limiter.limit("1 per 3 seconds")
def sheets_webhook():
    threading.Thread(target=update_sheets_data).start()
    return 'Sheets Webhook received', 200

# API endpoint to retrieve the stored data
@app.route('/server/crt23-data', methods=['GET'])
@limiter.limit("30 per 1 seconds")
def get_data():
    return jsonify(global_data_storage), 200

if __name__ == '__main__':
    print(os.getpid())
    initialize_base_values()  # Call initialization function on startup
    
    app.run(debug=True, port=5000)
    print(os.getpid())
    