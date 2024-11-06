from flask import Flask, request, jsonify
from g4f.client import Client

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "API is running"})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        text = data.get('message', '')
        
        client = Client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a more stable model
            messages=[{"role": "user", "content": text}]
        )
        
        return jsonify({
            "response": response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500