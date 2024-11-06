from flask import Flask, request, jsonify, render_template
from g4f.client import Client
import asyncio

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        text = data.get('message')
        
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": text}],
        )
        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-image', methods=['POST'])
async def generate_image():
    try:
        data = request.json
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
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)