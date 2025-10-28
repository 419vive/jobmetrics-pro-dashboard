"""
AI-powered natural language query module using Claude API
"""
import anthropic
import pandas as pd
import json
from . import config
from .analytics import SaaSAnalytics


class AIQueryEngine:
    """Natural language query engine powered by Claude"""

    def __init__(self, analytics=None, time_range_days=None):
        """
        Initialize AI query engine

        Args:
            analytics: Optional pre-initialized SaaSAnalytics instance (takes precedence)
            time_range_days: Optional time range filter in days (only used if analytics not provided)
        """
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

        # Use provided analytics instance or create new one with time filter
        if analytics is not None:
            self.analytics = analytics
        else:
            self.analytics = SaaSAnalytics(time_range_days=time_range_days)

    def _get_metrics_context(self):
        """Get current metrics context for Claude"""
        # Get channel performance data
        channel_perf = self.analytics.get_channel_performance()
        channel_data = {}
        for _, row in channel_perf.iterrows():
            channel_data[row['channel']] = {
                "total_users": int(row['total_users']),
                "conversions": int(row['conversions']),
                "conversion_rate": f"{row['conversion_rate']:.2f}%",
                "avg_cac": f"${row['avg_cac']:.2f}",
                "avg_ltv": f"${row['avg_ltv']:.2f}",
                "ltv_cac_ratio": f"{row['ltv_cac_ratio']:.2f}",
                "roi": f"{row['roi']:.2f}%",
                "total_mrr": f"${row['total_mrr']:.2f}"
            }

        # Get conversion funnel data
        funnel = self.analytics.get_conversion_funnel()
        funnel_data = {}
        for _, row in funnel.iterrows():
            funnel_data[row['index']] = int(row[0])

        # Calculate funnel drop-off rates
        if 'Total Signups' in funnel_data and funnel_data['Total Signups'] > 0:
            total = funnel_data['Total Signups']
            first_scan = funnel_data.get('Performed 1+ Scan', 0)
            second_scan = funnel_data.get('Performed 2+ Scans', 0)
            paid = funnel_data.get('Converted to Paid', 0)

            funnel_data['activation_rate'] = f"{(first_scan / total * 100):.2f}%"
            funnel_data['engagement_rate'] = f"{(second_scan / total * 100):.2f}%"
            funnel_data['paid_conversion_rate'] = f"{(paid / total * 100):.2f}%"

            # FIX #1: Add explicit drop-off calculations
            if first_scan > 0:
                drop_off_first_to_second = first_scan - second_scan
                drop_off_pct = (drop_off_first_to_second / first_scan * 100)
                funnel_data['first_to_second_scan_retention_rate'] = f"{((second_scan / first_scan * 100)):.2f}%"
                funnel_data['first_to_second_scan_drop_off_rate'] = f"{drop_off_pct:.1f}%"
                funnel_data['first_to_second_scan_users_lost'] = drop_off_first_to_second

            if second_scan > 0:
                # FIX #2: Add engaged→paid conversion rate (for MRR gain calculations)
                engaged_to_paid_rate = (paid / second_scan * 100)
                funnel_data['engaged_to_paid_conversion_rate'] = f"{engaged_to_paid_rate:.2f}%"
                funnel_data['engaged_to_paid_users_lost'] = second_scan - paid

        # Get conversion funnel trends (to answer "is conversion declining?")
        funnel_trend = self.analytics.get_conversion_funnel_trend()
        funnel_trend_summary = {}
        for stage, data in funnel_trend['conversion_stages'].items():
            funnel_trend_summary[stage] = {
                'recent_rate': f"{data['recent_rate']:.2f}%",
                'previous_rate': f"{data['previous_rate']:.2f}%",
                'change': f"{data['change']:+.2f}%",
                'is_declining': data['is_declining'],
                'trend': '📉 下降' if data['is_declining'] else '📈 上升'
            }

        # Get user segment LTV analysis
        segment_ltv = self.analytics.get_user_segment_ltv_analysis()
        segment_data = {}
        for _, row in segment_ltv.iterrows():
            segment_data[row['segment']] = {
                "total_users": int(row['total_users']),
                "conversions": int(row['conversions']),
                "conversion_rate": f"{row['conversion_rate']:.2f}%",
                "avg_ltv": f"${row['avg_ltv']:.2f}",
                "avg_cac": f"${row['cac']:.2f}",
                "ltv_cac_ratio": f"{row['ltv_cac_ratio']:.2f}",
                "roi": f"{row['roi']:.1f}%",
                "total_mrr": f"${row['total_mrr']:.2f}",
                "avg_mrr": f"${row['avg_mrr']:.2f}",
                "active_subs": int(row['active_subs'])
            }

        context = {
            "current_mrr": f"${self.analytics.get_current_mrr():,.2f}",
            "mrr_growth_30d": f"{self.analytics.get_mrr_growth_rate(30):.2f}%",
            "arpu": f"${self.analytics.get_arpu():.2f}",
            "churn_rate": f"{self.analytics.get_churn_rate(30):.2f}%",
            "conversion_rate": f"{self.analytics.get_conversion_rate():.2f}%",
            "cac": f"${self.analytics.get_cac():.2f}",
            "ltv": f"${self.analytics.get_ltv():.2f}",
            "ltv_cac_ratio": f"{self.analytics.get_ltv_cac_ratio():.2f}",
            "dau": self.analytics.get_active_users('daily'),
            "wau": self.analytics.get_active_users('weekly'),
            "mau": self.analytics.get_active_users('monthly'),
            "avg_match_rate": f"{self.analytics.get_avg_match_rate():.2f}%",
            "avg_scans_per_user": f"{self.analytics.get_avg_scans_per_user():.2f}",
            "channel_performance": channel_data,
            "conversion_funnel": funnel_data,
            "conversion_funnel_trends": funnel_trend_summary,
            "user_segments": segment_data
        }
        return context

    def query(self, user_question):
        """
        Process natural language query and return insights

        Args:
            user_question: Natural language question from user

        Returns:
            Dictionary with answer and relevant data
        """
        # Get current metrics
        metrics = self._get_metrics_context()

        # Get anomalies
        anomalies = self.analytics.detect_anomalies()

        # Build prompt for Claude
        prompt = f"""You are an expert SaaS analytics assistant and business strategist for a job search/resume optimization platform (like Jobscan).

Current Metrics:
{json.dumps(metrics, indent=2)}

Recent Anomalies Detected:
{json.dumps(anomalies, indent=2) if anomalies else "No critical anomalies detected"}

User Question: {user_question}

## CRITICAL CALCULATION RULES:

### FIX #1 & #2: Drop-off Rate and MRR Gain Calculations
When calculating drop-off from First Scan → Engaged (2+ scans):
- Use the provided data: conversion_funnel.first_to_second_scan_drop_off_rate (already calculated correctly)
- For MRR gain projections, use conversion_funnel.engaged_to_paid_conversion_rate (NOT overall conversion rate)
- Example: If 10% improvement saves 166 users, and engaged→paid is 31%, then 166 × 0.31 = 51 new paid users

### FIX #3: Churn Rate Assessment (CRITICAL!)
**IMPORTANT**: Low churn is GOOD, not alarming! Use these benchmarks:
- churn < 1%: "世界級水準" / "World-class" / "Outstanding" ✅ (Don't say 令人擔憂!)
- churn 1-2%: "表現良好" / "Good" / "Healthy" ✅
- churn 2-3%: "表現正常" / "Average" / "Normal" ⚠️
- churn > 3%: "需要關注" / "Needs attention" / "Concerning" 🚨

**DO NOT** say churn is "alarming" or "concerning" if it's below 1%!

### FIX #4: Churn Loss Calculation (CRITICAL!)
When calculating annual churn loss:
- churn_rate in metrics is ALREADY A PERCENTAGE (e.g., "0.38%")
- To calculate loss: MRR × (churn_rate / 100) × 12
- Example: $92,148 × (0.38 / 100) × 12 = $4,232 annual loss
- DO NOT multiply by churn_rate directly (that would be 100x too high!)

## CRITICAL INSTRUCTIONS:

**YOU ALREADY HAVE ALL THE DATA YOU NEED**. Do NOT say things like:
- ❌ "需要進一步確認"
- ❌ "建議進行深入的漏斗分析"
- ❌ "需要更多數據"
- ❌ "數據中並沒有按照這些用戶類型做區隔的資訊"

**YOU HAVE COMPLETE DATA FOR**:
1. `conversion_funnel_trends` - 轉換率趨勢（過去 30 天 vs 30-60 天前）
2. `user_segments` - 三個用戶區隔的完整 LTV 分析：job_seeker, career_switcher, university_students
3. `conversion_funnel` - 當前的轉換漏斗數據
4. `channel_performance` - 各獲客渠道的表現

**YOUR JOB**: Analyze the data provided and give SPECIFIC answers with NUMBERS from these datasets.

## Response Guidelines:

When answering questions about **conversion funnels or free-to-paid conversion**:

**CRITICAL**: You now have `conversion_funnel_trends` data that shows:
- `signup_to_first_scan`: 註冊 → 首次掃描的轉換率（最近 30 天 vs 30-60 天前）
- `first_to_second_scan`: 首次掃描 → 第二次掃描的留存率（最近 30 天 vs 30-60 天前）
- `second_scan_to_paid`: 第二次掃描 → 付費的轉換率（最近 30 天 vs 30-60 天前）
- `overall_conversion`: 整體轉換率（註冊 → 付費）（最近 30 天 vs 30-60 天前）

Each stage shows:
- `recent_rate`: 最近 30 天的轉換率
- `previous_rate`: 30-60 天前的轉換率
- `change`: 變化量（正數=上升，負數=下降）
- `is_declining`: true/false（是否下降）
- `trend`: 📉 下降 或 📈 上升

**EXAMPLE OF GOOD ANSWER**:

"根據過去 30 天 vs 30-60 天前的數據：

**📉 整體轉換趨勢**: 是的，轉換率正在下降
- 整體轉換率從 26.3% 降到 24.1%（下降 2.2%）

**🎯 最大瓶頸**: 首次掃描 → 第二次掃描這一步
- 留存率從 55.3% 降到 48.2%（下降 7.1%）
- 這是所有步驟中下降最嚴重的

**💸 商業影響**:
- 約 7% 的用戶在首次掃描後就離開
- 如果轉換率是 25%，假設平均 ARPU $45，這相當於每個月流失約 $787 潛在 MRR（計算：10,000 用戶 × 7% × 25% × $45 = $787.5）

**✅ 立即行動**:
1. 在首次掃描後 2 小時內發送 Email 提醒「再掃一份履歷解鎖更多洞察」
2. A/B 測試不同的首次掃描結果呈現方式
3. 添加「對比分析」功能，鼓勵用戶掃描第二份履歷"

**MUST USE THIS FORMAT** to answer:
1. **分析趨勢 (Analyze Trend)**: 明確說出「過去 30 天 vs 30-60 天前」的變化，使用 conversion_funnel_trends 中的實際數字
2. **找出瓶頸 (Identify Bottleneck)**: 比較各階段的 change 值，找出最大的負數（下降最嚴重）
3. **商業意義 (Business Impact)**: 用白話解釋這對公司的影響，計算收入損失
4. **行動方案 (Action Plan)**: 針對最嚴重的瓶頸，給出 2-3 個具體可執行的建議

When answering questions about **user segments and LTV**:

**CRITICAL**: You now have `user_segments` data that shows LTV analysis for THREE user types:
- `job_seeker`: 正在找工作的求職者
- `career_switcher`: 轉職者（從 career_changer 和 professional 合併而來）
- `university_students`: 大學生（從 recent_grad 改名而來）

Each segment shows:
- `total_users`: 這個區隔有多少用戶
- `conversions`: 有多少轉換為付費
- `conversion_rate`: 轉換率（%）
- `avg_ltv`: 平均客戶終身價值（$）
- `avg_cac`: 平均獲客成本（$）
- `ltv_cac_ratio`: LTV:CAC 比例
- `roi`: 投資回報率（%）
- `total_mrr`: 這個區隔貢獻的總 MRR（$）
- `avg_mrr`: 每個付費用戶的平均 MRR（$）
- `active_subs`: 活躍訂閱數

**EXAMPLE OF GOOD ANSWER**:

"根據用戶區隔 LTV 數據分析：

**📊 三大區隔表現對比**:
- job_seeker: LTV $546.19, ROI 2111%, 轉換率 24.98%
- career_switcher: LTV $542.45, ROI 2151%, 轉換率 24.70%
- university_students: LTV $543.24, ROI 2123%, 轉換率 25.54%

**🎯 推薦投資優先級**: career_switcher
- 原因：雖然三個區隔 LTV 相近，但 career_switcher 的 ROI 最高（2151%）
- 獲客成本：平均 CAC 只有 $25.21，是最經濟的獲客管道

**💰 商業影響**:
- 如果將 70% 行銷預算投入 career_switcher，預期可提升整體 ROI 約 X%

**✅ 行動計劃**:
1. 主攻 career_switcher 市場...
2. 同時培養 university_students..."

**MUST USE THIS FORMAT** to answer:
1. **數據分析 (Data Analysis)**: 使用 user_segments 中的實際數字，清楚比較各個區隔的表現
2. **洞察原因 (Root Cause)**: 解釋為什麼這個區隔表現更好
3. **投資建議 (Investment Strategy)**: 明確建議應該 focus 哪一群，使用 ROI 和 LTV:CAC ratio 數據支持
4. **長期策略 (Long-term Strategy)**: 提供產品和市場策略方向

For ALL questions, provide:
- **Direct answer** with specific numbers
- **Business context** - explain why this matters to revenue/growth
- **Actionable next steps** - what should the team DO about this
- **Priority level** - is this urgent or can it wait

Use plain language (白話文). Speak as if you're the Head of Growth advising the CEO/CFO on strategic decisions. Focus on impact to revenue, customer lifetime value, and resource allocation."""

        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            answer = message.content[0].text

            return {
                "success": True,
                "answer": answer,
                "metrics_used": metrics,
                "anomalies": anomalies
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "answer": f"Sorry, I encountered an error: {str(e)}"
            }

    def get_insights(self):
        """Generate automatic insights about the business"""
        metrics = self._get_metrics_context()
        anomalies = self.analytics.detect_anomalies()

        prompt = f"""You are an expert SaaS analytics assistant and business strategist for a job search/resume optimization platform (like Jobscan).

Current Metrics:
{json.dumps(metrics, indent=2)}

Anomalies:
{json.dumps(anomalies, indent=2) if anomalies else "No critical anomalies detected"}

## CRITICAL CALCULATION RULES:

### FIX #1 & #2: Drop-off Rate and MRR Gain Calculations
When analyzing First Scan → Engaged (2+ scans) drop-off:
- Use the provided data: conversion_funnel.first_to_second_scan_drop_off_rate (already calculated correctly, ~17%)
- For MRR gain projections, use conversion_funnel.engaged_to_paid_conversion_rate (~31%, NOT the overall 25% rate)
- Example correct calculation:
  * Drop-off users: 1,661 (from conversion_funnel.first_to_second_scan_users_lost)
  * 10% improvement: 166 users saved
  * Engaged→Paid rate: 31% (from conversion_funnel.engaged_to_paid_conversion_rate)
  * New paid users: 166 × 0.31 = 51
  * Annual MRR gain: 51 × ARPU × 12 ≈ $28K (NOT $142K!)

### FIX #3: Churn Rate Assessment (CRITICAL!)
**IMPORTANT**: Low churn is GOOD, not alarming! Use these benchmarks:
- churn < 1%: "世界級水準 🏆" / "World-class" - This is EXCELLENT, not concerning!
- churn 1-2%: "表現良好 ✅" / "Good"
- churn 2-3%: "表現正常 ⚠️" / "Average"
- churn > 3%: "需要關注 🚨" / "Needs attention"

**Example**: If churn_rate is "0.38%", you MUST say it's "世界級水準" (world-class), NOT "令人擔憂" (alarming)!

### FIX #4: Churn Loss Calculation (CRITICAL!)
When calculating annual churn loss:
- churn_rate in metrics is ALREADY A PERCENTAGE STRING (e.g., "0.38%")
- Parse the number and divide by 100: 0.38 / 100 = 0.0038
- Formula: current_mrr × (churn_rate_number / 100) × 12
- Example: $92,148 × (0.38 / 100) × 12 = $4,232 annual loss (NOT $420K!)
- Common error: Using 0.38 directly gives 100x wrong answer

Please provide 3-5 key insights about the current state of the business. **PRIORITIZE** these two critical areas:

1. **Conversion Funnel Analysis**: Analyze the free-to-paid conversion journey. Look at conversion_funnel data and identify:
   - Which step has the biggest drop-off (signup → first scan → second scan → paid)
   - What's the business impact in potential MRR lost
   - Specific actions to reduce friction at that step

2. **User Segment Performance**: Analyze which user segment (user_segments data) contributes most LTV and should get investment priority:
   - Compare segments by conversion rate and lifetime value
   - Recommend where to allocate marketing budget
   - Explain the strategic rationale (why this segment, why now)

Then cover other important insights from: MRR growth trends, churn rate health, channel ROI, or any anomalies detected.

For each insight:
- **title**: Clear, action-oriented title (例如: "Career Switcher 區隔 ROI 最高，應優先投資")
- **insight**: The what + the why in plain language (白話文)
- **impact**: Business impact - revenue, growth, or efficiency gains/losses
- **actions**: 2-3 specific, executable next steps

Speak as if you're the Head of Growth advising the CEO/CFO. Focus on decisions that affect Q1 roadmap and budget allocation.

Format your response as a JSON array of objects with keys: "title", "insight", "impact", "actions" (array of strings)"""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract JSON from response
            response_text = message.content[0].text

            # Try to parse JSON from the response
            # Claude might wrap it in markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            insights = json.loads(response_text)

            return {
                "success": True,
                "insights": insights
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "insights": []
            }

    def explain_metric(self, metric_name):
        """Explain what a specific metric means and why it matters"""
        metrics = self._get_metrics_context()

        prompt = f"""You are an expert SaaS analytics assistant.

Current value of {metric_name}: {metrics.get(metric_name, 'Not available')}

Please explain:
1. What this metric means in simple terms
2. Why it's important for a SaaS business
3. What the current value indicates
4. Industry benchmarks or targets (if applicable)
5. How to improve this metric

Keep it concise and actionable."""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=512,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                "success": True,
                "explanation": message.content[0].text
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Test function
if __name__ == "__main__":
    try:
        engine = AIQueryEngine()

        # Test query
        print("Testing AI Query Engine...")
        print("="*60)

        result = engine.query("What's our churn rate and should I be worried?")
        print("\nQuestion: What's our churn rate and should I be worried?")
        print(f"\nAnswer:\n{result['answer']}")

        print("\n" + "="*60)

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("1. Set ANTHROPIC_API_KEY in .env file")
        print("2. Run data_generator.py first to create the datasets")
