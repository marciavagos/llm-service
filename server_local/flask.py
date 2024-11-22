from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Environment variables
LLAMA_SERVER_URL = os.getenv("LLAMA_SERVER_URL", "http://localhost:8000")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "default_model")

@app.route("/inference", methods=["POST"])
def inference():
    try:
        # Get request JSON
        data = request.json
        if not data:
            return jsonify({"error": "Invalid request, JSON payload is required"}), 400

        # Extract parameters
        model = data.get("model", DEFAULT_MODEL)
        prompt = data.get("prompt", "")
        max_tokens = data.get("max_tokens", 100)
        temperature = data.get("temperature", 0.7)

        # Build the payload for llama-server
        payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        # Send request to llama-server
        response = requests.post(f"{LLAMA_SERVER_URL}/completion", json=payload)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Error from llama-server", "details": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == "__main__":
    # Run the server on host 0.0.0.0 to make it accessible from outside the container
    app.run(host="0.0.0.0", port=5000, debug=True)
