import os
import jwt
import time
import markdown
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app, origins=['https://ghost.quapton.com', 'https://ghost-ai.quapton.com'])

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
        content_markdown = blog_json.get('content', '')

        # Convert markdown to HTML
        content_html = markdown.markdown(content_markdown, extensions=['extra', 'codehilite', 'nl2br', 'tables'])

        app.logger.info(f"Publishing to Ghost: {title}")

        result = publish_to_ghost(title, content_html, status)

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

@app.route('/', methods=['GET'])
def index():
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost AI Blog Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            width: 100%;
            max-width: 500px;
        }

        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }

        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
            font-size: 14px;
        }

        input, select, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }

        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }

        textarea {
            resize: vertical;
            min-height: 100px;
        }

        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }

        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            display: none;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            display: block;
        }

        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            display: block;
        }

        .status.loading {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
            display: block;
        }

        .status a {
            color: inherit;
            font-weight: bold;
        }

        .ghost-link {
            display: inline-block;
            margin-top: 20px;
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
        }

        .ghost-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✨ Ghost AI Blog Generator</h1>
        <p class="subtitle">Generate SEO-optimized blog posts with AI</p>

        <form id="aiForm">
            <div class="form-group">
                <label for="topic">Blog Topic *</label>
                <textarea
                    id="topic"
                    placeholder="e.g., The Future of Renewable Energy in 2025
or
10 Best Practices for Kubernetes Security
or
How AI is Transforming Healthcare"
                    required
                ></textarea>
            </div>

            <div class="form-group">
                <label for="model">AI Model</label>
                <select id="model">
                    <option value="llama-3.3-70b-versatile">Llama 3.3 70B (Best Quality)</option>
                    <option value="llama-3.1-8b-instant" selected>Llama 3.1 8B (Fast)</option>
                    <option value="meta-llama/llama-4-maverick-17b-128e-instruct">Llama 4 Maverick</option>
                    <option value="meta-llama/llama-4-scout-17b-16e-instruct">Llama 4 Scout</option>
                    <option value="openai/gpt-oss-120b">GPT-OSS 120B</option>
                    <option value="qwen/qwen3-32b">Qwen3 32B</option>
                </select>
            </div>

            <div class="form-group">
                <label for="status">Post Status</label>
                <select id="status">
                    <option value="draft">Save as Draft</option>
                    <option value="published">Publish Immediately</option>
                </select>
            </div>

            <button type="submit" id="submitBtn">Generate Blog Post</button>

            <div id="status" class="status"></div>
        </form>

        <a href="https://ghost.quapton.com/ghost/" class="ghost-link" target="_blank">
            ← Back to Ghost Admin
        </a>
    </div>

    <script>
        const form = document.getElementById('aiForm');
        const submitBtn = document.getElementById('submitBtn');
        const statusDiv = document.getElementById('status');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const topic = document.getElementById('topic').value.trim();
            const model = document.getElementById('model').value;
            const status = document.getElementById('status').value;

            if (!topic) {
                showStatus('error', 'Please enter a blog topic');
                return;
            }

            submitBtn.disabled = true;
            submitBtn.textContent = 'Generating...';
            showStatus('loading', '🤖 AI is writing your blog post... This may take 30-60 seconds.');

            try {
                const response = await fetch('/generate-blog', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        topic: topic,
                        model: model,
                        status: status
                    })
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    showStatus('success',
                        `✅ Success! Post "${data.title}" has been ${data.status === 'published' ? 'published' : 'saved as draft'}.<br><br>` +
                        `<a href="${data.post_url}" target="_blank">📝 View Post</a> | ` +
                        `<a href="https://ghost.quapton.com/ghost/#/posts" target="_blank">📚 View All Posts</a>`
                    );
                    form.reset();
                } else {
                    showStatus('error', `❌ Error: ${data.error || 'Failed to generate post'}`);
                }
            } catch (error) {
                showStatus('error', `❌ Network error: ${error.message}`);
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Generate Blog Post';
            }
        });

        function showStatus(type, message) {
            statusDiv.className = `status ${type}`;
            statusDiv.innerHTML = message;
        }
    </script>
</body>
</html>'''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)