# 🔐 API Security Architecture - Backend Proxy Implementation

**Purpose**: Enterprise-grade security for API keys using backend proxy pattern
**Audience**: Developers, DevOps engineers
**Last Updated**: 2025-10-28
**Security Level**: 🔴 Production-ready

---

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Security Layers                         │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│              │         │              │         │              │
│   Browser    │────────▶│  Flask Proxy │────────▶│  Claude API  │
│  (Frontend)  │         │  (Backend)   │         │              │
│              │         │              │         │              │
└──────────────┘         └──────────────┘         └──────────────┘
      │                         │                         │
      │                         │                         │
   ❌ No API key          ✅ Has API key           ✅ Validates
   ❌ Untrusted          ✅ Rate limiting               requests
   ✅ Can't see key      ✅ Request validation
                         ✅ CORS protection
                         ✅ Logging & monitoring
```

---

## 🛡️ Why Backend Proxy?

### ❌ Direct API Calls (Insecure)

```python
# dashboard.py - BAD! API key exposed to browser
import anthropic

api_key = "sk-ant-api03-..."  # 🚨 Exposed in frontend!
client = anthropic.Anthropic(api_key=api_key)
response = client.messages.create(...)
```

**Problems**:
1. API key visible in browser DevTools
2. Anyone can copy your key from network requests
3. No rate limiting (users can abuse your quota)
4. No request validation
5. No audit trail

---

### ✅ Backend Proxy (Secure)

```python
# dashboard.py - GOOD! API key stays on server
import requests

response = requests.post('http://localhost:5001/api/query', json={
    'question': 'What is my MRR?',
    'context': {...}
})
answer = response.json()['answer']
```

**Benefits**:
1. ✅ API key never leaves the server
2. ✅ Rate limiting per IP address
3. ✅ Request validation & sanitization
4. ✅ Centralized logging & monitoring
5. ✅ CORS protection
6. ✅ Can add authentication layer
7. ✅ Cost control (limit queries)

---

## 📁 Files Created

### 1. `api_proxy.py` - Backend Server

**What it does**:
- Runs a Flask server on port 5001
- Exposes secure API endpoints
- Reads API key from `.env` (server-side only)
- Calls Claude API on behalf of frontend
- Implements rate limiting (30 requests/60 seconds per IP)
- Logs all requests for monitoring

**Endpoints**:
- `GET /health` - Health check
- `POST /api/query` - General Claude queries
- `POST /api/analytics-query` - Pre-defined analytics queries (whitelist)
- `GET /api/rate-limit-status` - Check quota remaining

---

### 2. `api_proxy_client.py` - Frontend Client

**What it does**:
- Provides `ProxyClient` class for easy integration
- Handles errors & retries
- Automatic rate limit backoff
- Clean API for dashboard.py

**Usage**:
```python
from api_proxy_client import ProxyClient

client = ProxyClient(base_url='http://localhost:5001')
response = client.query(
    question='What is my MRR?',
    context={'current_mrr': 92148.74}
)
print(response['answer'])
```

---

## 🚀 Setup Instructions

### Step 1: Install Dependencies

```bash
pip install flask flask-cors anthropic requests python-dotenv
```

Or update `requirements.txt`:
```txt
flask==3.0.0
flask-cors==4.0.0
anthropic==0.25.0
requests==2.31.0
python-dotenv==1.0.0
```

---

### Step 2: Start the Proxy Server

```bash
# Terminal 1: Start proxy server
python api_proxy.py
```

Output:
```
============================================================
🔐 API Proxy Server Starting...
============================================================
Port: 5001
Debug Mode: True
Rate Limit: 30 requests per 60 seconds
Claude API Key: ✅ Loaded
============================================================

Endpoints:
  GET  http://localhost:5001/health
  POST http://localhost:5001/api/query
  POST http://localhost:5001/api/analytics-query
  GET  http://localhost:5001/api/rate-limit-status
============================================================

🚀 Server ready! API keys are secure on backend.
```

---

### Step 3: Test the Proxy

```bash
# Terminal 2: Test health check
curl http://localhost:5001/health

# Should return:
# {"status":"healthy","timestamp":"2025-10-28T10:00:00","version":"1.0.0"}
```

---

### Step 4: Integrate with Dashboard

#### Option A: Direct Requests (Simple)

```python
# In dashboard.py, replace direct Claude API calls with:
import requests

def ask_claude(question: str, context: dict) -> str:
    """Query Claude through secure proxy"""
    try:
        response = requests.post(
            'http://localhost:5001/api/query',
            json={
                'question': question,
                'context': context
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json()['answer']
        else:
            return f"Error: {response.json().get('message', 'Unknown error')}"

    except requests.RequestException as e:
        return f"Connection error: {str(e)}"

# Usage
answer = ask_claude(
    question="What is my current MRR?",
    context={'current_mrr': 92148.74, 'previous_mrr': 87234.56}
)
print(answer)
```

---

#### Option B: Use ProxyClient (Recommended)

```python
# In dashboard.py
from api_proxy_client import ProxyClient, ProxyClientError

# Initialize once (can cache with @st.cache_resource)
proxy_client = ProxyClient(base_url='http://localhost:5001')

def ask_claude_safe(question: str, context: dict) -> str:
    """Query Claude through proxy with error handling"""
    try:
        # Check server health first
        if not proxy_client.health_check():
            return "⚠️ Proxy server unavailable. Please start api_proxy.py"

        # Query through proxy
        response = proxy_client.query(question, context)
        return response['answer']

    except ProxyClientError as e:
        return f"Error: {e.message}"

# Usage
answer = ask_claude_safe(
    question="What is my current MRR?",
    context={'current_mrr': 92148.74}
)
print(answer)
```

---

## 🔒 Security Features Explained

### 1. Rate Limiting

**What**: Limits requests to 30 per 60 seconds per IP address
**Why**: Prevents abuse and controls costs
**How**:
```python
# Automatically applied to all endpoints via @rate_limit decorator
@rate_limit
def query_claude():
    ...
```

**When triggered**:
```json
{
  "error": "Rate limit exceeded",
  "message": "Maximum 30 requests per 60 seconds",
  "retry_after": 60
}
```

---

### 2. Request Validation

**What**: Ensures requests contain required fields
**Why**: Prevents malformed requests and injection attacks
**How**:
```python
@validate_request(['question', 'context'])
def query_claude():
    # Only executes if 'question' and 'context' present
    ...
```

**Blocked requests**:
```json
{
  "error": "Missing required fields",
  "fields": ["question"]
}
```

---

### 3. CORS Protection

**What**: Only allows requests from trusted domains
**Why**: Prevents unauthorized websites from using your proxy
**Configuration**:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:8501",  # Streamlit
            "https://your-app.streamlit.app"  # Production
        ]
    }
})
```

---

### 4. Request Logging

**What**: Logs all API requests with IP, endpoint, status
**Why**: Audit trail for security monitoring
**Example logs**:
```
[2025-10-28T10:00:00] 127.0.0.1 → /api/query → SUCCESS
[2025-10-28T10:00:05] 127.0.0.1 → /api/query → ERROR | Error: Rate limit exceeded
```

---

### 5. Whitelisted Queries

**What**: Pre-defined query types (even more secure)
**Why**: Limits what users can ask Claude
**Usage**:
```python
# Only allows specific query types
client.analytics_query(
    query_type='mrr_analysis',  # Must be in whitelist
    parameters={'time_period': 'last_30_days'}
)
```

**Allowed query types**:
- `mrr_analysis` - MRR trends and insights
- `churn_analysis` - Churn rate patterns
- `conversion_analysis` - Funnel performance
- `cohort_analysis` - Retention patterns

---

## 🚀 Production Deployment

### Deployment Options

#### Option 1: Same Server as Dashboard (Simple)

```bash
# Run both on same server
python api_proxy.py &     # Port 5001
streamlit run dashboard.py # Port 8501
```

**Pros**: Simple, no CORS issues
**Cons**: Single point of failure

---

#### Option 2: Separate Backend Server (Recommended)

```
Frontend: https://your-app.streamlit.app
Backend:  https://api.yourdomain.com
```

**Update CORS origins**:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-app.streamlit.app"]
    }
})
```

**Update client**:
```python
client = ProxyClient(base_url='https://api.yourdomain.com')
```

---

#### Option 3: Serverless (AWS Lambda, Cloud Run)

**Deploy proxy as serverless function**:
- AWS Lambda + API Gateway
- Google Cloud Run
- Azure Functions

**Benefits**:
- Auto-scaling
- Pay per request
- No server management

**Example (Cloud Run)**:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY api_proxy.py .
CMD ["python", "api_proxy.py"]
```

```bash
gcloud run deploy api-proxy \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

### Environment Variables (Production)

Use cloud secret managers:

**AWS Secrets Manager**:
```python
import boto3
import json

def get_secret():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId='anthropic-api-key')
    return json.loads(response['SecretString'])['api_key']

ANTHROPIC_API_KEY = get_secret()
```

**GCP Secret Manager**:
```python
from google.cloud import secretmanager

def get_secret():
    client = secretmanager.SecretManagerServiceClient()
    name = "projects/PROJECT_ID/secrets/anthropic-api-key/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode('UTF-8')

ANTHROPIC_API_KEY = get_secret()
```

---

## 📊 Monitoring & Alerts

### What to Monitor

1. **Request Rate**: Unusual spikes?
2. **Error Rate**: More errors than usual?
3. **Response Time**: Slow responses?
4. **Cost**: API usage within budget?

---

### Setup Logging (Production)

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
handler = RotatingFileHandler(
    'api_proxy.log',
    maxBytes=10_000_000,  # 10MB
    backupCount=5
)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Use in endpoints
logger.info(f"{client_ip} → /api/query → SUCCESS")
logger.error(f"{client_ip} → /api/query → ERROR: {str(e)}")
```

---

### Setup Alerts

**CloudWatch (AWS)**:
```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Send custom metric
cloudwatch.put_metric_data(
    Namespace='APIProxy',
    MetricData=[{
        'MetricName': 'APIErrors',
        'Value': 1,
        'Unit': 'Count'
    }]
)
```

---

## 🧪 Testing

### Unit Tests

```python
# test_api_proxy.py
import unittest
from api_proxy import app

class TestAPIProxy(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json)

    def test_rate_limiting(self):
        # Make 31 requests (limit is 30)
        for i in range(31):
            response = self.app.post('/api/query', json={
                'question': 'test',
                'context': {}
            })

        # Last request should be rate limited
        self.assertEqual(response.status_code, 429)

    def test_missing_fields(self):
        response = self.app.post('/api/query', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
```

---

### Load Testing

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test with 100 requests, 10 concurrent
ab -n 100 -c 10 -p query.json -T application/json \
   http://localhost:5001/api/query
```

---

## 📋 Checklist: Before Going Live

### Security
- [ ] API key in `.env` (not hardcoded)
- [ ] `.env` in `.gitignore`
- [ ] CORS configured for production domains only
- [ ] Rate limiting enabled
- [ ] Request validation active
- [ ] HTTPS enabled (TLS certificate)
- [ ] Logging configured

### Performance
- [ ] Load tested (can handle expected traffic)
- [ ] Error handling for all endpoints
- [ ] Timeout configured (prevent hanging requests)
- [ ] Health check endpoint working

### Monitoring
- [ ] Logging to file or cloud
- [ ] Alerts configured (error rate, cost)
- [ ] Dashboard for metrics
- [ ] Cost tracking enabled

### Documentation
- [ ] API documentation for team
- [ ] Deployment runbook
- [ ] Incident response plan

---

## 🆘 Troubleshooting

### Problem: "Connection refused"

**Cause**: Proxy server not running
**Fix**:
```bash
python api_proxy.py
```

---

### Problem: "CORS error"

**Cause**: Frontend domain not in allowed origins
**Fix**: Update CORS config in `api_proxy.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://your-frontend-domain.com"]
    }
})
```

---

### Problem: "Rate limit exceeded"

**Cause**: Too many requests from same IP
**Fix**: Wait 60 seconds or increase limit:
```python
MAX_REQUESTS_PER_WINDOW = 60  # Increase from 30
```

---

### Problem: "504 Gateway Timeout"

**Cause**: Claude API taking too long
**Fix**: Increase timeout:
```python
response = requests.post(url, json=data, timeout=60)  # Increase from 30
```

---

## 📚 Additional Security Enhancements

### 1. JWT Authentication

Add user authentication:
```python
import jwt

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.InvalidTokenError:
        return None

@app.route('/api/query', methods=['POST'])
def query_claude():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_id = verify_token(token)

    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # Process request...
```

---

### 2. IP Whitelisting

Allow only specific IPs:
```python
ALLOWED_IPS = ['1.2.3.4', '5.6.7.8']

def ip_whitelist(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        client_ip = get_client_ip()
        if client_ip not in ALLOWED_IPS:
            return jsonify({'error': 'IP not allowed'}), 403
        return func(*args, **kwargs)
    return wrapper
```

---

### 3. Request Signing

Verify requests come from your app:
```python
import hmac

def verify_signature(payload, signature):
    expected = hmac.new(
        SECRET_KEY.encode(),
        payload.encode(),
        'sha256'
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

---

## ✅ Summary

**What you've implemented**:
1. ✅ Backend proxy server (`api_proxy.py`)
2. ✅ Client library (`api_proxy_client.py`)
3. ✅ Rate limiting (30 requests/60s per IP)
4. ✅ Request validation
5. ✅ CORS protection
6. ✅ Request logging
7. ✅ Health check endpoint
8. ✅ Error handling

**Security achieved**:
- 🔒 API key never exposed to frontend
- 🔒 Rate limiting prevents abuse
- 🔒 CORS blocks unauthorized domains
- 🔒 Request validation prevents injection
- 🔒 Audit trail for all requests

**Next steps**:
1. Test locally: `python api_proxy.py`
2. Integrate with dashboard
3. Deploy to production
4. Setup monitoring
5. Configure alerts

---

**Your API keys are now enterprise-grade secure! 🚀🔐**

*Last updated: 2025-10-28 by Jerry Lai*
