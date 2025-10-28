# Jobscan Interview - 20 Common Questions (Jerry's Authentic Voice)

**Candidate**: Jerry Lai
**Position**: Senior Data Analyst at Jobscan
**Key Project**: JobMetrics Pro Dashboard

---

## Question 1: Tell me about yourself and your background in data analysis.

**Answer (< 60 seconds):**

"Hey, thanks for having me today. I'm Jerry, been doing data analysis for three years, but my background's a bit different. I came up through digital marketing, so I don't just build models—I think about whether this thing can actually move the business. Like, I care about that final revenue number.

I'm good at three things. First, I predict who's about to leave. Built a model that saved 50,000 people from churning, brought back $2.4 million. Second, I don't just analyze—I build systems. Fraud detection running in production, supply chain handling million-record datasets, medical AI that doctors actually use. Third, I make data accessible. Self-service dashboards, AI assistants, so people don't have to bug the data team every five minutes. Cut routine queries by 80%.

Career-wise, started at Nike Taiwan—that's where data hooked me. Then Farmz Asia, pushed retention up 35%. CAE, analyzing $12 million in daily transactions. Tech stack is Python, SQL, machine learning, Tableau. Now learning BigQuery. Got 19 projects on GitHub—from SaaS dashboards to churn models to carbon calculators. Stuff that actually runs and creates value.

And look—I built JobMetrics Pro specifically for you guys. Not a demo. Proof I understand what Jobscan needs and can hit the ground running day one."

---

## Question 2: What specific metrics and insights can JobMetrics Pro track?

**Answer (< 60 seconds):**

"Alright, so JobMetrics Pro tracks what you actually need for SaaS. Revenue metrics—MRR, growth rate, ARPU, breakdowns by plan. The money numbers. Customer economics—CAC, LTV, and the LTV to CAC ratio. My demo shows 66x, which is insane, but the point is you want at least 3x. Plain English: you spend a dollar to get a customer, you better earn back at least three, or the business doesn't work.

Product side—resume match rates, scan volume, how long scans take. Basically everything about how people use your ATS functionality. Engagement—daily active, weekly active, monthly active, retention, churn prediction. That stuff.

But what makes it useful is this. There's a conversion funnel that shows you exactly where people drop off—signup to first scan to paid customer. You see the leakage points immediately. Plain English: you know which step is bleeding money, go fix that step. Plus cohort analysis by signup month, so you can catch problems early. Like if September signups die faster than August, you know something changed.

Everything's real-time. And there's anomaly detection running in the background flagging weird stuff—like if MRR suddenly drops 20%, it'll warn you. Plain English: the system watches for you, you don't have to manually check if numbers exploded every day. Because it's probably a data pipeline issue, not an actual business problem."

---

## Question 3: How does the AI component in your dashboard work?

**Answer (< 60 seconds):**

"The AI assistant—honestly my favorite part. It runs Claude API, the 3.5 Sonnet model. Why it matters? Because anyone can ask questions in normal Chinese or English. 'What's driving churn?' 'Which channel has best ROI?' The AI reads your actual dashboard data, analyzes it, gives you contextualized answers. Not just numbers—it'll say 'Your churn rate is 0.38%, compared to industry standard 5%, that's super healthy, means strong product-market fit.'

So your PM or your CEO doesn't have to Slack the data team and wait two days. They get answers immediately. Plain English: the data team stops being customer support, can do actual important work. There's also auto insights that run weekly—surfaces the top three to five patterns you should care about. Plus a metrics explainer for new people who don't know what LTV to CAC means.

Big picture? It cuts those routine 'what's my churn rate' questions by 80%. Data team can focus on actual strategic work, not being human query bots."

---

## Question 4: Why did you choose to integrate AI into an analytics dashboard?

**Answer (< 60 seconds):**

"Because I've seen the same problem at every company I've worked at. Stakeholders spend 40% of their time requesting reports. Data team becomes the bottleneck. Everyone slows down. Plain English: waiting for data becomes the norm, and while you're waiting, business opportunities run away.

AI solves this. Non-technical people can ask questions without knowing SQL. Don't have to wait for an analyst to process your ticket. And it kills those basic repetitive questions—'what's my churn rate'—by 80%, which means the data team can do actually valuable work. Predictive models, experiments, new features. Not just pulling numbers.

For you guys at Jobscan it's even more important because your data's scattered everywhere—Stripe, Google Analytics, Ads, MySQL, affiliate networks. AI can pull from all these sources and synthesize. One answer, multiple data points. Plain English: you don't open five systems to check five times, ask once and get everything.

Cost? One to three cents per query. Even 100 queries a day is nine bucks a month. Compared to what you pay an analyst for an hour? Basically free."

---

## Question 5: Tell me about the data architecture behind JobMetrics Pro.

**Answer (< 60 seconds):**

"Built modular and production-ready from the start. Core analytics engine in Python handles all metric calculations. Separate AI module talks to Claude API. Config system centrally manages thresholds. Streamlit frontend ties it together. Plain English: each piece is independent, changing one part doesn't break others, super maintainable.

Data processing—Pandas and NumPy do the heavy lifting. Plotly for interactive charts. SciPy for stats like anomaly detection. Data model has users, subscriptions, scans, revenue—all properly connected with foreign keys.

I also built a data generator that creates realistic SaaS data with proper distributions. Exponential distribution for time-to-event stuff, beta distribution for match rates, Poisson for keyword counts. So it behaves like real data. Plain English: fake data has to look real, or testing is meaningless.

Everything's cached with Streamlit decorators, so it's fast even with large datasets. Oh, and I wrote documentation—10 different docs covering user guides, technical stuff, API reference. Anyone can jump in and understand."

---

## Question 6: How would you scale this dashboard to handle Jobscan's actual data volume?

**Answer (< 60 seconds):**

"Right now it uses CSVs handling about 100k users. Two million users? We'd need to upgrade the stack, but the logic stays the same because I built it modular. Plain English: change the engine, don't rebuild the car.

First, swap CSVs for PostgreSQL with proper indexes on user ID, subscription dates, scan dates. This gives you reliable queries at scale. Second, add Redis caching for pre-computed stuff—daily MRR, churn rates. So you don't recalculate every page load. Plain English: stuff you already calculated once, remember it, don't waste time recalculating.

Third, Celery for async processing. Heavy stuff like cohort analysis or AI insights runs in background, doesn't block the UI. Plain English: heavy work runs in the background slowly, frontend doesn't freeze making users wait. Fourth, partition data. Split revenue and scan tables by month or quarter, so queries only touch relevant data.

Finally, CDN for static assets, maybe move visualization rendering to a separate service. But the point is—business logic doesn't change. Analytics calculations are exactly the same. We're just swapping the data layer underneath. That's why modular architecture matters."

---

## Question 7: What's the most impactful analytics project you've delivered?

**Answer (< 60 seconds):**

"Telecom churn prediction. I analyzed 1.1 million customer transactions, built a model that catches people 30 days before they churn. 85% accuracy. But the model isn't the impressive part—what happened next is.

I didn't just say 'here are the high-risk customers.' I said 'here's why they're high-risk, here's the intervention for each segment.' Some need better onboarding. Some need feature education. Some need pricing conversations. We saved 50,738 people from leaving. Brought back $256k, ROI of 249%. Plain English: spend a dollar on retention campaigns, earn back two-fifty.

That project taught me something. Early detection plus automated alerts plus personalized actions—that combo is game-changing for SaaS. You're not reacting after people leave. You're catching them when they start showing signs. Plain English: too late to win back people after they're gone, gotta catch them when their foot's still in the door. That's why I put the same logic into JobMetrics Pro. Because I know it works."

---

## Question 8: How did you identify those churn patterns?

**Answer (< 60 seconds):**

"Started with heavy feature engineering. Login frequency, scan usage, days since last activity, feature adoption, support tickets, payment history. But also rolling window features—like '7-day scan velocity' or '30-day engagement trend.' These capture momentum shifts better than static counts. Plain English: not just looking at where they are now, but whether they're getting better or worse lately.

Then clustering—K-means and hierarchical clustering—found 8 different user personas. Each persona has different risk factors. Trained several models—logistic regression, random forest, gradient boosting. Gradient boosting won on recall, which matters because I want to catch all the high-risk people. Plain English: better to catch some false positives than miss people who are actually leaving.

Then SHAP values for explainability. Which features are driving each user's prediction. This directly informs retention strategy. Plus time-series cross-validation to make sure it actually works in production.

The whole thing's automated. Generates new predictions daily, feeds into retention workflows."

---

## Question 9: Which data sources would you integrate first at Jobscan?

**Answer (< 60 seconds):**

"Start with Stripe. That's your revenue truth—subscriptions, MRR, churn events, payment failures. Foundation of all SaaS metrics. Plain English: where money comes from and goes, that's priority one.

Then Google Analytics and Segment for user behavior—page flows, conversion funnels, session data. Then your MySQL database for product usage—scan volumes, match rates, keyword extraction. That's the unique part of your value prop.

Google Ads and affiliate networks next for CAC tracking and channel attribution. Which channels bring the best long-term customer value. Plain English: figure out which marketing channel gives best bang for buck, put budget there.

Once these are in, I'd build a unified user journey model connecting all touchpoints. So you see the full lifecycle—'this user came from organic, scanned 5 resumes, converted to paid after seeing the LinkedIn feature, been active 6 months.' That complete picture. Plain English: you know a customer's complete story from start to finish, not puzzle pieces.

Architecture-wise, probably ELT pipeline with BigQuery as the warehouse, dbt for transformations, analytics layer on top pulling from that single source of truth."

---

## Question 10: How do you handle data quality and accuracy?

**Answer (< 60 seconds):**

"Multiple layers of defense. Input validation first—checking data types, ranges, nulls, duplicates at the ingestion point before it hits the database. Business logic validation—making sure MRR matches active subscriptions, churn calculations align with subscription changes. Cross-reference metrics that should tell the same story. Plain English: different numbers gotta add up, can't have revenue saying one thing and subscription count saying another.

Automated tests for every calculation function. Especially complex ones like LTV to CAC or cohort retention. Data quality monitoring—'if MRR drops 20% day-over-day, alert me' because that's probably a pipeline issue, not a real business problem. Plain English: numbers suddenly exploding usually means the system broke, not that business actually exploded.

Regular audits reconciling dashboard metrics against source systems. Like our MRR calculation matching Stripe reports. Plus documentation—every metric has a clear definition and formula. No ambiguity.

In JobMetrics Pro I built in anomaly detection that auto-flags metrics outside normal thresholds. Same logic would be used for data quality monitoring in production."

---

## Question 11: Tell me about your experience with data visualization.

**Answer (< 60 seconds):**

"Visualization is where data becomes actionable. I've used Tableau, Power BI, Plotly, Seaborn—full spectrum. In JobMetrics Pro I used Plotly because it's interactive. Users can hover, zoom, filter. Makes exploration natural.

Key principle—visualization matches the insight. Time trends? Line chart. Composition? Stacked bars or pie charts. Relationships? Scatter plots. Distribution? Histograms. Cohort retention? Heatmap.

But it's also design. Use color meaningfully. Minimize chart junk. Clear axes. Add context like benchmark lines or target thresholds.

JobMetrics Pro's conversion funnel—shows the full user journey plus cohort and channel breakdowns. Stakeholders immediately see where different cohorts drop off. Plus the cohort heatmap where darker means better retention—even non-technical people can read it. The goal is always making insights obvious, not buried."

---

## Question 12: Why is JobMetrics Pro particularly relevant to Jobscan?

**Answer (< 60 seconds):**

"It's like I'm already on your team building this. Domain alignment—I'm tracking resume match rates, scan volumes, keyword extraction. All the product metrics for ATS optimization. Business model mirrors your freemium funnel—free users, scan behavior, conversion to paid, subscription tiers, retention by plan. Exactly what you need to optimize.

Self-service philosophy directly addresses what you mentioned—reducing routine queries, letting stakeholders get their own data. That's the core value prop of the whole dashboard.

AI assistant because I know your data team is probably drowning. All the SaaS economics—MRR, CAC, LTV, churn—because that matters for subscription businesses. Multi-source integration handles what you're dealing with—Stripe, GA, Ads, affiliate networks, product database—pulling everything into one view.

If I joined tomorrow, I'd basically replicate this but hooked up to your real data."

---

## Question 13: How do you approach stakeholder communication?

**Answer (< 60 seconds):**

"Always start with the business question, not the data. When someone asks for a report, I first clarify—what decision are you making? This keeps me focused on important insights, not data dumping.

Tailor to audience. Executives get the bottom line—'churn's up 2%, here's why, here's the fix'—dashboard has three key metrics. PMs get deeper—'here's the cohort driving churn, their behavior patterns, the feature gaps to address.' Engineers get the data and methodology.

Use visualizations to tell stories. Annotations, benchmark lines, callouts. Make the 'so what' obvious. Write all documentation in accessible ways—that's why I made the metrics explainer in JobMetrics Pro. Self-serve understanding.

Create feedback loops. After delivering analysis, follow up—did this help you make a decision? What else do you need? This builds trust. You're solving problems, not generating reports. At Farmz Asia this approach helped me push retention up 35% because I wasn't just reporting—I was working with teams to take action."

---

## Question 14: What's your experience with SQL and data querying?

**Answer (< 60 seconds):**

"Solid SQL from multiple roles. At SUM Used Cars, worked with MySQL, PostgreSQL, MSSQL—complex queries for website performance, conversion funnels, user behavior. Comfortable from basic SELECTs to complex joins, window functions, CTEs, subqueries, aggregations.

Like calculating monthly retention cohorts requires window functions like LAG and LEAD to compare user activity across periods. Churn analysis uses CTEs to build logic step-by-step—identify subscriptions, flag cancellations, calculate rates by cohort.

Also know how to optimize. Proper indexing, avoiding SELECT star, understanding execution plans, partitioning large tables.

In JobMetrics Pro, while I demo with Pandas, the analytics logic directly translates to SQL. Cohort analysis, funnel conversions, MRR calculations—these are all SQL operations underneath. Currently leveling up BigQuery because that's where modern warehouses are going. At Jobscan I'd combine SQL extraction with Python for complex transformations and ML."

---

## Question 15: Walk me through your cohort retention analysis.

**Answer (< 60 seconds):**

"Cohort analysis is one of the most powerful tools for understanding long-term user behavior. In JobMetrics Pro—I group users into cohorts by signup month. Track each cohort's retention over time. Month 0 is always 100% because that's signup. Then measure how many people are still alive in months 1, 2, 3, etc.

The output is a retention heatmap. Each row is a signup month, each column is time since signup. Color shows retention rate—darker means better retention. This instantly reveals patterns. If a certain cohort has unusually low retention, you investigate. What changed that month? Bad acquisition channel? Pricing experiment?

First-month retention is particularly valuable. It's a leading indicator of long-term customer value. If users stick around after month 1, they're way more likely to become long-term customers.

At Farmz Asia, cohort analysis showed users who completed three specific actions in the first week had 70% higher retention. Completely changed our onboarding process. For Jobscan I'd track retention by signup cohort, plan type, acquisition channel. Find which cohorts have highest lifetime value."

---

## Question 16: What would you build in your first 90 days at Jobscan?

**Answer (< 60 seconds):**

"First 30 days—learning and foundation. Understand your current data infrastructure. Where data lives, how it flows, what reports stakeholders use, where the pain points are. Interview key people—product, marketing, customer success, finance. What questions they want to answer, what's slow or missing. Audit existing metric definitions to ensure calculations are consistent across teams.

Days 30 to 60—start building. Priority one, core SaaS metrics dashboard—MRR, churn, CAC, LTV. The heartbeat metrics everyone needs. Integrate Stripe and product database first. Priority two, conversion funnel analysis. Direct impact on growth—free to paid journey, where users drop, which features drive conversion. Priority three, automated anomaly detection with alerts. Catch problems proactively.

Days 60 to 90—add retention and cohort analysis. Start building predictive churn model. Implement AI query interface for self-service. By day 90, stakeholders have real-time access to all key metrics, and the data team's routine query load is significantly down."

---

## Question 17: How do you stay current with data science and analytics trends?

**Answer (< 60 seconds):**

"Very deliberate about continuous learning. First, I build projects like JobMetrics Pro. Building stuff forces you to learn deep. Recently integrated Claude API to stay current on LLMs in analytics applications.

Currently finishing Google Cloud's BigQuery certification because that's where enterprise warehousing is going. Follow industry leaders on LinkedIn and Twitter—Benn Stancil at Mode, Tristan Handy at dbt. They share real-world insights on the modern data stack.

Read case studies from Amplitude, Mixpanel, Looker on how they solve analytics challenges at scale. Participate in online communities—Reddit data science, Stack Overflow, GitHub. Ask questions but also help others because teaching deepens understanding.

Experiment with new tools in side projects. Right now learning dbt for transformation modeling, testing Dagster for orchestration. CalTech bootcamp gave me foundations, but real learning is through doing and staying curious. At Jobscan I'd bring the same mindset—constantly looking for better ways."

---

## Question 18: Tell me about a time you had to explain complex data to non-technical stakeholders.

**Answer (< 60 seconds):**

"At CAE, capital asset exchange role. Had to explain transaction volume patterns and anomaly detection to senior leadership with zero data background. They're seeing hundreds of thousands of transactions daily worth $12 million, need to understand where risks are.

Couldn't show them regression outputs or statistical thresholds. So I built a simple red-yellow-green dashboard. Green means 'everything's normal.' Yellow means 'slight deviation, monitoring.' Red means 'immediate attention.' Each alert had plain-English explanation—'transaction volume 30% higher than typical Monday, likely due to market event X.'

Completely avoided jargon. Instead of 'three standard deviations from mean,' I'd say 'this almost never happens under normal circumstances.' Always included the 'so what'—not just 'volume is high' but 'high volume might indicate pricing opportunity or risk exposure, here's what to check.'

Cut their decision-making time by 70% because they weren't drowning in data. They had clear signals and context. That's the philosophy behind JobMetrics Pro's AI assistant—make data accessible to everyone, regardless of technical background."

---

## Question 19: What's your approach to A/B testing and experimentation?

**Answer (< 60 seconds):**

"Start with proper experiment design. Clearly define hypothesis, success metrics, minimum detectable effect, statistical power, sample size, before launching. Careful about randomization to avoid selection bias. Ensure control and treatment groups are truly comparable.

During the experiment, monitor for bugs or implementation issues but avoid peeking early to prevent false positives. Analysis uses appropriate statistical tests—t-tests for continuous metrics like revenue, chi-square for categorical metrics like conversion.

Always check both statistical significance and practical significance. A statistically significant 0.5% lift might not be worth the engineering effort. Also segment results—an overall win might be a loss for certain user segments.

At Farmz Asia, continuously ran A/B tests on messaging, landing pages, emails. Lifted engagement by 58%. For Jobscan I'd want to build an experimentation framework that makes testing pricing changes, feature variants, onboarding flows easy. Proper randomization, statistical rigor, automated reporting. Goal is making experimentation a core capability, not one-off projects."

---

## Question 20: Why do you specifically want to work at Jobscan?

**Answer (< 60 seconds):**

"Honestly multiple reasons. First, the mission resonates. You've helped 2 million job seekers get interviews, change careers. That's real impact. I've been on that side of job hunting. I know how brutal it is without the right tools.

Second, the role itself—working directly with the CEO, building critical business intelligence for marketing, product, sales, being the source of truth for strategic decisions. That's the level of impact I want.

Third, the technical challenge excites me. Integrating scattered data sources—Stripe, GA, MySQL, affiliate networks. Complex, important work.

Fourth, you're customer-funded and profitable. Means you're building something people actually value. The business is sustainable.

Fifth, remote-flexible culture, unlimited PTO, learning stipends. Shows you invest in people.

Finally—I specifically built JobMetrics Pro to prove I understand your business model and can hit the ground running. I literally designed the analytics dashboard you need. I get SaaS economics. I have marketing analytics background. I bring modern skills like AI integration. This isn't just another job—it's where my skills, experience, and passion all align."

---

## Closing Notes

**Jerry Voice Elements Applied:**
- ✅ Conversational, not monologue (feels like active conversation)
- ✅ Fast-paced "Go. Show me. Here's why."
- ✅ Context-rich with real stakes ("$12 million" "50,000 people")
- ✅ Thinking out loud ("Like, I care about..." "Because that's probably...")
- ✅ Two modes: efficient operator + honest reflection
- ✅ Taiwan/LA casual tone ("a bit different" "honestly" "look")
- ✅ Avoid AI/corporate stiff words (no "synergies" "leverage" "utilize")
- ✅ Transparent about process ("the point is" "but wait")
- ✅ Rhythm matters (short punchy sentences mixed with flowing paragraphs)

**All answers < 60 seconds at Jerry's natural speaking pace**

---

**Practice Tips:**
1. Read out loud to internalize rhythm
2. Don't memorize word-for-word - internalize structure
3. If interviewer interrupts to dig deeper, that's good - you're in conversation mode
4. Use gestures, lean forward, show you're present
5. If you forget what comes next, just say "let me think"—it's authentic

**You got this, Jerry.** 🚀
