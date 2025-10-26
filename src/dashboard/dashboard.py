"""
JobMetrics Pro - Self-Service Analytics Dashboard
Main Streamlit application
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import config
from analytics import SaaSAnalytics
from ai_query import AIQueryEngine

# Page configuration
st.set_page_config(
    page_title=config.DASHBOARD_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .critical-alert {
        background-color: #ffebee;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #f44336;
    }
    .warning-alert {
        background-color: #fff3e0;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #ff9800;
    }
    .success-alert {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #4caf50;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_analytics():
    """Load analytics engine (cached)"""
    return SaaSAnalytics()


@st.cache_resource
def load_ai_engine():
    """Load AI query engine (cached)"""
    try:
        return AIQueryEngine()
    except ValueError:
        return None


def format_currency(value):
    """Format value as currency"""
    return f"${value:,.2f}"


def format_percentage(value):
    """Format value as percentage"""
    return f"{value:.2f}%"


def create_metric_card(label, value, delta=None, delta_color="normal"):
    """Create a metric display card"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.metric(label=label, value=value, delta=delta, delta_color=delta_color)


def display_anomalies(analytics):
    """Display anomaly alerts"""
    anomalies = analytics.detect_anomalies()

    if not anomalies:
        st.markdown("""
        <div class="success-alert">
            ✅ <strong>All systems normal</strong> - No critical anomalies detected
        </div>
        """, unsafe_allow_html=True)
        return

    for anomaly in anomalies:
        if anomaly['severity'] == 'critical':
            st.markdown(f"""
            <div class="critical-alert">
                🚨 <strong>{anomaly['metric']}</strong>: {anomaly['message']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="warning-alert">
                ⚠️ <strong>{anomaly['metric']}</strong>: {anomaly['message']}
            </div>
            """, unsafe_allow_html=True)


def render_overview_tab(analytics):
    """Render the Overview tab"""
    st.header("📊 Business Overview")

    # Display anomalies first
    with st.container():
        st.subheader("🔍 Health Check")
        display_anomalies(analytics)

    st.markdown("---")

    # Key Metrics Row 1
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mrr = analytics.get_current_mrr()
        mrr_growth = analytics.get_mrr_growth_rate(30)
        st.metric(
            "Monthly Recurring Revenue",
            format_currency(mrr),
            f"{mrr_growth:+.2f}% (30d)"
        )

    with col2:
        arpu = analytics.get_arpu()
        st.metric("Average Revenue Per User", format_currency(arpu))

    with col3:
        churn = analytics.get_churn_rate(30)
        st.metric("Churn Rate (30d)", format_percentage(churn))

    with col4:
        conversion = analytics.get_conversion_rate()
        st.metric("Conversion Rate", format_percentage(conversion))

    # Key Metrics Row 2
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        cac = analytics.get_cac()
        st.metric("Customer Acquisition Cost", format_currency(cac))

    with col2:
        ltv = analytics.get_ltv()
        st.metric("Lifetime Value", format_currency(ltv))

    with col3:
        ltv_cac = analytics.get_ltv_cac_ratio()
        st.metric("LTV:CAC Ratio", f"{ltv_cac:.2f}x")

    with col4:
        mau = analytics.get_active_users('monthly')
        st.metric("Monthly Active Users", f"{mau:,}")

    st.markdown("---")

    # MRR Trend Chart
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 MRR Trend (90 Days)")
        mrr_trend = analytics.get_mrr_trend(90)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=mrr_trend['date'],
            y=mrr_trend['mrr'],
            mode='lines',
            name='MRR',
            line=dict(color='#1f77b4', width=3),
            fill='tozeroy'
        ))

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="MRR ($)",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💰 Revenue by Plan")
        revenue_by_plan = analytics.get_revenue_by_plan()

        fig = px.pie(
            revenue_by_plan,
            values='mrr',
            names='plan_type',
            title='MRR Distribution'
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    # Product Metrics
    st.markdown("---")
    st.subheader("🎯 Product Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        avg_match_rate = analytics.get_avg_match_rate()
        st.metric("Avg Resume Match Rate", format_percentage(avg_match_rate))

    with col2:
        avg_scans = analytics.get_avg_scans_per_user()
        st.metric("Avg Scans per User", f"{avg_scans:.1f}")

    with col3:
        dau = analytics.get_active_users('daily')
        st.metric("Daily Active Users", f"{dau:,}")


def render_funnel_tab(analytics):
    """Render the Conversion Funnel tab"""
    st.header("🎯 Conversion Funnel Analysis")

    # Funnel visualization
    funnel_data = analytics.get_conversion_funnel()
    funnel_data.columns = ['Stage', 'Users']

    col1, col2 = st.columns([2, 1])

    with col1:
        # Calculate conversion rates between stages
        funnel_with_rates = funnel_data.copy()
        funnel_with_rates['Conversion_Rate'] = (
            funnel_with_rates['Users'] / funnel_with_rates['Users'].iloc[0] * 100
        )

        fig = go.Figure()

        fig.add_trace(go.Funnel(
            name='Users',
            y=funnel_with_rates['Stage'],
            x=funnel_with_rates['Users'],
            textposition="inside",
            textinfo="value+percent initial",
            marker=dict(
                color=["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728"]
            )
        ))

        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Funnel Metrics")
        for idx, row in funnel_with_rates.iterrows():
            st.metric(
                row['Stage'],
                f"{row['Users']:,}",
                f"{row['Conversion_Rate']:.1f}% of total"
            )

    # Segment performance
    st.markdown("---")
    st.subheader("📊 Performance by User Segment")

    segment_perf = analytics.get_user_segment_performance()

    fig = px.bar(
        segment_perf,
        x='segment',
        y='conversion_rate',
        title='Conversion Rate by User Segment',
        labels={'conversion_rate': 'Conversion Rate (%)', 'segment': 'User Segment'},
        color='conversion_rate',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Display table
    st.dataframe(
        segment_perf.style.format({
            'total_users': '{:,}',
            'conversions': '{:,}',
            'conversion_rate': '{:.2f}%'
        }),
        use_container_width=True
    )

    # Channel performance
    st.markdown("---")
    st.subheader("📢 Performance by Acquisition Channel")

    channel_perf = analytics.get_channel_performance()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            channel_perf,
            x='channel',
            y='conversion_rate',
            title='Conversion Rate by Channel',
            labels={'conversion_rate': 'Conversion Rate (%)', 'channel': 'Channel'},
            color='conversion_rate',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            channel_perf,
            x='avg_cac',
            y='conversion_rate',
            size='total_users',
            text='channel',
            title='CAC vs Conversion Rate',
            labels={'avg_cac': 'Avg CAC ($)', 'conversion_rate': 'Conversion Rate (%)'}
        )
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)

    # Display table
    st.dataframe(
        channel_perf.style.format({
            'total_users': '{:,}',
            'avg_cac': '${:.2f}',
            'conversions': '{:,.0f}',
            'conversion_rate': '{:.2f}%'
        }),
        use_container_width=True
    )


def render_cohort_tab(analytics):
    """Render the Cohort Analysis tab"""
    st.header("👥 Cohort Retention Analysis")

    st.info("""
    **Cohort Analysis** shows how user engagement changes over time for different signup cohorts.
    Each row represents users who signed up in a specific month, and columns show their activity in subsequent months.
    """)

    retention = analytics.get_cohort_analysis()

    # Convert period index to string for display
    retention_display = retention.copy()
    retention_display.index = retention_display.index.astype(str)

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=retention_display.values,
        x=[f"Month {i}" for i in retention_display.columns],
        y=retention_display.index,
        colorscale='Blues',
        text=retention_display.values.round(1),
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="Retention %")
    ))

    fig.update_layout(
        title="User Retention by Cohort (%)",
        xaxis_title="Months Since Signup",
        yaxis_title="Signup Cohort",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # Key insights
    st.subheader("📌 Key Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Average month 1 retention
        month_1_retention = retention_display.iloc[:, 1].mean()
        st.metric("Avg Month 1 Retention", f"{month_1_retention:.1f}%")

    with col2:
        # Average month 3 retention
        if len(retention_display.columns) > 3:
            month_3_retention = retention_display.iloc[:, 3].mean()
            st.metric("Avg Month 3 Retention", f"{month_3_retention:.1f}%")

    with col3:
        # Latest cohort size
        latest_cohort_size = retention_display.iloc[-1, 0]
        st.metric("Latest Cohort Size", f"{latest_cohort_size:.0f}")


def render_ai_query_tab(ai_engine):
    """Render the AI Query tab"""
    st.header("🤖 AI-Powered Analytics Assistant")

    if ai_engine is None:
        st.error("""
        ⚠️ AI Query feature is not available.

        To enable this feature:
        1. Get an API key from https://console.anthropic.com
        2. Add it to your .env file as ANTHROPIC_API_KEY=your_key_here
        3. Restart the dashboard
        """)
        return

    st.info("""
    Ask questions about your metrics in plain English! The AI assistant will analyze your data and provide insights.

    **Example questions:**
    - What's our current churn rate and should I be worried?
    - How is our MRR trending?
    - Which acquisition channel has the best ROI?
    - Why might our conversion rate be low?
    """)

    # Auto-generated insights
    with st.expander("✨ Auto-Generated Insights", expanded=True):
        if st.button("🔄 Generate Fresh Insights"):
            with st.spinner("Analyzing your data..."):
                insights_result = ai_engine.get_insights()

                if insights_result['success']:
                    for insight in insights_result['insights']:
                        st.markdown(f"### {insight['title']}")
                        st.write(f"**Insight:** {insight['insight']}")
                        st.write(f"**Impact:** {insight['impact']}")
                        st.write("**Recommended Actions:**")
                        for action in insight['actions']:
                            st.write(f"- {action}")
                        st.markdown("---")
                else:
                    st.error(f"Error generating insights: {insights_result['error']}")

    # Natural language query
    st.subheader("💬 Ask a Question")

    user_question = st.text_input(
        "Your question:",
        placeholder="e.g., What's driving our churn rate?"
    )

    if st.button("Ask AI Assistant", type="primary"):
        if user_question:
            with st.spinner("Thinking..."):
                result = ai_engine.query(user_question)

                if result['success']:
                    st.markdown("### Answer:")
                    st.write(result['answer'])

                    # Show metrics used
                    with st.expander("📊 Metrics Referenced"):
                        st.json(result['metrics_used'])

                    # Show anomalies
                    if result['anomalies']:
                        with st.expander("⚠️ Related Anomalies"):
                            for anomaly in result['anomalies']:
                                st.warning(f"{anomaly['metric']}: {anomaly['message']}")
                else:
                    st.error(result['answer'])
        else:
            st.warning("Please enter a question first.")

    # Metric explainer
    st.markdown("---")
    st.subheader("📖 Metric Explainer")

    metrics_to_explain = [
        'current_mrr', 'arpu', 'churn_rate', 'conversion_rate',
        'ltv', 'cac', 'ltv_cac_ratio'
    ]

    selected_metric = st.selectbox(
        "Select a metric to learn more:",
        metrics_to_explain,
        format_func=lambda x: x.replace('_', ' ').title()
    )

    if st.button("Explain This Metric"):
        with st.spinner("Generating explanation..."):
            result = ai_engine.explain_metric(selected_metric)

            if result['success']:
                st.markdown(result['explanation'])
            else:
                st.error(f"Error: {result['error']}")


def main():
    """Main dashboard application"""

    # Title and header
    st.title(config.DASHBOARD_TITLE)
    st.markdown(f"**{config.COMPANY_NAME}** | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Load analytics
    try:
        analytics = load_analytics()
        ai_engine = load_ai_engine()
    except FileNotFoundError:
        st.error("""
        ⚠️ Data files not found!

        Please run the data generator first:
        ```bash
        python data_generator.py
        ```
        """)
        return

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Dashboard Settings")

        st.subheader("📅 Date Range")
        # For now, using full dataset
        st.info("Currently showing all available data")

        st.markdown("---")

        st.subheader("📊 Quick Stats")
        st.metric("Total Users", f"{len(analytics.users):,}")
        st.metric("Active Subscriptions", f"{len(analytics.subscriptions[analytics.subscriptions['status'] == 'active']):,}")
        st.metric("Total Scans", f"{len(analytics.scans):,}")

        st.markdown("---")

        st.subheader("ℹ️ About")
        st.markdown("""
        This dashboard demonstrates:
        - **SaaS Metrics**: MRR, CAC, LTV, Churn
        - **Product Analytics**: Usage patterns
        - **AI Integration**: Natural language queries
        - **Automation**: Anomaly detection
        """)

    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "🎯 Conversion Funnel",
        "👥 Cohort Analysis",
        "🤖 AI Assistant"
    ])

    with tab1:
        render_overview_tab(analytics)

    with tab2:
        render_funnel_tab(analytics)

    with tab3:
        render_cohort_tab(analytics)

    with tab4:
        render_ai_query_tab(ai_engine)


if __name__ == "__main__":
    main()
