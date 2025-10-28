# 🧭 JobMetrics Pro - Quick Navigation Guide

## 🎯 What Do You Want to Do?

Choose your path below for instant guidance!

---

## 🚀 **I Want to Launch the Dashboard**

```bash
streamlit run src/dashboard/dashboard.py
```

Or use quick script:
```bash
./scripts/run.sh
```

Dashboard opens at: **http://localhost:8501**

📖 **More details**: [docs/guides/LAUNCH.md](docs/guides/LAUNCH.md)

---

## 📚 **I Want to Learn About the Project**

**Start Here**: [INDEX.md](INDEX.md) - Complete project navigation

**Then Read**:
1. [docs/guides/START_HERE.md](docs/guides/START_HERE.md) - Quick start (5 min)
2. [docs/README.md](docs/README.md) - Full documentation (30 min)
3. [docs/technical/PROJECT_SUMMARY.md](docs/technical/PROJECT_SUMMARY.md) - Technical deep dive (1 hour)

---

## 💻 **I Want to Understand the Code**

**Architecture**: [STRUCTURE.md](STRUCTURE.md) - Visual project tree

**Core Modules**:
- SaaS Analytics: [src/core/analytics.py](src/core/analytics.py)
- AI Engine: [src/core/ai_query.py](src/core/ai_query.py)
- Dashboard UI: [src/dashboard/dashboard.py](src/dashboard/dashboard.py)

**API Documentation**: [docs/technical/API_REFERENCE.md](docs/technical/API_REFERENCE.md)

---

## 🎤 **I Want to Prepare for the Interview**

**Demo Script**: [docs/guides/LAUNCH.md](docs/guides/LAUNCH.md)

**Key Documents**:
1. 5-minute demo flow
2. Talking points & business impact
3. Technical Q&A preparation
4. Code walkthrough strategy

**Practice**:
1. Launch dashboard: `streamlit run src/dashboard/dashboard.py`
2. Click through all 4 tabs
3. Practice explaining each feature
4. Review [docs/technical/PROJECT_SUMMARY.md](docs/technical/PROJECT_SUMMARY.md)

---

## 🔧 **I Want to Customize the Project**

**Change Settings**: [src/core/config.py](src/core/config.py)
- Thresholds for anomaly detection
- Number of users to generate
- Date ranges

**Add New Metrics**: [src/core/analytics.py](src/core/analytics.py)
- Add calculation method
- Update dashboard to display

**Modify UI**: [src/dashboard/dashboard.py](src/dashboard/dashboard.py)
- Change layouts
- Add new visualizations
- Customize colors/themes

**Regenerate Data**:
```bash
python scripts/data_generator.py
```

---

## 📊 **I Want to See the Data**

**Generated Datasets**: [data/](data/)
- `users.csv` - 10,000 user records
- `subscriptions.csv` - 2,498 subscriptions
- `scans.csv` - 83,277 resume scans
- `revenue.csv` - 365 days of MRR

**Create Fresh Data**:
```bash
python scripts/data_generator.py
```

---

## 🧪 **I Want to Run Tests**

**Install Testing Tools**:
```bash
pip install pytest pytest-cov
```

**Run Tests**:
```bash
pytest tests/ -v                    # All tests
pytest tests/unit/ -v               # Unit tests only
pytest tests/ --cov=src             # With coverage
```

**Testing Guide**: [tests/README.md](tests/README.md)

---

## 🤖 **I Want to Use AI Features**

**Setup**:
1. Get API key from https://console.anthropic.com
2. Create `.env` file: `cp .env.example .env`
3. Add key: `ANTHROPIC_API_KEY=sk-ant-xxxxx`
4. Restart dashboard

**Try AI Assistant**:
- Go to "AI Assistant" tab in dashboard
- Ask: "What's our churn rate?"
- Click "Generate Fresh Insights"

**Note**: Dashboard works without AI - it's optional!

---

## 📁 **I Want to Understand the File Structure**

**Quick View**: [STRUCTURE.md](STRUCTURE.md) - Visual tree

**Detailed Guide**: [docs/technical/DIRECTORY_STRUCTURE.md](docs/technical/DIRECTORY_STRUCTURE.md)

**Key Locations**:
```
src/core/         - Business logic
src/dashboard/    - UI components
scripts/          - Automation
docs/            - Documentation
tests/           - Test suites
data/            - Generated datasets
```

---

## 🔍 **I Want to Find Specific Information**

### SaaS Metrics
**File**: [src/core/analytics.py](src/core/analytics.py)
- MRR calculation: Line 23
- Churn rate: Line 41
- LTV:CAC ratio: Line 87

### AI Features
**File**: [src/core/ai_query.py](src/core/ai_query.py)
- Natural language queries: Line 40
- Auto insights: Line 101
- Metric explanations: Line 158

### Dashboard Tabs
**File**: [src/dashboard/dashboard.py](src/dashboard/dashboard.py)
- Overview tab: Line 80
- Funnel tab: Line 170
- Cohort tab: Line 250
- AI tab: Line 300

### Data Generation
**File**: [scripts/data_generator.py](scripts/data_generator.py)
- User generation: Line 25
- Subscriptions: Line 45
- Scans: Line 95

---

## 🆘 **I Need Help**

### Dashboard Won't Launch
```bash
# Check if data exists
ls data/

# If empty, generate data
python scripts/data_generator.py

# Then try again
streamlit run src/dashboard/dashboard.py
```

### AI Features Not Working
- Add `ANTHROPIC_API_KEY` to `.env` file
- Dashboard works without AI

### Import Errors
```bash
# Make sure you're in project root
cd "/Users/jerrylaivivemachi/DS PROJECT/self-help databboard"

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Use different port
streamlit run src/dashboard/dashboard.py --server.port 8502
```

---

## 📍 **Where Am I?**

**Current Directory**: `/Users/jerrylaivivemachi/DS PROJECT/self-help databboard`

**Important Files in Root**:
- `INDEX.md` - Project navigation index
- `STRUCTURE.md` - Visual file tree
- `NAVIGATION.md` - This file!
- `requirements.txt` - Dependencies
- `.env.example` - Environment template

**Organized Directories**:
- `src/` - All source code
- `docs/` - All documentation
- `scripts/` - Automation scripts
- `tests/` - Test suites
- `data/` - Generated datasets

---

## ⚡ **Quick Commands**

```bash
# Launch dashboard
streamlit run src/dashboard/dashboard.py

# Generate data
python scripts/data_generator.py

# Run tests
pytest tests/ -v

# View structure
cat STRUCTURE.md

# View this guide
cat NAVIGATION.md
```

---

## 🎯 **Recommended Learning Path**

### Beginner (1 hour)
1. Read [INDEX.md](INDEX.md) - 5 min
2. Read [docs/guides/START_HERE.md](docs/guides/START_HERE.md) - 10 min
3. Launch dashboard - 5 min
4. Explore all 4 tabs - 20 min
5. Read [STRUCTURE.md](STRUCTURE.md) - 10 min
6. Review [docs/guides/LAUNCH.md](docs/guides/LAUNCH.md) - 10 min

### Intermediate (4 hours)
1. Complete Beginner path
2. Read [docs/README.md](docs/README.md) - 30 min
3. Study [src/core/analytics.py](src/core/analytics.py) - 1 hour
4. Study [src/dashboard/dashboard.py](src/dashboard/dashboard.py) - 1 hour
5. Read [docs/technical/API_REFERENCE.md](docs/technical/API_REFERENCE.md) - 30 min
6. Practice demo presentation - 1 hour

### Advanced (1 day)
1. Complete Intermediate path
2. Read all documentation
3. Review all source code
4. Run and understand tests
5. Add custom metric
6. Modify dashboard
7. Master interview talking points

---

## 🌟 **Best Practices**

1. **Always start from project root** for consistent paths
2. **Use organized files** in `src/`, not legacy root files
3. **Read INDEX.md first** when navigating
4. **Check STRUCTURE.md** to understand layout
5. **Follow API_REFERENCE.md** for code examples

---

**Need to navigate?** Choose your goal above and follow the path! 🎯

**Lost?** Start with [INDEX.md](INDEX.md) ← Your complete map!
