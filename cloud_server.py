from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# API route to receive temperature and humidity data
@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json()

    # Process the data here (e.g., log it, store it in a database, etc.)
    if not data:
        return jsonify({"error": "No data received"}), 400

    timestamp = data.get('timestamp')
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    if not timestamp or not temperature or not humidity:
        return jsonify({"error": "Invalid data"}), 400

    print(f"Received data: Timestamp: {timestamp}, Temperature: {temperature}, Humidity: {humidity}")
    
    # You can save the data or process it further here.

    return jsonify({"message": "Data received successfully"}), 200

if __name__ == '__main__':
    # Use the environment variable for Render's port or fallback to 5000
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
