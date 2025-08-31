# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv # <<< ADD THIS IMPORT
import os # <<< ADD THIS IMPORT

# --- ADD THIS LINE TO LOAD THE .ENV FILE ---
load_dotenv()
# -------------------------------------------

from chatbot import get_chatbot_response 

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message')

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # The get_chatbot_response function will now have access to the GROQ_API_KEY
        bot_response = get_chatbot_response(user_message)

        return jsonify({"reply": bot_response})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)