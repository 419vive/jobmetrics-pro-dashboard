"""
Generate realistic SaaS metrics data for JobMetrics Pro Dashboard
Simulates a job search/resume optimization SaaS platform like Jobscan
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import config

np.random.seed(42)


class SaaSDataGenerator:
    """Generate realistic SaaS metrics data"""

    def __init__(self):
        self.start_date = pd.to_datetime(config.START_DATE)
        self.end_date = self.start_date + timedelta(days=config.DATE_RANGE_DAYS)
        self.num_users = config.NUM_USERS

    def generate_users(self):
        """Generate user registration data"""
        print("Generating users data...")

        # Users sign up over time with growth trend
        signup_dates = pd.date_range(
            start=self.start_date,
            end=self.end_date,
            periods=self.num_users
        )

        # Add some randomness to signup distribution
        signup_dates = signup_dates + pd.to_timedelta(
            np.random.randint(-7, 7, self.num_users), unit='D'
        )

        users = pd.DataFrame({
            'user_id': range(1, self.num_users + 1),
            'signup_date': signup_dates,
            'acquisition_channel': np.random.choice(
                ['organic', 'paid_search', 'social', 'referral', 'content'],
                self.num_users,
                p=[0.35, 0.25, 0.15, 0.15, 0.10]
            ),
            'user_segment': np.random.choice(
                ['job_seeker', 'career_changer', 'recent_grad', 'professional'],
                self.num_users,
                p=[0.40, 0.25, 0.20, 0.15]
            ),
            'country': np.random.choice(
                ['US', 'UK', 'CA', 'AU', 'IN'],
                self.num_users,
                p=[0.50, 0.20, 0.15, 0.10, 0.05]
            )
        })

        # Add Customer Acquisition Cost (CAC) based on channel
        cac_map = {
            'organic': 0,
            'paid_search': np.random.uniform(30, 80, self.num_users),
            'social': np.random.uniform(20, 50, self.num_users),
            'referral': np.random.uniform(10, 25, self.num_users),
            'content': np.random.uniform(15, 40, self.num_users)
        }

        users['cac'] = users['acquisition_channel'].apply(
            lambda x: cac_map[x] if x == 'organic' else
            np.random.choice(cac_map[x])
        )

        return users

    def generate_subscriptions(self, users):
        """Generate subscription data (free to paid conversions)"""
        print("Generating subscriptions data...")

        subscriptions = []

        for _, user in users.iterrows():
            user_id = user['user_id']
            signup_date = user['signup_date']

            # 25% convert from free to paid
            if np.random.random() < 0.25:
                # Time to conversion (1-30 days)
                days_to_convert = np.random.exponential(7)
                days_to_convert = min(days_to_convert, 30)

                conversion_date = signup_date + timedelta(days=days_to_convert)

                # Plan types with pricing
                plan_type = np.random.choice(
                    ['basic', 'professional', 'premium'],
                    p=[0.50, 0.35, 0.15]
                )

                plan_prices = {'basic': 29.99, 'professional': 49.99, 'premium': 99.99}
                mrr = plan_prices[plan_type]

                # Billing cycle
                billing_cycle = np.random.choice(['monthly', 'annual'], p=[0.70, 0.30])
                if billing_cycle == 'annual':
                    mrr = mrr * 0.85  # 15% discount for annual

                # Calculate churn
                # Lower churn for annual, professional, and premium
                base_churn_prob = 0.05
                if billing_cycle == 'annual':
                    base_churn_prob *= 0.5
                if plan_type in ['professional', 'premium']:
                    base_churn_prob *= 0.7

                # Check if churned
                days_since_conversion = (self.end_date - conversion_date).days
                months_subscribed = max(1, days_since_conversion / 30)

                churned = False
                churn_date = None

                for month in range(int(months_subscribed)):
                    if np.random.random() < base_churn_prob:
                        churned = True
                        churn_date = conversion_date + timedelta(days=month * 30)
                        break

                subscriptions.append({
                    'user_id': user_id,
                    'subscription_start': conversion_date,
                    'subscription_end': churn_date if churned else None,
                    'plan_type': plan_type,
                    'billing_cycle': billing_cycle,
                    'mrr': mrr,
                    'status': 'churned' if churned else 'active'
                })

        return pd.DataFrame(subscriptions)

    def generate_resume_scans(self, users, subscriptions):
        """Generate resume scan activity data"""
        print("Generating resume scans data...")

        scans = []

        for _, user in users.iterrows():
            user_id = user['user_id']
            signup_date = user['signup_date']

            # Check if user has subscription
            user_sub = subscriptions[subscriptions['user_id'] == user_id]
            is_paid = len(user_sub) > 0

            # Free users: 1-5 scans, Paid users: 5-50 scans
            num_scans = np.random.randint(1, 6) if not is_paid else np.random.randint(5, 51)

            for scan_num in range(num_scans):
                # Scan happens after signup
                days_after_signup = np.random.exponential(30)
                scan_date = signup_date + timedelta(days=days_after_signup)

                # Don't create scans after end date
                if scan_date > self.end_date:
                    continue

                # Match rate (paid users get better matches due to more features)
                if is_paid:
                    match_rate = np.random.beta(8, 2) * 100  # Higher match rates
                else:
                    match_rate = np.random.beta(5, 3) * 100  # Lower match rates

                # Processing time (milliseconds)
                processing_time = np.random.gamma(2, 500)

                # Number of keywords extracted
                keywords_extracted = np.random.poisson(15)

                # Job title matched against
                job_titles = [
                    'Software Engineer', 'Data Analyst', 'Product Manager',
                    'Marketing Manager', 'Sales Representative', 'Designer',
                    'Accountant', 'HR Manager', 'Operations Manager'
                ]

                scans.append({
                    'user_id': user_id,
                    'scan_date': scan_date,
                    'match_rate': match_rate,
                    'processing_time_ms': processing_time,
                    'keywords_extracted': keywords_extracted,
                    'job_title': np.random.choice(job_titles),
                    'is_paid_user': is_paid
                })

        return pd.DataFrame(scans)

    def generate_revenue(self, subscriptions):
        """Generate monthly recurring revenue data"""
        print("Generating revenue data...")

        date_range = pd.date_range(
            start=self.start_date,
            end=self.end_date,
            freq='D'
        )

        daily_revenue = []

        for date in date_range:
            # Calculate active subscriptions on this date
            active_subs = subscriptions[
                (subscriptions['subscription_start'] <= date) &
                ((subscriptions['subscription_end'].isna()) |
                 (subscriptions['subscription_end'] > date))
            ]

            # Daily revenue (MRR / 30)
            daily_mrr = active_subs['mrr'].sum() / 30

            # Number of active subscriptions
            num_active = len(active_subs)

            # New subscriptions today
            new_subs = len(subscriptions[
                subscriptions['subscription_start'].dt.date == date.date()
            ])

            # Churned subscriptions today
            churned_subs = len(subscriptions[
                subscriptions['subscription_end'].notna() &
                (subscriptions['subscription_end'].dt.date == date.date())
            ])

            daily_revenue.append({
                'date': date,
                'daily_revenue': daily_mrr,
                'mrr': active_subs['mrr'].sum(),
                'active_subscriptions': num_active,
                'new_subscriptions': new_subs,
                'churned_subscriptions': churned_subs
            })

        return pd.DataFrame(daily_revenue)

    def generate_all(self):
        """Generate all datasets"""
        print(f"\n{'='*60}")
        print("JobMetrics Pro - Data Generation")
        print(f"{'='*60}\n")

        # Generate data
        users = self.generate_users()
        subscriptions = self.generate_subscriptions(users)
        scans = self.generate_resume_scans(users, subscriptions)
        revenue = self.generate_revenue(subscriptions)

        # Save to CSV
        print("\nSaving data to CSV files...")
        users.to_csv(config.DATA_DIR / 'users.csv', index=False)
        subscriptions.to_csv(config.DATA_DIR / 'subscriptions.csv', index=False)
        scans.to_csv(config.DATA_DIR / 'scans.csv', index=False)
        revenue.to_csv(config.DATA_DIR / 'revenue.csv', index=False)

        # Print summary statistics
        print(f"\n{'='*60}")
        print("Data Generation Summary")
        print(f"{'='*60}")
        print(f"Total Users: {len(users):,}")
        print(f"Total Subscriptions: {len(subscriptions):,}")
        print(f"Active Subscriptions: {len(subscriptions[subscriptions['status'] == 'active']):,}")
        print(f"Total Scans: {len(scans):,}")
        print(f"Conversion Rate: {len(subscriptions) / len(users) * 100:.2f}%")
        print(f"Current MRR: ${revenue.iloc[-1]['mrr']:,.2f}")
        print(f"Average MRR per User: ${revenue.iloc[-1]['mrr'] / revenue.iloc[-1]['active_subscriptions']:.2f}")
        print(f"\nData saved to: {config.DATA_DIR}")
        print(f"{'='*60}\n")

        return users, subscriptions, scans, revenue


if __name__ == "__main__":
    generator = SaaSDataGenerator()
    generator.generate_all()
