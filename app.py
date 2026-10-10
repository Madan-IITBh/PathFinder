import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

# Serve static files from the current directory
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Initialize Gemini Client (Requires GEMINI_API_KEY in environment variables)
client = genai.Client()

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"success": False, "error": "Message is required"}), 400

        # System prompt setting the persona for IIT Bhilai
        prompt = f"""You are Pathfinder, IIT Bhilai's helpful course registration assistant. 
        Answer the following student query concisely and accurately. 
        Return ONLY a JSON object with a single key "reply" containing your response.
        Query: {user_message}"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        
        # Parse the JSON string returned by Gemini
        gemini_data = json.loads(response.text)
        
        return jsonify({"success": True, "data": gemini_data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    # debug=False is safer for deployment environments
    app.run(debug=False, host="0.0.0.0", port=port)
