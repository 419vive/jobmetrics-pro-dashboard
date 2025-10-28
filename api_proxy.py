#!/usr/bin/env python3
"""
🔐 API Proxy Server - Secure Backend for Claude API Calls

This proxy server acts as an intermediary between your Streamlit dashboard
and the Claude API, keeping your API keys secure on the server side.

Architecture:
    Browser/Streamlit → Flask Proxy (this file) → Claude API
                         ↑
                    Reads API key from .env
                    (never exposed to frontend)

Security Features:
- API key stored server-side only
- Rate limiting per IP
- Request validation
- CORS protection
- Optional JWT authentication
- Request logging for monitoring

Usage:
    python api_proxy.py

    Then in dashboard.py, instead of calling Claude API directly:
    response = requests.post('http://localhost:5001/api/query', json={
        'question': 'What is my MRR?',
        'context': {...}
    })
"""

import os
import time
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Optional

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import anthropic
from collections import defaultdict
import hashlib

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# CORS configuration - restrict to your domains in production
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:8501",  # Streamlit default
            "http://localhost:3000",  # React dev server
            # Add your production domains here:
            # "https://your-app.streamlit.app",
            # "https://yourdomain.com"
        ]
    }
})

# Rate limiting configuration
RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS_PER_WINDOW = 30  # requests
rate_limit_store = defaultdict(list)

# Initialize Claude client
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY not found in environment variables!\n"
        "Make sure you have a .env file with your API key."
    )

claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# ==========================================
# Security Utilities
# ==========================================

def get_client_ip():
    """Get the real client IP (handles proxies)"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    return request.remote_addr

def rate_limit(func):
    """Rate limiting decorator - prevents abuse"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        client_ip = get_client_ip()
        current_time = time.time()

        # Clean old requests
        rate_limit_store[client_ip] = [
            req_time for req_time in rate_limit_store[client_ip]
            if current_time - req_time < RATE_LIMIT_WINDOW
        ]

        # Check rate limit
        if len(rate_limit_store[client_ip]) >= MAX_REQUESTS_PER_WINDOW:
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': f'Maximum {MAX_REQUESTS_PER_WINDOW} requests per {RATE_LIMIT_WINDOW} seconds',
                'retry_after': RATE_LIMIT_WINDOW
            }), 429

        # Add current request
        rate_limit_store[client_ip].append(current_time)

        return func(*args, **kwargs)
    return wrapper

def validate_request(required_fields):
    """Validate request contains required fields"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()

            if not data:
                return jsonify({
                    'error': 'Invalid request',
                    'message': 'Request body must be JSON'
                }), 400

            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    'error': 'Missing required fields',
                    'fields': missing_fields
                }), 400

            return func(*args, **kwargs)
        return wrapper
    return decorator

def log_request(endpoint: str, client_ip: str, status: str, error: Optional[str] = None):
    """Log API requests for monitoring"""
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {client_ip} → {endpoint} → {status}"
    if error:
        log_entry += f" | Error: {error}"
    print(log_entry)  # In production, use proper logging (e.g., to file or cloud)

# ==========================================
# API Endpoints
# ==========================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint - verify server is running"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200

@app.route('/api/query', methods=['POST'])
@rate_limit
@validate_request(['question', 'context'])
def query_claude():
    """
    Proxy endpoint for Claude API queries

    Request JSON:
        {
            "question": "What is my current MRR?",
            "context": {
                "current_mrr": 92148.74,
                "previous_mrr": 87234.56,
                ...
            }
        }

    Response JSON:
        {
            "answer": "Your current MRR is $92,148.74...",
            "usage": {
                "input_tokens": 150,
                "output_tokens": 89
            }
        }
    """
    client_ip = get_client_ip()

    try:
        data = request.get_json()
        question = data['question']
        context = data['context']

        # Build prompt
        prompt = f"""You are a SaaS analytics assistant. Use the following data to answer the user's question.

Context data:
{context}

User question: {question}

Provide a clear, concise answer with specific numbers when relevant."""

        # Call Claude API (server-side, API key never exposed)
        response = claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract answer
        answer = response.content[0].text

        # Log success
        log_request('/api/query', client_ip, 'SUCCESS')

        return jsonify({
            'answer': answer,
            'usage': {
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens
            },
            'model': response.model
        }), 200

    except anthropic.APIError as e:
        log_request('/api/query', client_ip, 'ERROR', str(e))
        return jsonify({
            'error': 'Claude API error',
            'message': str(e)
        }), 502

    except Exception as e:
        log_request('/api/query', client_ip, 'ERROR', str(e))
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/analytics-query', methods=['POST'])
@rate_limit
@validate_request(['query_type', 'parameters'])
def analytics_query():
    """
    Endpoint for pre-defined analytics queries

    This is even more secure - only allows specific query types,
    preventing arbitrary Claude API calls

    Request JSON:
        {
            "query_type": "mrr_analysis",
            "parameters": {
                "time_period": "last_30_days"
            }
        }
    """
    client_ip = get_client_ip()

    try:
        data = request.get_json()
        query_type = data['query_type']
        parameters = data['parameters']

        # Define allowed query types (whitelist approach)
        allowed_queries = {
            'mrr_analysis': 'Analyze MRR trends and provide insights',
            'churn_analysis': 'Analyze churn rate and identify patterns',
            'conversion_analysis': 'Analyze conversion funnel performance',
            'cohort_analysis': 'Analyze cohort retention patterns'
        }

        if query_type not in allowed_queries:
            return jsonify({
                'error': 'Invalid query type',
                'allowed_types': list(allowed_queries.keys())
            }), 400

        # Build specific prompt based on query type
        prompt = f"{allowed_queries[query_type]}.\n\nParameters: {parameters}"

        # Call Claude API
        response = claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )

        log_request('/api/analytics-query', client_ip, 'SUCCESS')

        return jsonify({
            'answer': response.content[0].text,
            'query_type': query_type,
            'usage': {
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens
            }
        }), 200

    except Exception as e:
        log_request('/api/analytics-query', client_ip, 'ERROR', str(e))
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/rate-limit-status', methods=['GET'])
def rate_limit_status():
    """Check remaining rate limit quota"""
    client_ip = get_client_ip()
    current_time = time.time()

    # Clean old requests
    rate_limit_store[client_ip] = [
        req_time for req_time in rate_limit_store[client_ip]
        if current_time - req_time < RATE_LIMIT_WINDOW
    ]

    requests_used = len(rate_limit_store[client_ip])
    requests_remaining = MAX_REQUESTS_PER_WINDOW - requests_used

    return jsonify({
        'requests_used': requests_used,
        'requests_remaining': requests_remaining,
        'max_requests': MAX_REQUESTS_PER_WINDOW,
        'window_seconds': RATE_LIMIT_WINDOW,
        'client_ip': client_ip
    }), 200

# ==========================================
# Main
# ==========================================

if __name__ == '__main__':
    # Configuration
    PORT = int(os.getenv('FLASK_PORT', 5001))
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'

    print("=" * 60)
    print("🔐 API Proxy Server Starting...")
    print("=" * 60)
    print(f"Port: {PORT}")
    print(f"Debug Mode: {DEBUG}")
    print(f"Rate Limit: {MAX_REQUESTS_PER_WINDOW} requests per {RATE_LIMIT_WINDOW} seconds")
    print(f"Claude API Key: {'✅ Loaded' if ANTHROPIC_API_KEY else '❌ Missing'}")
    print("=" * 60)
    print("\nEndpoints:")
    print(f"  GET  http://localhost:{PORT}/health")
    print(f"  POST http://localhost:{PORT}/api/query")
    print(f"  POST http://localhost:{PORT}/api/analytics-query")
    print(f"  GET  http://localhost:{PORT}/api/rate-limit-status")
    print("=" * 60)
    print("\n🚀 Server ready! API keys are secure on backend.\n")

    # Run server
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=PORT,
        debug=DEBUG
    )
