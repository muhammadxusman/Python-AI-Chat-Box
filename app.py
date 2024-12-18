from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Replace with your API key
API_KEY = "AIzaSyAIQrbxX43xemLmtoepPWxPCyidIA_XFYU"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route("/")
def home():
    # Serve the frontend HTML page
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": user_message}]}
        ]
    }

    try:
        # Send request to Google Gemini API
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse response
        gemini_response = response.json()
        reply = gemini_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

        # Return the reply to the frontend
        return jsonify({"reply": reply})

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return jsonify({"error": f"API Request failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
