"""
🔐 API Proxy Client - Safe way to call Claude API from frontend

This module provides a client for calling the API proxy server,
which keeps your API keys secure on the backend.

Usage in dashboard.py:
    from api_proxy_client import ProxyClient

    # Initialize client
    client = ProxyClient(base_url='http://localhost:5001')

    # Query Claude through the proxy
    response = client.query(
        question='What is my current MRR?',
        context={'current_mrr': 92148.74, ...}
    )

    print(response['answer'])
"""

import requests
from typing import Dict, Optional, Any
import time


class ProxyClient:
    """Client for communicating with the API proxy server"""

    def __init__(self, base_url: str = 'http://localhost:5001', timeout: int = 30):
        """
        Initialize proxy client

        Args:
            base_url: URL of the proxy server (default: http://localhost:5001)
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def health_check(self) -> bool:
        """
        Check if proxy server is healthy

        Returns:
            bool: True if server is healthy, False otherwise
        """
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def query(
        self,
        question: str,
        context: Dict[str, Any],
        retry_on_rate_limit: bool = True,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Query Claude API through the proxy

        Args:
            question: User's question
            context: Context data for the query
            retry_on_rate_limit: Automatically retry if rate limited
            max_retries: Maximum number of retries

        Returns:
            Dict containing:
                - answer: Claude's response
                - usage: Token usage stats
                - model: Model used

        Raises:
            ProxyClientError: If request fails
            RateLimitError: If rate limit exceeded (after retries)
        """
        url = f"{self.base_url}/api/query"
        payload = {
            'question': question,
            'context': context
        }

        for attempt in range(max_retries):
            try:
                response = self.session.post(
                    url,
                    json=payload,
                    timeout=self.timeout
                )

                # Handle rate limiting
                if response.status_code == 429:
                    if not retry_on_rate_limit or attempt == max_retries - 1:
                        raise RateLimitError(
                            "Rate limit exceeded. Try again later.",
                            retry_after=response.json().get('retry_after', 60)
                        )

                    # Wait and retry
                    wait_time = min(2 ** attempt, 10)  # Exponential backoff, max 10s
                    time.sleep(wait_time)
                    continue

                # Handle other errors
                if response.status_code != 200:
                    error_data = response.json()
                    raise ProxyClientError(
                        f"Proxy error: {error_data.get('message', 'Unknown error')}",
                        status_code=response.status_code
                    )

                return response.json()

            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    raise ProxyClientError(f"Request failed: {str(e)}")
                time.sleep(2 ** attempt)

        raise ProxyClientError("Max retries exceeded")

    def analytics_query(
        self,
        query_type: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Pre-defined analytics query (more secure)

        Args:
            query_type: Type of analysis (e.g., 'mrr_analysis')
            parameters: Query parameters

        Returns:
            Dict containing analysis results

        Raises:
            ProxyClientError: If request fails
        """
        url = f"{self.base_url}/api/analytics-query"
        payload = {
            'query_type': query_type,
            'parameters': parameters
        }

        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code != 200:
                error_data = response.json()
                raise ProxyClientError(
                    f"Proxy error: {error_data.get('message', 'Unknown error')}",
                    status_code=response.status_code
                )

            return response.json()

        except requests.RequestException as e:
            raise ProxyClientError(f"Request failed: {str(e)}")

    def get_rate_limit_status(self) -> Dict[str, Any]:
        """
        Check current rate limit status

        Returns:
            Dict containing:
                - requests_used: Number of requests used in current window
                - requests_remaining: Number of requests remaining
                - max_requests: Maximum requests allowed
                - window_seconds: Time window in seconds
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/rate-limit-status",
                timeout=5
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {'error': 'Failed to get rate limit status'}

        except requests.RequestException:
            return {'error': 'Connection failed'}


# ==========================================
# Custom Exceptions
# ==========================================

class ProxyClientError(Exception):
    """Base exception for proxy client errors"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class RateLimitError(ProxyClientError):
    """Exception raised when rate limit is exceeded"""
    def __init__(self, message: str, retry_after: int):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


# ==========================================
# Example Usage
# ==========================================

def example_usage():
    """Example of how to use the proxy client"""

    # Initialize client
    client = ProxyClient(base_url='http://localhost:5001')

    # 1. Health check
    print("Checking proxy server health...")
    if not client.health_check():
        print("❌ Proxy server is not healthy!")
        return
    print("✅ Proxy server is healthy\n")

    # 2. Check rate limit status
    print("Checking rate limit status...")
    status = client.get_rate_limit_status()
    print(f"Requests remaining: {status.get('requests_remaining', 'unknown')}\n")

    # 3. Query Claude through proxy
    print("Querying Claude through proxy...")
    try:
        response = client.query(
            question="What is my current MRR and how does it compare to last month?",
            context={
                'current_mrr': 92148.74,
                'previous_mrr': 87234.56,
                'growth_rate': 5.63
            }
        )

        print(f"Answer: {response['answer']}")
        print(f"\nUsage:")
        print(f"  Input tokens: {response['usage']['input_tokens']}")
        print(f"  Output tokens: {response['usage']['output_tokens']}")

    except RateLimitError as e:
        print(f"❌ Rate limited! Retry after {e.retry_after} seconds")

    except ProxyClientError as e:
        print(f"❌ Error: {e.message}")

    # 4. Pre-defined analytics query
    print("\n\nRunning pre-defined analytics query...")
    try:
        response = client.analytics_query(
            query_type='mrr_analysis',
            parameters={
                'time_period': 'last_30_days'
            }
        )

        print(f"Analysis: {response['answer']}")

    except ProxyClientError as e:
        print(f"❌ Error: {e.message}")


if __name__ == '__main__':
    example_usage()
