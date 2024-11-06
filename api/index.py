from flask import Flask, request, jsonify, render_template
from g4f.client import Client
import asyncio
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/_vercel/deploy-complete', methods=['POST'])
def deploy_complete():
    return jsonify({"status": "ok"})

@app.route('/', methods=['GET'])
def home():
    return "API is running"

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
            
        text = data.get('message')
        
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": text}],
        )
        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-image', methods=['POST'])
async def generate_image():
    try:
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({"error": "No prompt provided"}), 400
            
        prompt = data.get('prompt')
        
        client = Client()
        response = await client.images.async_generate(
            model="sdxl",
            prompt=prompt,
            n=1
        )
        image_url = response.data[0].url
        return jsonify({"url": image_url})
    except Exception as e:
        print(f"Error in generate-image endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500