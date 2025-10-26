# 📖 API Reference - JobMetrics Pro

## Overview

This document provides detailed API documentation for all core modules in JobMetrics Pro.

---

## Table of Contents

1. [SaaSAnalytics](#saasanalytics) - Core metrics calculation engine
2. [AIQueryEngine](#aiqueryengine) - AI-powered query interface
3. [Configuration](#configuration) - Project configuration

---

## SaaSAnalytics

**Module**: `src/core/analytics.py`
**Class**: `SaaSAnalytics`

### Description
Core analytics engine that calculates all SaaS metrics from raw data files.

### Initialization

```python
from src.core import SaaSAnalytics

analytics = SaaSAnalytics()
```

**What it does**:
- Loads all CSV files from `data/` directory
- Parses dates automatically
- Caches DataFrames for performance

---

### Revenue Metrics

#### `get_current_mrr()`
Get current Monthly Recurring Revenue.

**Returns**: `float` - Current MRR in dollars

**Example**:
```python
mrr = analytics.get_current_mrr()
# Returns: 92148.74
```

---

#### `get_mrr_growth_rate(days=30)`
Calculate MRR growth rate over specified period.

**Parameters**:
- `days` (int, optional): Number of days to look back. Default: 30

**Returns**: `float` - Growth rate as percentage

**Example**:
```python
growth = analytics.get_mrr_growth_rate(30)
# Returns: 5.23  (meaning 5.23% growth)
```

---

#### `get_arpu()`
Calculate Average Revenue Per User.

**Returns**: `float` - Average MRR per active subscriber

**Example**:
```python
arpu = analytics.get_arpu()
# Returns: 45.39
```

---

#### `get_mrr_trend(days=90)`
Get MRR trend data for visualization.

**Parameters**:
- `days` (int, optional): Number of days of history. Default: 90

**Returns**: `pandas.DataFrame` with columns:
- `date`: Date
- `mrr`: Monthly recurring revenue
- `active_subscriptions`: Number of active subs

**Example**:
```python
trend = analytics.get_mrr_trend(90)
# Returns DataFrame with 90 rows of daily MRR data
```

---

### Customer Metrics

#### `get_cac()`
Calculate average Customer Acquisition Cost.

**Returns**: `float` - Average CAC in dollars

**Example**:
```python
cac = analytics.get_cac()
# Returns: 23.45
```

---

#### `get_ltv()`
Calculate Customer Lifetime Value.

**Formula**: ARPU / Monthly Churn Rate
**Note**: Capped at 36 months to avoid infinity

**Returns**: `float` - LTV in dollars

**Example**:
```python
ltv = analytics.get_ltv()
# Returns: 1567.89
```

---

#### `get_ltv_cac_ratio()`
Calculate LTV:CAC ratio (key SaaS health indicator).

**Target**: > 3.0x for healthy SaaS

**Returns**: `float` - Ratio value

**Example**:
```python
ratio = analytics.get_ltv_cac_ratio()
# Returns: 66.89
```

---

### Retention Metrics

#### `get_churn_rate(period_days=30)`
Calculate churn rate for specified period.

**Parameters**:
- `period_days` (int, optional): Period in days. Default: 30

**Returns**: `float` - Churn rate as percentage

**Example**:
```python
churn = analytics.get_churn_rate(30)
# Returns: 0.38  (meaning 0.38% monthly churn)
```

---

#### `get_cohort_analysis()`
Generate cohort retention analysis.

**Returns**: `pandas.DataFrame` - Retention matrix
- **Index**: Signup cohort (by month)
- **Columns**: Months since signup (0, 1, 2, ...)
- **Values**: Retention percentage

**Example**:
```python
cohorts = analytics.get_cohort_analysis()
# Returns retention heatmap data
```

---

### Conversion Metrics

#### `get_conversion_rate()`
Calculate free to paid conversion rate.

**Returns**: `float` - Conversion rate as percentage

**Example**:
```python
conversion = analytics.get_conversion_rate()
# Returns: 24.98  (meaning 24.98% of users convert)
```

---

#### `get_conversion_funnel()`
Get conversion funnel data.

**Returns**: `pandas.DataFrame` with stages:
1. Total Signups
2. Performed 1+ Scan
3. Performed 2+ Scans
4. Converted to Paid

**Example**:
```python
funnel = analytics.get_conversion_funnel()
```

---

### User Engagement Metrics

#### `get_active_users(period='daily')`
Get active users (users who performed scans).

**Parameters**:
- `period` (str): One of 'daily', 'weekly', 'monthly'

**Returns**: `int` - Count of active users

**Example**:
```python
dau = analytics.get_active_users('daily')   # DAU
wau = analytics.get_active_users('weekly')  # WAU
mau = analytics.get_active_users('monthly') # MAU
```

---

### Product Metrics

#### `get_avg_match_rate()`
Calculate average resume match rate.

**Returns**: `float` - Average match rate as percentage

**Example**:
```python
match_rate = analytics.get_avg_match_rate()
# Returns: 72.34
```

---

#### `get_avg_scans_per_user()`
Calculate average number of scans per user.

**Returns**: `float` - Average scans

**Example**:
```python
avg_scans = analytics.get_avg_scans_per_user()
# Returns: 8.33
```

---

### Segmentation Analysis

#### `get_user_segment_performance()`
Analyze performance by user segment.

**Returns**: `pandas.DataFrame` with columns:
- `segment`: User segment name
- `total_users`: Count of users
- `conversions`: Count of paid conversions
- `conversion_rate`: Conversion rate (%)

**Example**:
```python
segments = analytics.get_user_segment_performance()
```

---

#### `get_channel_performance()`
Analyze performance by acquisition channel.

**Returns**: `pandas.DataFrame` with columns:
- `channel`: Acquisition channel
- `total_users`: Count of users
- `avg_cac`: Average CAC
- `conversions`: Count of conversions
- `conversion_rate`: Conversion rate (%)

**Example**:
```python
channels = analytics.get_channel_performance()
```

---

#### `get_revenue_by_plan()`
Calculate revenue breakdown by plan type.

**Returns**: `pandas.DataFrame` with columns:
- `plan_type`: Plan name (basic, professional, premium)
- `mrr`: Total MRR from this plan
- `subscribers`: Count of subscribers

**Example**:
```python
plans = analytics.get_revenue_by_plan()
```

---

### Anomaly Detection

#### `detect_anomalies()`
Detect anomalies in key metrics based on thresholds.

**Returns**: `list` of dictionaries with:
- `metric`: Metric name
- `value`: Current value
- `severity`: 'warning' or 'critical'
- `message`: Description

**Thresholds** (from `config.py`):
- Churn Rate: warning > 5%, critical > 8%
- Conversion Rate: warning < 2%, critical < 1%
- Match Rate: warning < 65%, critical < 60%
- MRR Growth: warning < -5%, critical < -10%

**Example**:
```python
anomalies = analytics.detect_anomalies()
# Returns: [
#     {
#         'metric': 'Churn Rate',
#         'value': '8.5%',
#         'severity': 'critical',
#         'message': 'Churn rate (8.5%) exceeds critical threshold'
#     }
# ]
```

---

## AIQueryEngine

**Module**: `src/core/ai_query.py`
**Class**: `AIQueryEngine`

### Description
AI-powered natural language query interface using Claude API.

### Initialization

```python
from src.core import AIQueryEngine

ai_engine = AIQueryEngine()
# Raises ValueError if ANTHROPIC_API_KEY not found
```

**Requirements**:
- `ANTHROPIC_API_KEY` in environment variables
- Active Anthropic API account

---

### Methods

#### `query(user_question)`
Process natural language query and return insights.

**Parameters**:
- `user_question` (str): Question in plain English

**Returns**: `dict` with:
- `success` (bool): Whether query succeeded
- `answer` (str): AI-generated answer
- `metrics_used` (dict): Relevant metrics referenced
- `anomalies` (list): Related anomalies
- `error` (str, optional): Error message if failed

**Example**:
```python
result = ai_engine.query("What's our current churn rate and should I be worried?")

if result['success']:
    print(result['answer'])
    # "Your current churn rate is 0.38%, which is excellent..."
```

---

#### `get_insights()`
Generate automatic insights about the business.

**Returns**: `dict` with:
- `success` (bool): Whether generation succeeded
- `insights` (list): List of insight objects
- `error` (str, optional): Error message if failed

**Insight Object Structure**:
```python
{
    'title': 'Strong Product-Market Fit',
    'insight': 'Conversion rate of 24.98% is well above industry average...',
    'impact': 'This indicates strong value proposition...',
    'actions': [
        'Focus on scaling acquisition channels',
        'Document what drives high conversion'
    ]
}
```

**Example**:
```python
result = ai_engine.get_insights()

if result['success']:
    for insight in result['insights']:
        print(f"{insight['title']}: {insight['insight']}")
```

---

#### `explain_metric(metric_name)`
Explain what a specific metric means.

**Parameters**:
- `metric_name` (str): Name of metric to explain

**Returns**: `dict` with:
- `success` (bool): Whether explanation succeeded
- `explanation` (str): Detailed explanation
- `error` (str, optional): Error message if failed

**Example**:
```python
result = ai_engine.explain_metric('ltv_cac_ratio')

if result['success']:
    print(result['explanation'])
```

---

## Configuration

**Module**: `src/core/config.py`

### Environment Variables

**ANTHROPIC_API_KEY**
- **Type**: String
- **Required**: For AI features only
- **Example**: `sk-ant-xxxxx...`

**FLASK_ENV**
- **Type**: String
- **Default**: `development`
- **Options**: `development`, `production`

**FLASK_PORT**
- **Type**: Integer
- **Default**: `5001`

**STREAMLIT_SERVER_PORT**
- **Type**: Integer
- **Default**: `8501`

---

### Data Configuration

**NUM_USERS**
- **Type**: Integer
- **Default**: `10000`
- **Purpose**: Number of users to generate

**DATE_RANGE_DAYS**
- **Type**: Integer
- **Default**: `365`
- **Purpose**: Days of historical data

**START_DATE**
- **Type**: String (YYYY-MM-DD)
- **Default**: `2024-01-01`
- **Purpose**: Start date for data generation

---

### Thresholds

**THRESHOLDS**
- **Type**: Dictionary
- **Purpose**: Anomaly detection thresholds

```python
THRESHOLDS = {
    "churn_rate": {"warning": 0.05, "critical": 0.08},
    "conversion_rate": {"warning": 0.02, "critical": 0.01},
    "avg_match_rate": {"warning": 0.65, "critical": 0.60},
    "mrr_growth": {"warning": -0.05, "critical": -0.10},
}
```

---

### Path Configuration

**BASE_DIR**
- **Type**: `pathlib.Path`
- **Value**: Project root directory

**DATA_DIR**
- **Type**: `pathlib.Path`
- **Value**: `{BASE_DIR}/data/`
- **Auto-created**: Yes

---

## Usage Examples

### Complete Workflow

```python
from src.core import SaaSAnalytics, AIQueryEngine

# Initialize analytics
analytics = SaaSAnalytics()

# Get key metrics
print(f"MRR: ${analytics.get_current_mrr():,.2f}")
print(f"Churn: {analytics.get_churn_rate(30):.2f}%")
print(f"LTV:CAC: {analytics.get_ltv_cac_ratio():.2f}x")

# Check for anomalies
anomalies = analytics.detect_anomalies()
if anomalies:
    for anomaly in anomalies:
        print(f"⚠️ {anomaly['message']}")

# Use AI for insights (requires API key)
try:
    ai = AIQueryEngine()
    result = ai.query("What should I focus on to reduce churn?")
    print(result['answer'])
except ValueError:
    print("AI features require ANTHROPIC_API_KEY")
```

---

## Error Handling

### Common Errors

**FileNotFoundError**
```python
# Occurs when data files don't exist
# Solution: Run scripts/data_generator.py
```

**ValueError (AI)**
```python
# Occurs when ANTHROPIC_API_KEY missing
# Solution: Add key to .env file
```

**KeyError (Analytics)**
```python
# Occurs when expected data columns missing
# Solution: Regenerate data with updated generator
```

---

## Performance Notes

### Caching
- `SaaSAnalytics` is decorated with `@st.cache_resource` in dashboard
- Data loads only once per session
- Recalculation only when data changes

### Optimization Tips
- Use `get_mrr_trend(days=30)` instead of full history for faster rendering
- Cache `SaaSAnalytics()` instance, don't recreate
- AI queries rate-limited by Anthropic (50 requests/min)

---

## Version History

**v1.0.0** - Initial release
- Core analytics engine
- AI query interface
- Complete metric coverage

---

**Last Updated**: 2025-10-26
**Maintained By**: Jerry Lai
