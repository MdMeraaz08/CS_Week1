import os
import subprocess
import json
import time
import threading
from flask import Flask, jsonify

# Function to collect logs
def collect_logs():
    logs = {}
    
    try:
        logs['syslog'] = subprocess.check_output(['tail', '-n', '20', '/var/log/syslog']).decode('utf-8')
    except Exception as e:
        logs['syslog'] = f'Error: {e}'
    
    try:
        logs['authlog'] = subprocess.check_output(['tail', '-n', '20', '/var/log/auth.log']).decode('utf-8')
    except Exception as e:
        logs['authlog'] = f'Error: {e}'
    
    try:
        logs['dmesg'] = subprocess.check_output(['dmesg | tail -n 20'], shell=True).decode('utf-8')
    except Exception as e:
        logs['dmesg'] = f'Error: {e}'
    
    with open('logs.json', 'w') as f:
        json.dump(logs, f, indent=4)
    
    return logs

# Flask API to serve logs
app = Flask(__name__)

@app.route('/logs', methods=['GET'])
def get_logs():
    if os.path.exists('logs.json'):
        with open('logs.json', 'r') as f:
            return jsonify(json.load(f))
    else:
        return jsonify({'error': 'No logs found'}), 404

# Function to run log collection in a separate thread
def log_collector():
    while True:
        collect_logs()
        time.sleep(60)

if __name__ == '__main__':
    # Start log collection thread
    threading.Thread(target=log_collector, daemon=True).start()
    app.run(debug=True, port=5000)
