import os
import jwt
import time
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app, origins=['https://ghost.quapton.com'])

GHOST_ADMIN_API_KEY = os.getenv('GHOST_ADMIN_API_KEY')
GHOST_API_URL = os.getenv('GHOST_API_URL', 'https://ghost.quapton.com')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

groq_client = Groq(api_key=GROQ_API_KEY)

def generate_ghost_token():
    key_id, secret = GHOST_ADMIN_API_KEY.split(':')

    iat = int(datetime.now().timestamp())

    header = {'alg': 'HS256', 'typ': 'JWT', 'kid': key_id}
    payload = {
        'iat': iat,
        'exp': iat + 5 * 60,
        'aud': '/admin/'
    }

    token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)
    return token

def generate_blog_content(topic, model='llama-3.3-70b-versatile'):
    prompt = f"""Write a comprehensive, SEO-optimized blog post about: {topic}

Requirements:
- Create an engaging title
- Write a compelling introduction
- Include 3-5 main sections with subheadings
- Add actionable insights and examples
- Write a strong conclusion
- Use markdown formatting
- Make it approximately 1000-1500 words

Format the response as JSON with keys: "title", "content" (in markdown)"""

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an expert blog writer who creates engaging, informative, and SEO-optimized content."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model=model,
        temperature=0.7,
        max_tokens=8000,
        response_format={"type": "json_object"}
    )

    return chat_completion.choices[0].message.content

def publish_to_ghost(title, content, status='draft'):
    import requests

    token = generate_ghost_token()

    url = f"{GHOST_API_URL}/ghost/api/admin/posts/"

    headers = {
        'Authorization': f'Ghost {token}',
        'Content-Type': 'application/json'
    }

    post_data = {
        'posts': [{
            'title': title,
            'html': content,
            'status': status,
            'tags': []
        }]
    }

    response = requests.post(url, json=post_data, headers=headers)
    response.raise_for_status()

    return response.json()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/generate-blog', methods=['POST'])
def generate_blog():
    try:
        data = request.json
        topic = data.get('topic')
        status = data.get('status', 'draft')
        model = data.get('model', 'llama-3.3-70b-versatile')

        if not topic:
            return jsonify({'error': 'Topic is required'}), 400

        app.logger.info(f"Generating blog for topic: {topic}")

        blog_content = generate_blog_content(topic, model)

        import json
        blog_json = json.loads(blog_content)

        title = blog_json.get('title', topic)
        content = blog_json.get('content', '')

        app.logger.info(f"Publishing to Ghost: {title}")

        result = publish_to_ghost(title, content, status)

        return jsonify({
            'success': True,
            'post_id': result['posts'][0]['id'],
            'post_url': result['posts'][0]['url'],
            'title': title,
            'status': status
        }), 201

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/models', methods=['GET'])
def list_models():
    models = [
        'llama-3.3-70b-versatile',
        'llama-3.1-8b-instant',
        'meta-llama/llama-4-maverick-17b-128e-instruct',
        'meta-llama/llama-4-scout-17b-16e-instruct',
        'openai/gpt-oss-120b',
        'qwen/qwen3-32b'
    ]
    return jsonify({'models': models}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)