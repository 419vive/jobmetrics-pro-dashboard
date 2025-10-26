"""
AI-powered natural language query module using Claude API
"""
import anthropic
import pandas as pd
import json
import config
from analytics import SaaSAnalytics


class AIQueryEngine:
    """Natural language query engine powered by Claude"""

    def __init__(self):
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.analytics = SaaSAnalytics()

    def _get_metrics_context(self):
        """Get current metrics context for Claude"""
        context = {
            "current_mrr": f"${self.analytics.get_current_mrr():,.2f}",
            "mrr_growth_30d": f"{self.analytics.get_mrr_growth_rate(30):.2f}%",
            "arpu": f"${self.analytics.get_arpu():.2f}",
            "churn_rate": f"{self.analytics.get_churn_rate(30):.2f}%",
            "conversion_rate": f"{self.analytics.get_conversion_rate():.2f}%",
            "cac": f"${self.analytics.get_cac():.2f}",
            "ltv": f"${self.analytics.get_ltv():.2f}",
            "ltv_cac_ratio": f"{self.analytics.get_ltv_cac_ratio():.2f}",
            "dau": self.analytics.get_active_users('daily'),
            "wau": self.analytics.get_active_users('weekly'),
            "mau": self.analytics.get_active_users('monthly'),
            "avg_match_rate": f"{self.analytics.get_avg_match_rate():.2f}%",
            "avg_scans_per_user": f"{self.analytics.get_avg_scans_per_user():.2f}",
        }
        return context

    def query(self, user_question):
        """
        Process natural language query and return insights

        Args:
            user_question: Natural language question from user

        Returns:
            Dictionary with answer and relevant data
        """
        # Get current metrics
        metrics = self._get_metrics_context()

        # Get anomalies
        anomalies = self.analytics.detect_anomalies()

        # Build prompt for Claude
        prompt = f"""You are an expert SaaS analytics assistant for a job search/resume optimization platform (like Jobscan).

Current Metrics:
{json.dumps(metrics, indent=2)}

Recent Anomalies Detected:
{json.dumps(anomalies, indent=2) if anomalies else "No critical anomalies detected"}

User Question: {user_question}

Please provide a clear, concise answer to the user's question based on the metrics above. Include:
1. Direct answer to their question
2. Relevant context and insights
3. Actionable recommendations if applicable
4. Any concerning trends they should be aware of

Keep your response professional but conversational, as if you're talking to a product manager or business stakeholder."""

        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            answer = message.content[0].text

            return {
                "success": True,
                "answer": answer,
                "metrics_used": metrics,
                "anomalies": anomalies
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "answer": f"Sorry, I encountered an error: {str(e)}"
            }

    def get_insights(self):
        """Generate automatic insights about the business"""
        metrics = self._get_metrics_context()
        anomalies = self.analytics.detect_anomalies()

        prompt = f"""You are an expert SaaS analytics assistant for a job search/resume optimization platform.

Current Metrics:
{json.dumps(metrics, indent=2)}

Anomalies:
{json.dumps(anomalies, indent=2) if anomalies else "No critical anomalies detected"}

Please provide 3-5 key insights about the current state of the business. For each insight:
1. State the insight clearly
2. Explain why it matters
3. Suggest 1-2 specific actions

Format your response as a JSON array of objects with keys: "title", "insight", "impact", "actions" (array of strings)"""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract JSON from response
            response_text = message.content[0].text

            # Try to parse JSON from the response
            # Claude might wrap it in markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            insights = json.loads(response_text)

            return {
                "success": True,
                "insights": insights
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "insights": []
            }

    def explain_metric(self, metric_name):
        """Explain what a specific metric means and why it matters"""
        metrics = self._get_metrics_context()

        prompt = f"""You are an expert SaaS analytics assistant.

Current value of {metric_name}: {metrics.get(metric_name, 'Not available')}

Please explain:
1. What this metric means in simple terms
2. Why it's important for a SaaS business
3. What the current value indicates
4. Industry benchmarks or targets (if applicable)
5. How to improve this metric

Keep it concise and actionable."""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=512,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                "success": True,
                "explanation": message.content[0].text
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Test function
if __name__ == "__main__":
    try:
        engine = AIQueryEngine()

        # Test query
        print("Testing AI Query Engine...")
        print("="*60)

        result = engine.query("What's our churn rate and should I be worried?")
        print("\nQuestion: What's our churn rate and should I be worried?")
        print(f"\nAnswer:\n{result['answer']}")

        print("\n" + "="*60)

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("1. Set ANTHROPIC_API_KEY in .env file")
        print("2. Run data_generator.py first to create the datasets")
