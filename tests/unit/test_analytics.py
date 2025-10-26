"""
Unit tests for SaaSAnalytics class

Run with: pytest tests/unit/test_analytics.py
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.analytics import SaaSAnalytics


class TestSaaSAnalytics:
    """Test suite for SaaSAnalytics class"""

    @pytest.fixture(scope="class")
    def analytics(self):
        """Create analytics instance for testing"""
        return SaaSAnalytics()

    def test_initialization(self, analytics):
        """Test that analytics initializes correctly"""
        assert analytics is not None
        assert hasattr(analytics, 'users')
        assert hasattr(analytics, 'subscriptions')
        assert hasattr(analytics, 'scans')
        assert hasattr(analytics, 'revenue')

    def test_get_current_mrr(self, analytics):
        """Test MRR calculation"""
        mrr = analytics.get_current_mrr()
        assert isinstance(mrr, float)
        assert mrr > 0, "MRR should be positive"

    def test_get_arpu(self, analytics):
        """Test ARPU calculation"""
        arpu = analytics.get_arpu()
        assert isinstance(arpu, float)
        assert arpu > 0, "ARPU should be positive"

    def test_get_churn_rate(self, analytics):
        """Test churn rate calculation"""
        churn = analytics.get_churn_rate(30)
        assert isinstance(churn, float)
        assert 0 <= churn <= 100, "Churn rate should be between 0-100%"

    def test_get_conversion_rate(self, analytics):
        """Test conversion rate calculation"""
        conversion = analytics.get_conversion_rate()
        assert isinstance(conversion, float)
        assert 0 <= conversion <= 100, "Conversion rate should be between 0-100%"

    def test_get_ltv_cac_ratio(self, analytics):
        """Test LTV:CAC ratio calculation"""
        ratio = analytics.get_ltv_cac_ratio()
        assert isinstance(ratio, float)
        assert ratio > 0, "LTV:CAC ratio should be positive"

    def test_get_active_users(self, analytics):
        """Test active users calculation"""
        dau = analytics.get_active_users('daily')
        wau = analytics.get_active_users('weekly')
        mau = analytics.get_active_users('monthly')

        assert isinstance(dau, (int, np.int64))
        assert isinstance(wau, (int, np.int64))
        assert isinstance(mau, (int, np.int64))
        assert dau <= wau <= mau, "DAU <= WAU <= MAU"

    def test_detect_anomalies(self, analytics):
        """Test anomaly detection"""
        anomalies = analytics.detect_anomalies()
        assert isinstance(anomalies, list)

        for anomaly in anomalies:
            assert 'metric' in anomaly
            assert 'severity' in anomaly
            assert anomaly['severity'] in ['warning', 'critical']

    def test_get_conversion_funnel(self, analytics):
        """Test conversion funnel data"""
        funnel = analytics.get_conversion_funnel()
        assert len(funnel) == 4, "Should have 4 funnel stages"

        # Check funnel decreases at each stage
        values = funnel.iloc[:, 1].values
        for i in range(len(values) - 1):
            assert values[i] >= values[i+1], "Funnel should decrease"

    def test_get_cohort_analysis(self, analytics):
        """Test cohort analysis"""
        cohorts = analytics.get_cohort_analysis()
        assert cohorts is not None
        assert len(cohorts) > 0, "Should have cohort data"


# Note: To run these tests, you need pytest installed:
# pip install pytest pytest-cov
#
# Run with:
# pytest tests/unit/test_analytics.py -v
# pytest tests/unit/test_analytics.py --cov=src/core
