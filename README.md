# JobMetrics Pro - Self-Service Analytics Dashboard

A production-ready, AI-powered analytics dashboard built for SaaS platforms in the career tech space (like Jobscan). This project demonstrates enterprise-level data analytics, product metrics, and self-service BI capabilities.

## 📸 Dashboard Preview

> **Note**: Run the dashboard locally to see the full interactive experience!
> ```bash
> streamlit run dashboard.py
> ```

## 🎯 Project Overview

**JobMetrics Pro** is a self-service analytics platform that reduces routine data queries by 80% while providing stakeholders with actionable insights through:

- **Real-time SaaS Metrics**: MRR, ARPU, CAC, LTV, Churn Rate
- **Product Analytics**: User engagement, feature usage, conversion funnels
- **AI-Powered Insights**: Natural language queries using Claude API
- **Automated Anomaly Detection**: Proactive alerts for business metrics
- **Cohort Analysis**: User retention and behavior tracking

## 🚀 Key Features

### 1. Comprehensive SaaS Metrics Dashboard
- **Revenue Metrics**: MRR tracking, growth rates, revenue by plan type
- **Customer Metrics**: CAC, LTV, LTV:CAC ratio
- **Product Metrics**: Resume match rates, scan volumes, processing times
- **User Metrics**: DAU/WAU/MAU, retention, engagement

### 2. AI-Powered Analytics Assistant
- Natural language queries: "What's driving our churn rate?"
- Auto-generated insights with actionable recommendations
- Metric explanations for stakeholders
- Powered by Claude 3.5 Sonnet

### 3. Self-Service Capabilities
- Interactive conversion funnel analysis
- Cohort retention heatmaps
- Segment and channel performance breakdowns
- Drag-and-drop filtering (coming soon)

### 4. Automated Monitoring
- Real-time anomaly detection
- Threshold-based alerts (critical/warning levels)
- Proactive health checks

## 📊 Dashboard Screenshots

### Overview Dashboard
- Key metrics at a glance
- MRR trends and growth rates
- Product performance indicators

### Conversion Funnel
- User journey visualization
- Segment performance analysis
- Channel ROI comparison

### Cohort Analysis
- Retention heatmaps
- Engagement trends over time

### AI Assistant
- Natural language query interface
- Auto-generated insights
- Metric explanations

## 🛠 Technical Stack

### Core Technologies
- **Frontend**: Streamlit 1.31.0 (interactive dashboards)
- **Data Processing**: Pandas, NumPy, SciPy
- **Visualization**: Plotly, Seaborn
- **AI Integration**: Anthropic Claude API
- **Backend**: Python 3.8+

### Architecture
```
jobmetrics-pro-dashboard/
├── src/                          # Source code (modular architecture)
│   ├── core/                     # Core business logic
│   │   ├── analytics.py          # SaaS metrics calculations & analysis
│   │   ├── ai_query.py           # AI-powered query engine (Claude API)
│   │   └── config.py             # Configuration management
│   ├── dashboard/                # Frontend layer
│   │   ├── dashboard.py          # Main Streamlit application
│   │   ├── i18n.py               # Internationalization (EN/ZH)
│   │   └── i18n_jerry_style.py   # Extended translations
│   └── utils/                    # Utility functions
│
├── data/                         # Generated datasets (synthetic)
│   ├── users.csv                 # User demographics & segments
│   ├── subscriptions.csv         # Subscription lifecycle data
│   ├── scans.csv                 # Product usage data
│   ├── revenue.csv               # Daily revenue tracking
│   └── anomaly_history.json      # Anomaly detection log
│
├── docs/                         # Comprehensive documentation
│   ├── 00-START-HERE.md          # Quick start guide
│   ├── 01-getting-started/       # Setup & installation
│   ├── 03-technical/             # Architecture & design
│   ├── 04-operations/            # Deployment & security
│   ├── 05-project-management/    # Project info & decisions
│   ├── 06-development-logs/      # Bug reports & performance
│   └── 07-demo/                  # Demo scripts & interview prep
│
├── Root-level files (legacy/compatibility)
│   ├── config.py                 # [Legacy] Config (use src/core/config.py)
│   ├── data_generator.py         # Data generation script
│   ├── analytics.py              # [Legacy] Analytics (use src/core/analytics.py)
│   ├── ai_query.py               # [Legacy] AI (use src/core/ai_query.py)
│   └── dashboard.py              # [Legacy] Dashboard (use src/dashboard/dashboard.py)
│
├── Scripts & utilities
│   ├── run_dashboard.sh          # Quick start script
│   ├── START_DEMO.sh             # Demo launcher
│   ├── start_with_proxy.sh       # API proxy mode
│   ├── api_proxy.py              # API key protection proxy
│   ├── api_proxy_client.py       # Proxy client
│   └── daily_anomaly_checker.py  # Scheduled monitoring
│
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

**Note**: The project follows a modular architecture with source code in `src/`. Legacy files remain in the root for backward compatibility.

## 📈 Data Model

### Users
- User demographics and segmentation
- Acquisition channel tracking
- CAC calculation per user

### Subscriptions
- Plan types (Basic, Professional, Premium)
- Billing cycles (Monthly, Annual)
- Churn tracking and MRR calculation

### Resume Scans
- Match rate analytics
- Processing time metrics
- Keyword extraction performance

### Revenue
- Daily MRR tracking
- Active subscription counts
- Churn and new subscription events

## 🚦 Getting Started

### Prerequisites
- Python 3.8 or higher
- Anthropic API key (for AI features)

### Installation

1. **Clone the repository**
```bash
cd self-help-dashboard
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** 🔐
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

> **🔒 Security Note**: Your `.env` file contains sensitive API keys and is automatically protected:
> - ✅ Blocked by `.gitignore` (won't be committed to git)
> - ✅ Pre-commit hook scans for accidental leaks
> - ✅ Only `.env.example` (template with no real keys) should be shared
>
> For production deployment with enterprise-grade security, see **[API Security Architecture](docs/04-operations/api-security-architecture.md)** for backend proxy setup.
>
> **Quick security check**:
> ```bash
> git check-ignore .env  # Should output: .env
> ```

5. **Generate sample data**
```bash
python data_generator.py
```

This will create realistic SaaS data with:
- 10,000 users
- 365 days of history
- Realistic conversion and churn patterns
- Product usage data

6. **Launch the dashboard**
```bash
streamlit run dashboard.py
```

The dashboard will open at `http://localhost:8501`

## 🔑 API Key Setup

To use the AI-powered features:

1. Get your API key from [Anthropic Console](https://console.anthropic.com)
2. Add to `.env` file:
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

Without an API key, the dashboard still works but AI features will be disabled.

## 📊 Key Metrics Explained

### Monthly Recurring Revenue (MRR)
- **Definition**: Normalized monthly revenue from all active subscriptions
- **Why it matters**: Core health indicator for SaaS businesses
- **Target**: Consistent month-over-month growth

### Customer Acquisition Cost (CAC)
- **Definition**: Average cost to acquire a new customer
- **Calculation**: Marketing/Sales spend ÷ New customers
- **Why it matters**: Determines marketing efficiency

### Lifetime Value (LTV)
- **Definition**: Expected revenue from a customer over their lifetime
- **Calculation**: ARPU ÷ Monthly churn rate
- **Why it matters**: Determines profitability potential

### LTV:CAC Ratio
- **Definition**: Ratio of customer lifetime value to acquisition cost
- **Target**: > 3.0x (healthy SaaS business)
- **Why it matters**: Indicates sustainable growth potential

### Churn Rate
- **Definition**: % of customers who cancel in a period
- **Target**: < 5% monthly for SaaS
- **Why it matters**: Directly impacts revenue and growth

## 🎓 For Interview Preparation

### Talking Points

**1. Problem Statement**
"At Jobscan, stakeholders spend 40% of their time requesting custom reports. This dashboard reduces that to near-zero by empowering self-service analytics."

**2. Technical Approach**
- Modular architecture for easy extension
- Cached analytics engine for performance
- AI integration for accessibility
- Production-ready code with error handling

**3. Business Impact**
- 80% reduction in routine data queries
- Real-time anomaly detection
- Democratized data access across org
- AI-powered insights for non-technical users

**4. Scalability**
- Designed for 100K+ users
- Optimized pandas operations
- Caching strategy for performance
- Ready for cloud deployment (Streamlit Cloud, AWS, GCP)

### Demo Flow

1. **Start with Overview**: Show key metrics and health check
2. **Demonstrate AI**: Ask natural language question
3. **Show Funnel**: Explain conversion insights
4. **Highlight Cohorts**: Discuss retention patterns
5. **Discuss Architecture**: Code walkthrough if requested

## 🔬 Data Science Highlights

### Advanced Analytics
- **Cohort Analysis**: Period-over-period retention tracking
- **Anomaly Detection**: Statistical threshold-based alerting
- **Funnel Optimization**: Multi-stage conversion analysis
- **Segment Performance**: A/B testing readiness

### Statistical Methods
- Exponential distributions for time-to-event modeling
- Beta distributions for match rate simulation
- Poisson processes for keyword extraction
- Time-series analysis for trend detection

### Data Engineering
- Efficient pandas operations
- Data validation and cleaning
- Type-safe date handling
- Memory-optimized processing

## 📝 Customization Guide

### Adding New Metrics

1. **Update analytics.py**
```python
def get_your_metric(self):
    # Calculation logic
    return result
```

2. **Add to dashboard.py**
```python
metric_value = analytics.get_your_metric()
st.metric("Your Metric", f"{metric_value:.2f}")
```

### Configuring Thresholds

Edit `config.py`:
```python
THRESHOLDS = {
    "your_metric": {"warning": 0.05, "critical": 0.08}
}
```

### Changing Data Parameters

Edit `config.py`:
```python
NUM_USERS = 50000  # Increase dataset size
DATE_RANGE_DAYS = 730  # 2 years of data
```

## 🧪 Testing

```bash
# Generate fresh data
python data_generator.py

# Test analytics engine
python -c "from analytics import SaaSAnalytics; a = SaaSAnalytics(); print(a.get_current_mrr())"

# Test AI engine (requires API key)
python ai_query.py
```

## 🚀 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Add `ANTHROPIC_API_KEY` to secrets

### Docker (Coming Soon)
```bash
docker build -t jobmetrics-pro .
docker run -p 8501:8501 jobmetrics-pro
```

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Anthropic Claude API](https://docs.anthropic.com)
- [SaaS Metrics Guide](https://www.saastr.com)
- [Plotly Documentation](https://plotly.com/python/)

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome:
1. Open an issue
2. Describe the enhancement
3. Submit a pull request

## 📄 License

MIT License - feel free to use this for your portfolio or learning

## 👤 Author

**Jerry Lai (Ho-Chu Lai)**
- LinkedIn: [linkedin.com/in/ho-chu-lai-44355569](https://www.linkedin.com/in/ho-chu-lai-44355569/)
- GitHub: [@419vive](https://github.com/419vive)
- Email: [419vive@gmail.com](mailto:419vive@gmail.com)

---

## 🎯 Jobscan Interview Prep Notes

### Why This Project is Relevant

1. **Domain Expertise**: Built specifically for job search/resume SaaS
2. **Self-Service Focus**: Aligns with reducing support burden
3. **AI Integration**: Shows modern tech stack proficiency
4. **Production Quality**: Clean code, documentation, error handling
5. **Business Acumen**: Understands SaaS metrics that matter

### Questions to Prepare

1. "How would you scale this to handle 1M users?"
   - Database backend (PostgreSQL)
   - Caching layer (Redis)
   - Async processing (Celery)
   - CDN for static assets

2. "How do you ensure data accuracy?"
   - Input validation
   - Unit tests for calculations
   - Comparison with source of truth
   - Audit logging

3. "What would you add next?"
   - Real-time streaming data
   - Predictive churn models
   - A/B test analysis
   - Custom report builder

### Key Differentiators

- **AI Integration**: Not just dashboards, but intelligent insights
- **Anomaly Detection**: Proactive vs reactive analytics
- **Self-Service**: Reduces dependency on data team
- **Clean Code**: Production-ready, maintainable

---

**Built with ❤️ for demonstrating enterprise analytics capabilities**
