"""
Configuration file for JobMetrics Pro Dashboard
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).parent.parent.parent  # Go up to project root
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Flask Configuration
FLASK_ENV = os.getenv("FLASK_ENV", "development")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5001))

# Streamlit Configuration
STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", 8501))

# Data Generation Parameters
NUM_USERS = 10000
DATE_RANGE_DAYS = 365
START_DATE = "2024-01-01"

# SaaS Metrics Thresholds (for anomaly detection)
THRESHOLDS = {
    "churn_rate": {"warning": 0.05, "critical": 0.08},
    "conversion_rate": {"warning": 0.02, "critical": 0.01},
    "avg_match_rate": {"warning": 0.65, "critical": 0.60},
    "mrr_growth": {"warning": -0.05, "critical": -0.10},
}

# Dashboard Configuration
DASHBOARD_TITLE = "JobMetrics Pro - Self-Service Analytics"
COMPANY_NAME = "Career Tech SaaS Platform"

# Email Notification Configuration
EMAIL_NOTIFICATIONS_ENABLED = os.getenv("EMAIL_NOTIFICATIONS_ENABLED", "false").lower() == "true"
EMAIL_FROM = os.getenv("EMAIL_FROM", "alerts@jobmetrics.com")
EMAIL_TO = os.getenv("EMAIL_TO", "admin@company.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# Slack Notification Configuration
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
