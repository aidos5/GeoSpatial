from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def receive_data():
    # Parse incoming JSON data
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Print received data to the console (for testing)
    print("Received data:", data)

    # Respond to the client
    return jsonify({"message": "Data received successfully!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
