# 📑 JobMetrics Pro - Project Index

**Your complete navigation guide to the project**

---

## 🚀 Quick Start

**First time here?** Start with these files in order:

1. **[docs/guides/START_HERE.md](docs/guides/START_HERE.md)** - Quick setup (5 min)
2. **[docs/guides/LAUNCH.md](docs/guides/LAUNCH.md)** - Launch dashboard & demo script
3. **[docs/README.md](docs/README.md)** - Full project documentation

**Launch the Dashboard:**
```bash
streamlit run src/dashboard/dashboard.py
# Or use: ./scripts/run.sh
```

---

## 📂 Project Navigation

### 🎯 Core Application

| File | Purpose | When to Use |
|------|---------|-------------|
| [src/dashboard/dashboard.py](src/dashboard/dashboard.py) | Main Streamlit app | Launch the dashboard |
| [src/core/analytics.py](src/core/analytics.py) | SaaS metrics engine | Understand calculations |
| [src/core/ai_query.py](src/core/ai_query.py) | AI query interface | See AI integration |
| [src/core/config.py](src/core/config.py) | Configuration | Change settings |

### 📊 Data & Scripts

| File | Purpose | When to Use |
|------|---------|-------------|
| [scripts/data_generator.py](scripts/data_generator.py) | Generate sample data | Create/refresh datasets |
| [scripts/run.sh](scripts/run.sh) | Quick launch script | Fast startup |
| [data/](data/) | Generated datasets | View raw data (CSV files) |

### 📚 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| [docs/README.md](docs/README.md) | Complete guide | Everyone |
| [docs/guides/START_HERE.md](docs/guides/START_HERE.md) | Quick start | New users |
| [docs/guides/LAUNCH.md](docs/guides/LAUNCH.md) | Demo guide | Interview prep |
| [docs/technical/PROJECT_SUMMARY.md](docs/technical/PROJECT_SUMMARY.md) | Technical deep dive | Technical interviews |
| [docs/technical/API_REFERENCE.md](docs/technical/API_REFERENCE.md) | API documentation | Developers |
| [docs/technical/DIRECTORY_STRUCTURE.md](docs/technical/DIRECTORY_STRUCTURE.md) | File organization | Project understanding |

### 🧪 Testing

| File | Purpose | When to Use |
|------|---------|-------------|
| [tests/README.md](tests/README.md) | Testing guide | Set up tests |
| [tests/unit/test_analytics.py](tests/unit/test_analytics.py) | Unit tests | Run/write tests |

### ⚙️ Configuration

| File | Purpose | When to Use |
|------|---------|-------------|
| [requirements.txt](requirements.txt) | Python dependencies | Installation |
| [.env.example](.env.example) | Environment template | Setup API keys |
| [.gitignore](.gitignore) | Git exclusions | Version control |

---

## 🗺️ User Journey Guides

### For Interview Preparation

1. **[docs/guides/LAUNCH.md](docs/guides/LAUNCH.md)** - 5-minute demo script
2. **[docs/technical/PROJECT_SUMMARY.md](docs/technical/PROJECT_SUMMARY.md)** - Talking points
3. **[docs/technical/API_REFERENCE.md](docs/technical/API_REFERENCE.md)** - Technical Q&A prep
4. Launch dashboard: `streamlit run src/dashboard/dashboard.py`

### For Understanding the Code

1. **[docs/technical/DIRECTORY_STRUCTURE.md](docs/technical/DIRECTORY_STRUCTURE.md)** - Project layout
2. **[src/core/config.py](src/core/config.py)** - Configuration
3. **[src/core/analytics.py](src/core/analytics.py)** - Core logic
4. **[docs/technical/API_REFERENCE.md](docs/technical/API_REFERENCE.md)** - API details

### For Customization

1. **[src/core/config.py](src/core/config.py)** - Change thresholds, settings
2. **[scripts/data_generator.py](scripts/data_generator.py)** - Modify data generation
3. **[src/dashboard/dashboard.py](src/dashboard/dashboard.py)** - Customize UI
4. **[docs/README.md](docs/README.md)** - See customization guide

---

## 📋 Common Tasks

### Launch Dashboard
```bash
cd "/path/to/self-help databboard"
streamlit run src/dashboard/dashboard.py
```

### Generate Fresh Data
```bash
python scripts/data_generator.py
```

### Run Tests
```bash
pip install pytest pytest-cov
pytest tests/ -v
```

### View API Documentation
Open: [docs/technical/API_REFERENCE.md](docs/technical/API_REFERENCE.md)

### Setup Environment
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

---

## 🎓 Learning Paths

### Path 1: Quick Demo (15 minutes)
1. Read [docs/guides/LAUNCH.md](docs/guides/LAUNCH.md)
2. Launch dashboard
3. Click through all 4 tabs
4. Practice 5-minute demo

### Path 2: Code Understanding (1 hour)
1. Read [docs/technical/DIRECTORY_STRUCTURE.md](docs/technical/DIRECTORY_STRUCTURE.md)
2. Review [src/core/analytics.py](src/core/analytics.py)
3. Check [docs/technical/API_REFERENCE.md](docs/technical/API_REFERENCE.md)
4. Explore [src/dashboard/dashboard.py](src/dashboard/dashboard.py)

### Path 3: Customization (2 hours)
1. Modify [src/core/config.py](src/core/config.py) thresholds
2. Regenerate data with new parameters
3. Add custom metric to [src/core/analytics.py](src/core/analytics.py)
4. Display in [src/dashboard/dashboard.py](src/dashboard/dashboard.py)

### Path 4: Full Mastery (1 day)
1. Read all documentation
2. Review all source code
3. Run and understand tests
4. Add custom feature end-to-end

---

## 🔍 Find Something Specific

### SaaS Metrics
- **MRR, ARPU, LTV, CAC**: [src/core/analytics.py](src/core/analytics.py:15-85)
- **Churn Rate**: [src/core/analytics.py](src/core/analytics.py:87-105)
- **Conversion Funnel**: [src/core/analytics.py](src/core/analytics.py:140-160)

### AI Features
- **Natural Language Queries**: [src/core/ai_query.py](src/core/ai_query.py:32-80)
- **Auto Insights**: [src/core/ai_query.py](src/core/ai_query.py:82-130)
- **Metric Explanations**: [src/core/ai_query.py](src/core/ai_query.py:132-160)

### Dashboard Components
- **Overview Tab**: [src/dashboard/dashboard.py](src/dashboard/dashboard.py:80-150)
- **Funnel Tab**: [src/dashboard/dashboard.py](src/dashboard/dashboard.py:152-220)
- **Cohort Tab**: [src/dashboard/dashboard.py](src/dashboard/dashboard.py:222-280)
- **AI Tab**: [src/dashboard/dashboard.py](src/dashboard/dashboard.py:282-360)

### Data Generation
- **User Generation**: [scripts/data_generator.py](scripts/data_generator.py:25-65)
- **Subscriptions**: [scripts/data_generator.py](scripts/data_generator.py:67-125)
- **Resume Scans**: [scripts/data_generator.py](scripts/data_generator.py:127-180)

---

## 📱 Contact & Support

### For This Project
- **Author**: Jerry Lai
- **Purpose**: Portfolio project for Jobscan interview
- **Created**: 2025-10-26

### Resources
- **Streamlit Docs**: https://docs.streamlit.io
- **Anthropic Claude**: https://docs.anthropic.com
- **Pandas Docs**: https://pandas.pydata.org

---

## ✅ Project Status

**Version**: 1.0.0
**Status**: Production Ready
**Last Updated**: 2025-10-26

### Completed Features
- ✅ Core SaaS metrics (MRR, CAC, LTV, Churn, ARPU)
- ✅ Product analytics (match rates, scan volumes)
- ✅ AI-powered natural language queries
- ✅ Automated anomaly detection
- ✅ Interactive dashboards (4 tabs)
- ✅ Cohort retention analysis
- ✅ Conversion funnel visualization
- ✅ Comprehensive documentation
- ✅ Professional project structure
- ✅ Test framework setup

### Future Enhancements
- ⏳ Complete test coverage
- ⏳ Database backend integration
- ⏳ User authentication
- ⏳ Custom report builder
- ⏳ Email alerts
- ⏳ Mobile responsive design

---

## 🎯 Quick Reference

### Essential Commands
```bash
# Launch dashboard
streamlit run src/dashboard/dashboard.py

# Generate data
python scripts/data_generator.py

# Run tests
pytest tests/ -v

# Quick launch
./scripts/run.sh
```

### Essential Files
- **Main App**: `src/dashboard/dashboard.py`
- **Core Logic**: `src/core/analytics.py`
- **Config**: `src/core/config.py`
- **Data Gen**: `scripts/data_generator.py`

### Essential Docs
- **Getting Started**: `docs/guides/START_HERE.md`
- **Full Docs**: `docs/README.md`
- **API Reference**: `docs/technical/API_REFERENCE.md`

---

**This index is your map to the entire project. Bookmark it! 📌**
