"""
Analytics module for calculating SaaS metrics
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats
from . import config


class SaaSAnalytics:
    """Calculate key SaaS metrics and insights"""

    def __init__(self):
        self.users = pd.read_csv(config.DATA_DIR / 'users.csv', parse_dates=['signup_date'])
        self.subscriptions = pd.read_csv(
            config.DATA_DIR / 'subscriptions.csv',
            parse_dates=['subscription_start', 'subscription_end']
        )
        self.scans = pd.read_csv(config.DATA_DIR / 'scans.csv', parse_dates=['scan_date'])
        self.revenue = pd.read_csv(config.DATA_DIR / 'revenue.csv', parse_dates=['date'])

    def get_current_mrr(self):
        """Get current Monthly Recurring Revenue"""
        return self.revenue.iloc[-1]['mrr']

    def get_mrr_growth_rate(self, days=30):
        """Calculate MRR growth rate over specified days"""
        current_mrr = self.revenue.iloc[-1]['mrr']
        past_mrr = self.revenue.iloc[-days]['mrr']
        growth_rate = ((current_mrr - past_mrr) / past_mrr) * 100
        return growth_rate

    def get_arpu(self):
        """Calculate Average Revenue Per User"""
        active_subs = self.subscriptions[self.subscriptions['status'] == 'active']
        if len(active_subs) == 0:
            return 0
        return active_subs['mrr'].mean()

    def get_churn_rate(self, period_days=30):
        """Calculate churn rate for the specified period"""
        end_date = self.revenue['date'].max()
        start_date = end_date - timedelta(days=period_days)

        # Subscriptions active at start
        active_start = self.subscriptions[
            (self.subscriptions['subscription_start'] <= start_date) &
            ((self.subscriptions['subscription_end'].isna()) |
             (self.subscriptions['subscription_end'] > start_date))
        ]

        # Subscriptions that churned during period
        churned = self.subscriptions[
            (self.subscriptions['subscription_end'] >= start_date) &
            (self.subscriptions['subscription_end'] <= end_date)
        ]

        if len(active_start) == 0:
            return 0

        churn_rate = (len(churned) / len(active_start)) * 100
        return churn_rate

    def get_conversion_rate(self):
        """Calculate free to paid conversion rate"""
        total_users = len(self.users)
        total_conversions = len(self.subscriptions)
        return (total_conversions / total_users) * 100

    def get_cac(self):
        """Calculate average Customer Acquisition Cost"""
        return self.users['cac'].mean()

    def get_ltv(self):
        """Calculate Customer Lifetime Value"""
        # Simple LTV = ARPU / Churn Rate
        arpu = self.get_arpu()
        monthly_churn = self.get_churn_rate(30) / 100

        if monthly_churn == 0:
            return arpu * 36  # Cap at 3 years

        ltv = arpu / monthly_churn
        return min(ltv, arpu * 36)  # Cap at 3 years

    def get_ltv_cac_ratio(self):
        """Calculate LTV:CAC ratio"""
        ltv = self.get_ltv()
        cac = self.get_cac()
        return ltv / cac if cac > 0 else 0

    def get_active_users(self, period='daily'):
        """Get active users (users who performed scans)"""
        if period == 'daily':
            days = 1
        elif period == 'weekly':
            days = 7
        else:  # monthly
            days = 30

        cutoff_date = self.scans['scan_date'].max() - timedelta(days=days)
        active = self.scans[self.scans['scan_date'] > cutoff_date]['user_id'].nunique()
        return active

    def get_avg_match_rate(self):
        """Calculate average resume match rate"""
        return self.scans['match_rate'].mean()

    def get_avg_scans_per_user(self):
        """Calculate average scans per user"""
        return self.scans.groupby('user_id').size().mean()

    def get_cohort_analysis(self):
        """Generate cohort retention analysis"""
        # Group users by signup month
        self.users['cohort'] = self.users['signup_date'].dt.to_period('M')

        # Merge with scans to see activity
        user_scans = self.scans.merge(
            self.users[['user_id', 'cohort']],
            on='user_id'
        )

        user_scans['scan_month'] = user_scans['scan_date'].dt.to_period('M')

        # Calculate months since signup
        user_scans['months_since_signup'] = (
            (user_scans['scan_month'] - user_scans['cohort']).apply(lambda x: x.n)
        )

        # Create cohort matrix
        cohort_data = user_scans.groupby(['cohort', 'months_since_signup'])['user_id'].nunique().reset_index()
        cohort_pivot = cohort_data.pivot(
            index='cohort',
            columns='months_since_signup',
            values='user_id'
        )

        # Calculate retention percentages
        cohort_sizes = cohort_pivot.iloc[:, 0]
        retention = cohort_pivot.divide(cohort_sizes, axis=0) * 100

        return retention

    def get_conversion_funnel(self):
        """Calculate conversion funnel metrics"""
        total_users = len(self.users)
        users_with_scans = self.scans['user_id'].nunique()
        users_with_multiple_scans = self.scans.groupby('user_id').size()
        users_with_multiple_scans = len(users_with_multiple_scans[users_with_multiple_scans > 1])
        paid_users = len(self.subscriptions)

        funnel = {
            'Total Signups': total_users,
            'Performed 1+ Scan': users_with_scans,
            'Performed 2+ Scans': users_with_multiple_scans,
            'Converted to Paid': paid_users
        }

        return pd.DataFrame([funnel]).T.reset_index()

    def get_revenue_by_plan(self):
        """Calculate revenue breakdown by plan type"""
        active_subs = self.subscriptions[self.subscriptions['status'] == 'active']
        revenue_by_plan = active_subs.groupby('plan_type').agg({
            'mrr': 'sum',
            'user_id': 'count'
        }).reset_index()
        revenue_by_plan.columns = ['plan_type', 'mrr', 'subscribers']
        return revenue_by_plan

    def get_mrr_trend(self, days=90):
        """Get MRR trend for the last N days"""
        cutoff_date = self.revenue['date'].max() - timedelta(days=days)
        trend = self.revenue[self.revenue['date'] > cutoff_date][
            ['date', 'mrr', 'active_subscriptions']
        ].copy()
        return trend

    def detect_anomalies(self):
        """Detect anomalies in key metrics"""
        anomalies = []

        # Check churn rate
        churn_rate = self.get_churn_rate(30)
        if churn_rate > config.THRESHOLDS['churn_rate']['critical']:
            anomalies.append({
                'metric': 'Churn Rate',
                'value': f'{churn_rate:.2f}%',
                'severity': 'critical',
                'message': f'Churn rate ({churn_rate:.2f}%) exceeds critical threshold'
            })
        elif churn_rate > config.THRESHOLDS['churn_rate']['warning']:
            anomalies.append({
                'metric': 'Churn Rate',
                'value': f'{churn_rate:.2f}%',
                'severity': 'warning',
                'message': f'Churn rate ({churn_rate:.2f}%) exceeds warning threshold'
            })

        # Check conversion rate
        conversion_rate = self.get_conversion_rate()
        if conversion_rate < config.THRESHOLDS['conversion_rate']['critical']:
            anomalies.append({
                'metric': 'Conversion Rate',
                'value': f'{conversion_rate:.2f}%',
                'severity': 'critical',
                'message': f'Conversion rate ({conversion_rate:.2f}%) below critical threshold'
            })
        elif conversion_rate < config.THRESHOLDS['conversion_rate']['warning']:
            anomalies.append({
                'metric': 'Conversion Rate',
                'value': f'{conversion_rate:.2f}%',
                'severity': 'warning',
                'message': f'Conversion rate ({conversion_rate:.2f}%) below warning threshold'
            })

        # Check match rate
        avg_match_rate = self.get_avg_match_rate() / 100
        if avg_match_rate < config.THRESHOLDS['avg_match_rate']['critical']:
            anomalies.append({
                'metric': 'Avg Match Rate',
                'value': f'{avg_match_rate*100:.2f}%',
                'severity': 'critical',
                'message': f'Average match rate ({avg_match_rate*100:.2f}%) below critical threshold'
            })
        elif avg_match_rate < config.THRESHOLDS['avg_match_rate']['warning']:
            anomalies.append({
                'metric': 'Avg Match Rate',
                'value': f'{avg_match_rate*100:.2f}%',
                'severity': 'warning',
                'message': f'Average match rate ({avg_match_rate*100:.2f}%) below warning threshold'
            })

        # Check MRR growth
        mrr_growth = self.get_mrr_growth_rate(30) / 100
        if mrr_growth < config.THRESHOLDS['mrr_growth']['critical']:
            anomalies.append({
                'metric': 'MRR Growth',
                'value': f'{mrr_growth*100:.2f}%',
                'severity': 'critical',
                'message': f'MRR growth ({mrr_growth*100:.2f}%) below critical threshold'
            })
        elif mrr_growth < config.THRESHOLDS['mrr_growth']['warning']:
            anomalies.append({
                'metric': 'MRR Growth',
                'value': f'{mrr_growth*100:.2f}%',
                'severity': 'warning',
                'message': f'MRR growth ({mrr_growth*100:.2f}%) needs attention'
            })

        return anomalies

    def get_user_segment_performance(self):
        """Analyze performance by user segment"""
        # Merge users with subscriptions
        user_conversion = self.users.merge(
            self.subscriptions[['user_id', 'mrr']],
            on='user_id',
            how='left'
        )

        segment_stats = user_conversion.groupby('user_segment').agg({
            'user_id': 'count',
            'mrr': lambda x: x.notna().sum()
        }).reset_index()

        segment_stats.columns = ['segment', 'total_users', 'conversions']
        segment_stats['conversion_rate'] = (
            segment_stats['conversions'] / segment_stats['total_users'] * 100
        )

        return segment_stats

    def get_channel_performance(self):
        """Analyze performance by acquisition channel"""
        channel_users = self.users.groupby('acquisition_channel').agg({
            'user_id': 'count',
            'cac': 'mean'
        }).reset_index()

        channel_conversions = self.users.merge(
            self.subscriptions[['user_id', 'mrr']],
            on='user_id'
        ).groupby('acquisition_channel').size().reset_index(name='conversions')

        channel_stats = channel_users.merge(channel_conversions, on='acquisition_channel', how='left')
        channel_stats['conversions'] = channel_stats['conversions'].fillna(0)
        channel_stats['conversion_rate'] = (
            channel_stats['conversions'] / channel_stats['user_id'] * 100
        )

        channel_stats.columns = ['channel', 'total_users', 'avg_cac', 'conversions', 'conversion_rate']

        return channel_stats
