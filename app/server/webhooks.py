from flask import Flask, request
import threading
import json

app = Flask(__name__)

# Shared data storage
global_data_storage = {
    "tiltify": None,
    "fourthwall": None,
    "sheets": None
}

# Lock for thread-safe operations
lock = threading.Lock()

# Dummy functions to fetch data from APIs - replace these with your actual functions
def fetch_tiltify_data():
    data = Flask.tiltify_api.raised()
    return {data}

def fetch_fourthwall_data():
    data = Flask.fourthwall_api.get_fw_profit()
    return {data}

def fetch_sheets_data():
    # Your logic to fetch and return data from Google Sheets API
    return {}

# Update functions that use the API fetching functions
def update_tiltify_data():
    data = fetch_tiltify_data()
    print(data)
    
    with lock:
        global_data_storage["tiltify"] = data

def update_fourthwall_data():
    data = fetch_fourthwall_data()
    print(data)
    print(data)
    with lock:
        global_data_storage["fourthwall"] = data

def update_sheets_data():
    data = fetch_sheets_data()
    with lock:
        global_data_storage["sheets"] = data

# Webhook endpoints
@server.route('/webhook/tiltify', methods=['POST'])
def tiltify_webhook():
    threading.Thread(target=update_tiltify_data).start()
    return 'Tiltify Webhook received', 200

@server.route('/webhook/fourthwall', methods=['POST'])
def fourthwall_webhook():
    threading.Thread(target=update_fourthwall_data).start()
    return 'Fourthwall Webhook received', 200

@server.route('/webhook/sheets', methods=['POST'])
def sheets_webhook():
    threading.Thread(target=update_sheets_data).start()
    return 'Sheets Webhook received', 200

# API endpoint to retrieve the stored data
@server.route('/get-data', methods=['GET'])
def get_data():
    return json.dumps(global_data_storage), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Additional Flask setup...
