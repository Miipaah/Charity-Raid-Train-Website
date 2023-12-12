from flask import Flask, jsonify,request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import threading
import api
import os
from dotenv import load_dotenv
import requests
from flask_cors import CORS




app = Flask(__name__)
CORS(app)
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
    "sheets": [
   {
      "Streamer":"duckisaurus",
      "Time":1702260000000,
      "TILTIFY":"https://tiltify.com/@duckisaurus/last-stop-on-the-charity-raid-train",
      "TWITCH":"www.twitch.tv/duckisaurus",
      "TEST TIME":1701901192610
   }
]
}

def getraised():
    print(int(global_data_storage["fourthwall"]))
    amount =  global_data_storage["fourthwall"]+ global_data_storage["tiltify"]
    return jsonify(amount), 200
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

def update_sheets_data(data):
    
    with lock:
        global_data_storage["sheets"] = data
    print("Sheets Data Updated:", data)

# Function to run on server startup to initialize base values

def initialize_base_values():
    global initialized
    if not initialized:
        update_tiltify_data()
        update_fourthwall_data()
        initialized = True
        print(global_data_storage)
initialize_base_values()

@app.route('/api/')
def hello():
    return 'Hello, World!'

@app.route('/')
def hello():
    return 'Hello, World!'

# Webhook endpoints
@app.route(Tiltify_HOOK, methods=['POST'])
@limiter.limit("1 per 5 seconds")
def tiltify_webhook():
    threading.Thread(target=update_tiltify_data).start()
    return 'Tiltify Webhook received', 200

@app.route(Fourthwall_HOOK, methods=['POST'])
@limiter.limit("1 per 5 seconds")
def fourthwall_webhook():
    threading.Thread(target=update_fourthwall_data).start()
    return 'Fourthwall Webhook received', 200

@app.route(Sheets_HOOK, methods=['POST'])
@limiter.limit("5 per 30 seconds")
def webhook():
    load_dotenv()
    sig = os.getenv('SHEETS_SIGN')
    incoming_data = request.json
    if incoming_data['signature'] == sig:
        print(incoming_data['data'])
        # Start the thread and pass data to the function
        threading.Thread(target=update_sheets_data, args=(incoming_data['data'],)).start()
        return jsonify(incoming_data['data'])
    
    return jsonify({"message": "Error Unauthorized"}), 401


# API endpoint to retrieve the stored data
@app.route('/crt23-data', methods=['GET'])
@limiter.limit("15 per 1 seconds")
def get_data():
    return jsonify(global_data_storage), 200

@app.route('/total-raised', methods=['GET'])
@limiter.limit("15 per 1 seconds")
def get_total():
    tiltify_amount = fetch_tiltify_data()
    fourthwall_amount = fetch_fourthwall_data()
    raised = round(fourthwall_amount + tiltify_amount, 2)
    return jsonify(raised), 200


@app.route('/api/schedule', methods=['GET'])
@limiter.limit("15 per 1 seconds")
def get_schedule():
    return jsonify(global_data_storage["sheets"]), 200

if __name__ == '__main__':

    initialize_base_values()  # Call initialization function on startup
    
    app.run( port=5000)
    
    
