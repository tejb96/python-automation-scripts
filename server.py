from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_event():
    data = request.json  # This will capture the data sent by RuneLite
    print(data)  # You can process the data as needed
    return jsonify({"status": "success"}), 200

@app.route('/<event_type>/', methods=['POST'])
def handle_dynamic_event(event_type):
    data = request.json
    print(f"Event type: {event_type}, Data: {data}")
    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    # Bind to the loopback address to restrict access to only this machine
    app.run(host="127.0.0.1", port=8080)
