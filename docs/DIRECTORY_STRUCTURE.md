# 📁 JobMetrics Pro - Directory Structure

## Overview

This document describes the organization and purpose of each directory and file in the JobMetrics Pro project.

---

## 📂 Project Structure

```
jobmetrics-pro/
├── 📁 src/                          # Source code
│   ├── 📁 core/                     # Core business logic
│   │   ├── analytics.py             # SaaS metrics calculations
│   │   ├── ai_query.py              # AI-powered query engine
│   │   ├── config.py                # Configuration management
│   │   └── __init__.py              # Package initialization
│   │
│   ├── 📁 dashboard/                # Dashboard UI components
│   │   ├── dashboard.py             # Main Streamlit application
│   │   └── __init__.py              # Package initialization
│   │
│   └── 📁 utils/                    # Utility functions
│       └── __init__.py              # Package initialization
│
├── 📁 scripts/                      # Executable scripts
│   ├── data_generator.py            # Generate sample SaaS data
│   └── run.sh                       # Quick launch script
│
├── 📁 data/                         # Generated datasets
│   ├── users.csv                    # User registration data
│   ├── subscriptions.csv            # Subscription & revenue data
│   ├── scans.csv                    # Resume scan activity
│   └── revenue.csv                  # Daily MRR tracking
│
├── 📁 docs/                         # Documentation
│   ├── README.md                    # Main project documentation
│   │
│   ├── 📁 guides/                   # User guides
│   │   ├── START_HERE.md            # Quick start guide
│   │   └── LAUNCH.md                # Launch instructions
│   │
│   ├── 📁 technical/                # Technical documentation
│   │   ├── PROJECT_SUMMARY.md       # Technical overview
│   │   ├── DIRECTORY_STRUCTURE.md   # This file
│   │   └── API_REFERENCE.md         # API documentation
│   │
│   └── 📁 diagrams/                 # Architecture diagrams
│       └── (Future: system diagrams)
│
├── 📁 tests/                        # Test suites
│   ├── 📁 unit/                     # Unit tests
│   │   └── (Future: unit tests)
│   │
│   └── 📁 integration/              # Integration tests
│       └── (Future: integration tests)
│
├── 📁 notebooks/                    # Jupyter notebooks
│   └── (Future: exploratory analysis)
│
├── 📁 assets/                       # Static assets
│   └── (Future: images, logos, etc.)
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 .env.example                  # Environment variables template
├── 📄 .gitignore                    # Git ignore rules
└── 📄 INDEX.md                      # Project navigation index

```

---

## 📖 Directory Descriptions

### `/src/` - Source Code
**Purpose**: All production source code organized by responsibility

#### `/src/core/` - Core Business Logic
- **analytics.py**: SaaS metrics calculations (MRR, CAC, LTV, Churn, etc.)
- **ai_query.py**: AI-powered natural language query engine using Claude
- **config.py**: Centralized configuration and environment management
- **Purpose**: Business logic independent of presentation layer

#### `/src/dashboard/` - Dashboard UI
- **dashboard.py**: Main Streamlit application with all visualizations
- **Purpose**: User interface and visualization layer

#### `/src/utils/` - Utilities
- **Purpose**: Reusable helper functions (future: formatters, validators, etc.)

---

### `/scripts/` - Executable Scripts
**Purpose**: Standalone scripts for automation and utilities

- **data_generator.py**: Generates realistic SaaS data for development/demo
- **run.sh**: Quick launch script for the dashboard
- **Future**: deployment scripts, data migration tools, etc.

---

### `/data/` - Generated Datasets
**Purpose**: Storage for generated or imported data

**Files:**
- **users.csv** (710KB): 10,000 user records with demographics, channels, segments
- **subscriptions.csv** (175KB): 2,498 subscription records with plans, billing, churn
- **scans.csv** (7.5MB): 83,277 resume scan records with match rates, performance
- **revenue.csv** (18KB): 365 days of daily MRR and subscription metrics

**Note**: This directory is gitignored. Data is regenerated via `scripts/data_generator.py`

---

### `/docs/` - Documentation
**Purpose**: All project documentation organized by audience

#### `/docs/README.md` - Main Documentation
- Comprehensive project overview
- Feature descriptions
- Installation instructions
- Technical stack details

#### `/docs/guides/` - User Guides
- **START_HERE.md**: Quick start guide for new users
- **LAUNCH.md**: Dashboard launch instructions and demo script
- **Future**: deployment guide, customization guide

#### `/docs/technical/` - Technical Documentation
- **PROJECT_SUMMARY.md**: Technical deep dive and architecture
- **DIRECTORY_STRUCTURE.md**: This file - project organization
- **API_REFERENCE.md**: API documentation for core modules
- **Future**: data model documentation, algorithm explanations

#### `/docs/diagrams/` - Visual Documentation
- **Future**: System architecture diagrams, data flow diagrams, etc.

---

### `/tests/` - Test Suites
**Purpose**: Automated testing infrastructure

#### `/tests/unit/` - Unit Tests
- **Future**: Test individual functions and classes in isolation
- **Coverage goal**: 80%+ for core business logic

#### `/tests/integration/` - Integration Tests
- **Future**: Test component interactions and workflows
- **Focus**: Data pipelines, API integrations, dashboard rendering

---

### `/notebooks/` - Jupyter Notebooks
**Purpose**: Exploratory data analysis and prototyping

- **Future**: Data exploration, metric validation, A/B test analysis
- **Use case**: Ad-hoc analysis before productionizing features

---

### `/assets/` - Static Assets
**Purpose**: Images, logos, and other static resources

- **Future**: Dashboard logos, icons, screenshots for documentation
- **Organization**: `/assets/images/`, `/assets/icons/`, `/assets/screenshots/`

---

## 🔧 Configuration Files

### Root Level Configuration

**requirements.txt**
- Python package dependencies
- Pinned versions for reproducibility
- Groups: Core, Data Processing, Visualization, AI, Utilities

**.env.example**
- Template for environment variables
- API keys (ANTHROPIC_API_KEY)
- Configuration settings
- **Note**: Copy to `.env` and customize

**.gitignore**
- Specifies files/folders to exclude from Git
- Includes: venv, data files, .env, IDE configs, Python cache

---

## 📊 Data Flow

```
scripts/data_generator.py
        ↓
    data/*.csv
        ↓
src/core/analytics.py  →  src/core/ai_query.py
        ↓                           ↓
    src/dashboard/dashboard.py (Streamlit UI)
        ↓
    Browser (http://localhost:8501)
```

---

## 🚀 Common Operations

### Run Dashboard
```bash
# From project root
streamlit run src/dashboard/dashboard.py

# Or use script
./scripts/run.sh
```

### Regenerate Data
```bash
python scripts/data_generator.py
```

### Import Core Modules
```python
from src.core import SaaSAnalytics, AIQueryEngine
from src.core.config import DATA_DIR, THRESHOLDS

analytics = SaaSAnalytics()
mrr = analytics.get_current_mrr()
```

---

## 📐 Design Principles

### 1. Separation of Concerns
- **Core logic** (`src/core/`) independent of UI
- **Dashboard** (`src/dashboard/`) purely presentational
- **Scripts** (`scripts/`) for automation, not business logic

### 2. Modularity
- Each file has single responsibility
- Minimal coupling between modules
- Easy to test and maintain

### 3. Scalability
- Structure supports growth to 100+ files
- Clear places for new features
- Organized for team collaboration

### 4. Documentation
- Every major directory has purpose
- Code is self-documenting
- External docs for context and guides

---

## 🔄 Future Enhancements

### Planned Additions

**`/src/api/`** - REST API (if needed)
- Flask/FastAPI endpoints
- Authentication/authorization
- Rate limiting

**`/src/models/`** - Data models
- Pydantic schemas
- SQLAlchemy models (if adding database)
- Data validation classes

**`/config/`** - Environment-specific configs
- `development.py`
- `production.py`
- `testing.py`

**`/migrations/`** - Database migrations
- Alembic migration scripts (if adding database)

**`/deploy/`** - Deployment configurations
- Docker files
- Kubernetes manifests
- CI/CD pipelines

---

## 📚 Additional Resources

- **Main README**: `/docs/README.md`
- **Quick Start**: `/docs/guides/START_HERE.md`
- **Technical Details**: `/docs/technical/PROJECT_SUMMARY.md`
- **API Reference**: `/docs/technical/API_REFERENCE.md`
- **Project Index**: `/INDEX.md`

---

**Last Updated**: 2025-10-26
**Maintained By**: Jerry Lai
**Version**: 1.0.0
