# Ghost AI Service

AI-powered blog content generation service for Ghost CMS using GroqCloud API.

## Features

- 🤖 AI blog generation using GroqCloud (Llama 3.3, Llama 4, GPT-OSS, Qwen3)
- 📝 Automatic publishing to Ghost CMS
- 🔒 Secure secret management with HashiCorp Vault
- 🚀 GitOps deployment with ArgoCD
- 📦 CI/CD with GitHub Actions

## API Endpoints

### Generate Blog Post
```bash
POST https://ghost-ai.quapton.com/generate-blog
Content-Type: application/json

{
  "topic": "The Future of AI in Healthcare",
  "status": "draft",
  "model": "llama-3.3-70b-versatile"
}
```

**Response:**
```json
{
  "success": true,
  "post_id": "abc123",
  "post_url": "https://ghost.quapton.com/the-future-of-ai-in-healthcare/",
  "title": "The Future of AI in Healthcare",
  "status": "draft"
}
```

### List Available Models
```bash
GET https://ghost-ai.quapton.com/models
```

**Response:**
```json
{
  "models": [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "openai/gpt-oss-120b",
    "qwen/qwen3-32b"
  ]
}
```

### Health Check
```bash
GET https://ghost-ai.quapton.com/health
```

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   User/API  │─────▶│  Ghost AI    │─────▶│  GroqCloud  │
│             │      │  Service     │      │     API     │
└─────────────┘      └──────┬───────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  Ghost CMS  │
                     │  Admin API  │
                     └─────────────┘
```

## Deployment

### Prerequisites
- Kubernetes cluster with ArgoCD
- HashiCorp Vault with secrets:
  - `secret/ghost/admin` (admin_api_key, api_url)
  - `secret/ghost/groq` (groq_key)
- Harbor registry credentials

### ArgoCD Application

Create ArgoCD application:
```bash
kubectl apply -f argocd-app.yaml
```

### GitHub Secrets

Configure in GitHub repository settings:
- `HARBOR_USERNAME`: Harbor registry username
- `HARBOR_PASSWORD`: Harbor registry password

## Development

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GHOST_ADMIN_API_KEY="your_key"
export GHOST_API_URL="https://ghost.quapton.com"
export GROQ_API_KEY="your_groq_key"

# Run locally
python app.py
```

### Build Docker Image
```bash
docker build -t ghost-ai-service:latest .
```

## Configuration

All sensitive configuration is managed through Vault:
- Ghost Admin API credentials
- GroqCloud API key
- Automatically synced to Kubernetes secrets via Vault Secrets Operator

## License

MIT