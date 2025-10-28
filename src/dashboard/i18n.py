"""
Internationalization (i18n) support for Dashboard
Multi-language text content
"""

def get_mrr_status(mrr_growth, lang='zh'):
    """生成 MRR 戰況說明"""
    if lang == 'zh':
        if mrr_growth > 15:
            return f"MRR 漲了 {mrr_growth:.1f}% 🚀\n→ **成長很猛**！策略有效，繼續加碼"
        elif mrr_growth > 5:
            return f"MRR 漲了 {mrr_growth:.1f}% ✅\n→ **穩定成長中**，繼續保持"
        elif mrr_growth > 0:
            return f"MRR 只漲了 {mrr_growth:.1f}% ⚠️\n→ **成長在放慢**，該注意了"
        elif mrr_growth > -5:
            return f"MRR 掉了 {abs(mrr_growth):.1f}% 🚨\n→ **紅燈**！流失太快，得馬上處理"
        else:
            return f"MRR 大跌 {abs(mrr_growth):.1f}% 🔥\n→ **緊急狀況**！立刻找出原因"
    else:
        if mrr_growth > 15:
            return f"MRR grew {mrr_growth:.1f}% 🚀 - Strong growth!"
        elif mrr_growth > 5:
            return f"MRR grew {mrr_growth:.1f}% ✅ - Steady growth"
        elif mrr_growth > 0:
            return f"MRR only grew {mrr_growth:.1f}% ⚠️ - Slowing down"
        elif mrr_growth > -5:
            return f"MRR dropped {abs(mrr_growth):.1f}% 🚨 - Warning!"
        else:
            return f"MRR crashed {abs(mrr_growth):.1f}% 🔥 - Emergency!"

def get_churn_status(churn_rate, lang='zh'):
    """生成流失率戰況說明"""
    if lang == 'zh':
        if churn_rate < 3:
            return f"流失率 {churn_rate:.1f}% ✅\n→ **健康**！產品有黏性，繼續做"
        elif churn_rate < 5:
            return f"流失率 {churn_rate:.1f}% ⚠️\n→ **還可以**，但要開始注意了"
        elif churn_rate < 10:
            return f"流失率 {churn_rate:.1f}% 🚨\n→ **警戒**！會拖累成長，得處理"
        else:
            return f"流失率 {churn_rate:.1f}% 🔥\n→ **致命**！用戶在大量流失"
    else:
        if churn_rate < 3:
            return f"Churn {churn_rate:.1f}% ✅ - Healthy!"
        elif churn_rate < 5:
            return f"Churn {churn_rate:.1f}% ⚠️ - Acceptable"
        elif churn_rate < 10:
            return f"Churn {churn_rate:.1f}% 🚨 - Warning!"
        else:
            return f"Churn {churn_rate:.1f}% 🔥 - Critical!"

def get_ltv_cac_status(ltv_cac, lang='zh'):
    """生成 LTV:CAC 戰況說明"""
    if lang == 'zh':
        if ltv_cac > 5:
            return f"LTV:CAC = {ltv_cac:.1f}x 🚀\n→ **非常健康**！可以放心加大獲客預算"
        elif ltv_cac > 3:
            return f"LTV:CAC = {ltv_cac:.1f}x ✅\n→ **健康**！單位經濟很好"
        elif ltv_cac > 1:
            return f"LTV:CAC = {ltv_cac:.1f}x ⚠️\n→ **還可以**，但要優化降低獲客成本"
        else:
            return f"LTV:CAC = {ltv_cac:.1f}x 🚨\n→ **虧錢**！別再燒錢了，先解決這個"
    else:
        if ltv_cac > 5:
            return f"LTV:CAC = {ltv_cac:.1f}x 🚀 - Excellent!"
        elif ltv_cac > 3:
            return f"LTV:CAC = {ltv_cac:.1f}x ✅ - Healthy"
        elif ltv_cac > 1:
            return f"LTV:CAC = {ltv_cac:.1f}x ⚠️ - Needs improvement"
        else:
            return f"LTV:CAC = {ltv_cac:.1f}x 🚨 - Unprofitable!"

def get_arpu_status(arpu, prev_arpu, lang='zh'):
    """生成 ARPU 戰況說明"""
    if prev_arpu and prev_arpu > 0:
        change = ((arpu - prev_arpu) / prev_arpu) * 100
        if lang == 'zh':
            if change > 5:
                return f"ARPU 從 ${prev_arpu:.2f} 漲到 ${arpu:.2f} 🚀\n→ **成長 {change:.1f}%**！客戶願意付更多錢"
            elif change > 0:
                return f"ARPU 從 ${prev_arpu:.2f} 漲到 ${arpu:.2f} ✅\n→ **微幅成長 {change:.1f}%**，繼續優化"
            elif change > -5:
                return f"ARPU 從 ${prev_arpu:.2f} 掉到 ${arpu:.2f} ⚠️\n→ **下降 {abs(change):.1f}%**，客戶在降級"
            else:
                return f"ARPU 從 ${prev_arpu:.2f} 跌到 ${arpu:.2f} 🚨\n→ **大跌 {abs(change):.1f}%**！檢查定價策略"
        else:
            if change > 5:
                return f"ARPU grew from ${prev_arpu:.2f} to ${arpu:.2f} 🚀 (+{change:.1f}%)"
            elif change > 0:
                return f"ARPU grew from ${prev_arpu:.2f} to ${arpu:.2f} ✅ (+{change:.1f}%)"
            elif change > -5:
                return f"ARPU dropped from ${prev_arpu:.2f} to ${arpu:.2f} ⚠️ ({change:.1f}%)"
            else:
                return f"ARPU crashed from ${prev_arpu:.2f} to ${arpu:.2f} 🚨 ({change:.1f}%)"
    else:
        if lang == 'zh':
            return f"ARPU = ${arpu:.2f}/人"
        else:
            return f"ARPU = ${arpu:.2f} per user"

def get_conversion_status(conversion_rate, lang='zh'):
    """生成轉換率戰況說明"""
    if lang == 'zh':
        if conversion_rate > 20:
            return f"轉換率 {conversion_rate:.1f}% 🚀\n→ **很健康**！產品價值很明確"
        elif conversion_rate > 10:
            return f"轉換率 {conversion_rate:.1f}% ✅\n→ **還可以**，有優化空間"
        elif conversion_rate > 5:
            return f"轉換率 {conversion_rate:.1f}% ⚠️\n→ **偏低**，要檢討產品體驗或定價"
        else:
            return f"轉換率 {conversion_rate:.1f}% 🚨\n→ **有問題**！大部分人不願意付費"
    else:
        if conversion_rate > 20:
            return f"Conversion {conversion_rate:.1f}% 🚀 - Excellent!"
        elif conversion_rate > 10:
            return f"Conversion {conversion_rate:.1f}% ✅ - Good"
        elif conversion_rate > 5:
            return f"Conversion {conversion_rate:.1f}% ⚠️ - Low"
        else:
            return f"Conversion {conversion_rate:.1f}% 🚨 - Critical!"

def get_mau_status(mau, prev_mau, lang='zh'):
    """生成 MAU 戰況說明"""
    if prev_mau and prev_mau > 0:
        change = ((mau - prev_mau) / prev_mau) * 100
        if lang == 'zh':
            if change > 10:
                return f"MAU 從 {prev_mau:,} 漲到 {mau:,} 🚀\n→ **成長 {change:.1f}%**！產品在快速擴張"
            elif change > 0:
                return f"MAU 從 {prev_mau:,} 漲到 {mau:,} ✅\n→ **成長 {change:.1f}%**，穩定成長中"
            elif change > -10:
                return f"MAU 從 {prev_mau:,} 掉到 {mau:,} ⚠️\n→ **下降 {abs(change):.1f}%**，用戶在流失"
            else:
                return f"MAU 從 {prev_mau:,} 跌到 {mau:,} 🚨\n→ **大跌 {abs(change):.1f}%**！產品留存有問題"
        else:
            if change > 10:
                return f"MAU grew from {prev_mau:,} to {mau:,} 🚀 (+{change:.1f}%)"
            elif change > 0:
                return f"MAU grew from {prev_mau:,} to {mau:,} ✅ (+{change:.1f}%)"
            elif change > -10:
                return f"MAU dropped from {prev_mau:,} to {mau:,} ⚠️ ({change:.1f}%)"
            else:
                return f"MAU crashed from {prev_mau:,} to {mau:,} 🚨 ({change:.1f}%)"
    else:
        if lang == 'zh':
            return f"MAU = {mau:,} 活躍用戶"
        else:
            return f"MAU = {mau:,} active users"

LANGUAGES = {
    'zh': {
        # Header
        'data_status': '📊 數據狀態',
        'real_time_update': '✅ 實時更新',
        'update_time': '更新時間',
        'refresh_data': '🔄 刷新數據',
        'refresh_help': '重新加載最新數據',

        # Sidebar
        'control_panel': '⚙️ 控制面板',
        'quick_actions': '⚡ 快速操作',
        'export_report': '📥 匯出報告',
        'export_help': '匯出當前數據為 CSV',
        'export_dev': '匯出功能開發中...',
        'email_report': '📧 Email 報告',
        'email_help': '將報告發送到您的信箱',
        'email_dev': 'Email 功能開發中...',
        'data_filter': '🎛️ 數據篩選',
        'time_range': '時間範圍',
        'time_range_help': '選擇要查看的時間範圍',
        'all_data': '全部數據',
        'last_7_days': '過去 7 天',
        'last_30_days': '過去 30 天',
        'last_90_days': '過去 90 天',
        'last_year': '過去一年',
        'health_check': '🏥 健康快檢',
        'mrr_growth_strong': '🟢 MRR 成長強勁',
        'mrr_growth_stable': '🟡 MRR 穩定成長',
        'mrr_growth_slow': '🔴 MRR 成長緩慢',
        'churn_excellent': '🟢 流失率優秀',
        'churn_normal': '🟡 流失率正常',
        'churn_high': '🔴 流失率過高',
        'basic_stats': '📊 基本統計',
        'total_users': '總用戶數',
        'total_users_help': '註冊用戶總數',
        'active_subs': '活躍訂閱',
        'active_subs_help': '當前付費訂閱數',
        'total_scans': '總掃描次數',
        'total_scans_help': '所有用戶的履歷掃描總數',
        'about_dashboard': 'ℹ️ 關於此 Dashboard',
        'features': '**功能特色**',
        'feature_1': '🎯 實時 SaaS 指標追蹤',
        'feature_2': '📈 智能異常檢測',
        'feature_3': '🤖 AI 數據分析助手',
        'feature_4': '🔔 自動警報系統',
        'data_source': '**數據來源**: 模擬數據',
        'update_freq': '**更新頻率**: 實時',
        'tip': '💡 **提示**: 使用頂部的刷新按鈕來更新數據快取',

        # Tabs
        'tab_overview': '📊 Overview',
        'tab_funnel': '🎯 Conversion Funnel',
        'tab_cohort': '👥 Cohort Analysis',
        'tab_ai': '🤖 AI Assistant',

        # Overview Tab
        # Project Context Note Pad (STAR + 5W1H)
        'project_context_note': '''
## 🤔 **如果你無法在 30 秒內回答這 4 個問題，你需要這個 Dashboard**

---

### 🎯 **SITUATION (情境)**

**WHO** 誰在用這個產品？
→ **JobMetrics Pro** 的用戶 — 求職者使用 AI 履歷掃描服務來優化履歷

**WHAT** 這是什麼類型的業務？
→ **SaaS 訂閱制產品** — 用戶註冊 → 免費試用掃描 → 付費訂閱

**WHERE** 數據從哪裡來？
→ 從 4 個核心數據表：`users`（用戶註冊）、`scans`（掃描行為）、`subscriptions`（訂閱狀態）、`revenue`（收入數據）

**WHEN** 現在處於什麼階段？
→ **產品成長期** — 已有 10,000 用戶、2,500+ 付費訂閱、月收入 $92K+

---

### 🚨 **TASK (任務)**

**WHY** 為什麼需要這個 Dashboard？
→ **決策困境**：雖然有數據，但分散在多個表，無法快速回答關鍵問題：
  • 💰 收入是在長還是在掉？
  • 📉 用戶為什麼流失？
  • 🎯 哪個環節轉換率最低？
  • 💡 下一步該優化什麼？

**目標**：建立一個「自助式分析儀表板」，讓決策者能在 **30 秒內** 找到答案並採取行動

---

### ⚙️ **ACTION (行動)**

**HOW** 怎麼解決？
1. **📊 數據整合** — 將 4 個數據表整合成 SaaS 關鍵指標（MRR、流失率、LTV、轉換率等）
2. **🎨 視覺化設計** — 用漏斗圖、趨勢圖、對比卡片讓複雜數據一目了然
3. **🤖 AI 洞察** — 內建 AI Query 引擎，用自然語言問問題，立即獲得數據驅動的建議
4. **🧮 Jerry 風格解釋** — 每個數字都附上「怎麼算的」和「為什麼重要」的詳細說明

**核心功能模組**：
→ **Overview（總覽）** — 3 秒看懂生意健康度
→ **Funnel（漏斗）** — 找出轉換率瓶頸
→ **Revenue（收入）** — 追蹤收入趨勢和異常
→ **AI Insights（洞察）** — 用自然語言提問，獲得行動建議

---

### 🎉 **RESULT (成果)**

**這個 Dashboard 能幫你做什麼？**

✅ **快速決策** — 30 秒內看懂核心指標，無需 SQL 或 BI 工具
✅ **找到瓶頸** — 漏斗分析明確指出「哪個環節在掉用戶」
✅ **數據驅動** — 每個建議都基於真實數據計算，不是猜測
✅ **行動導向** — 不只告訴你「發生了什麼」，還告訴你「該做什麼」

**💡 設計哲學**：
→ **Jerry 風格** = 數字背後的「為什麼」比數字本身更重要
→ **自助式** = 非技術人員也能自己探索數據
→ **決策驅動** = 每個圖表都回答一個具體的業務問題

---

**📌 使用建議**：
1. 先看 **Overview** 掌握整體健康度
2. 再看 **Funnel** 找出轉換瓶頸
3. 最後用 **AI Insights** 問「我該優化什麼？」
''',

        # Period Comparison Section
        'period_comparison': '📊 本期 vs 上期對比',
        'period_comparison_help': '''**這個「對比」是怎麼算的？**

我先講人話版本：

→ **本期** = 你選擇的時間範圍（例如：過去 30 天）
→ **上期** = 本期之前的同等長度時間（例如：再往前 30 天）

**舉例說明**：
• 如果你選「過去 30 天」
  → 本期 = 最近 30 天（12/25 - 1/24）
  → 上期 = 前一個 30 天（11/25 - 12/24）

• 如果你選「過去 7 天」
  → 本期 = 最近 7 天
  → 上期 = 前一個 7 天

**為什麼這樣比？**
→ 讓你快速看出「生意是在長還是在掉」
→ 綠色向上箭頭 = 進步了 ✅
→ 紅色向下箭頭 = 退步了 ⚠️

就像你每個月看體重計，這個月 vs 上個月，馬上知道是胖了還是瘦了。

**🔍 我們怎麼確保準確？**（技術細節）
→ **精確篩選**：系統會精確篩選「上期」的數據，不會混入其他時間範圍
→ **數據驗證**：檢查上期是否有足夠數據（至少需要 30% 的預期數據量）
→ **智能降級**：如果上期數據不足，會基於本期數據和成長率做合理估算
→ **錯誤處理**：即使遇到異常情況，也會自動使用備用計算方式，不會崩潰

**為什麼需要這些？**
因為早期數據可能不完整，這樣可以確保：
1. 有數據時 = 用真實數據（最準確）
2. 數據不足時 = 用估算（至少有參考價值）
3. 永遠不會因為數據問題而顯示錯誤或崩潰
''',
        'current_period': '本期',
        'previous_period': '上期',
        'vs_last_period': 'vs 上期',

        'revenue_status': '💰 收入狀況 — 這個月賺多少？',
        'period_total_revenue': '📊 選定期間總收入',
        'period_total_revenue_help': '''**這個數字代表什麼？**

這是你選擇的時間範圍內的**實際總收入**。

**和 MRR 有什麼不同？**
• **MRR** = 當前的月經常性收入（一個時間點的快照）
• **期間總收入** = 選定時間內實際賺的所有錢（累計）

**舉例說明**：
→ 如果你選「過去 7 天」：顯示這 7 天的總收入
→ 如果你選「過去 30 天」：顯示這 30 天的總收入
→ 如果你選「過去 90 天」：顯示這 90 天的總收入

**為什麼有用？**
快速了解不同時間段的實際營收表現，方便做同期比較。
''',
        'strong_growth': '✅ **成長很猛** — MRR 漲了',
        'continue_invest': '策略有效，繼續加碼',
        'growth_slowing': '⚠️ **成長在放慢** — MRR 只漲了',
        'need_attention': '該注意了，可能要調整策略',
        'growth_stalled': '🚨 **幾乎沒在長** — MRR 才漲',
        'take_action': '紅燈了，得馬上動手',
        'key_health': '💊 兩個最關鍵的數字（決定你公司還能活多久）',
        'churn_rate': '客戶流失率 — 白話就是：有多少人不玩了？',
        'churn_help': '我先給你 benchmark：\n\n✅ **< 3% = 健康**\n   → 100 個客戶最多流失 3 個，這很正常\n\n⚠️ **> 5% = 警戒**\n   → 開始會拖累成長，得處理了\n\n💸 **商業上的意思**：\n   流失率 3% = 每個月流失 3% 的收入\n\n你可能會問：為什麼這麼重要？\n→ 因為獲得新客戶的成本 >> 留住舊客戶\n→ 流失率高，就算拉新客戶也是在補洞',
        'unit_economics': '單位經濟 — 白話就是：每個客戶能賺多少？',
        'ltv_cac_help': '我先講人話版本：\n\n**花 $100 拉一個客戶，這個客戶總共會付你多少錢？**\n\n✅ **至少要 $300（賺 3 倍）**\n   → 這才叫健康的單位經濟\n\n⚠️ **低於 $100 = 虧錢**\n   → 每拉一個客戶就在虧，越成長虧越多\n\n🎯 **判斷標準很簡單**：\n   • 3x 以上 = 可以放心加大獲客預算\n   • 1-3x = 還可以，但要優化\n   • < 1x = 別再燒錢了，先解決這個\n\n就像開早餐店，一個客戶來一次花 $100，你得賺回至少 $300 才划算。',
        'current_mrr': '💵 MRR — 白話就是：這個月固定會收多少錢？',
        'current_mrr_help': 'MRR = Monthly Recurring Revenue（月經常性收入）\n\n我先說為什麼這個數字重要：\n\n✅ **可預測**\n   → 就像健身房會員制，你知道下個月會有多少錢進來\n\n✅ **可追蹤**\n   → 每天看這個數字，馬上知道生意在長還是在縮\n\n✅ **可成長**\n   → 每多一個付費客戶，MRR 就往上\n\n**商業上的意思**：\n如果所有付費客戶都不取消，下個月你會收到多少錢。\n\n這個數字越穩定、越高 = 你的生意越健康。',

        'mrr_calculation': '''**💰 MRR 是怎麼算出來的？**

🧮 **公式很簡單**：
```
MRR = 所有活躍訂閱的月費加總
```

**舉例說明**：
• 20 人訂閱 Basic 方案（$9.99/月）= $199.80
• 10 人訂閱 Pro 方案（$19.99/月）= $199.90
• 5 人訂閱 Premium 方案（$49.99/月）= $249.95
→ **總 MRR = $649.65**

**如果是年費怎麼算？**
→ 年費 $120 ÷ 12 = 月費 $10
→ 都轉成「每月」來算

**📈 現在的戰況**：
{mrr_status}

**🎯 這個數字告訴你**：
→ MRR 往上 = 生意在長 ✅
→ MRR 持平 = 新客戶剛好抵銷流失 ⚠️
→ MRR 往下 = 流失太快，紅燈 🚨
''',

        'churn_calculation': '''**📉 流失率是怎麼算出來的？**

🧮 **公式**：
```
流失率 = (本期取消訂閱的客戶數 ÷ 期初總客戶數) × 100%
```

**💡 用你的實際數據計算（過去 {period_days} 天）**：

**步驟 1**：定義計算期間
→ 開始日期：{start_date}
→ 結束日期：{end_date}
→ 計算期間：{period_days} 天

**步驟 2**：計算期初的活躍訂閱數
→ 查詢條件：`subscription_start <= {start_date}` 且 (`subscription_end` 是 NULL 或 `> {start_date}`)
→ 期初活躍訂閱數 = **{active_start_count:,} 個**

**步驟 3**：計算期間內取消的訂閱數
→ 查詢條件：`subscription_end >= {start_date}` 且 `<= {end_date}`
→ 取消訂閱數 = **{churned_count:,} 個**

**步驟 4**：計算流失率
→ 流失率 = {churned_count:,} ÷ {active_start_count:,} × 100% = **{churn_rate:.2f}%**

**💸 商業上的意思**：
流失率 {churn_rate:.2f}% = 每 {period_days} 天流失 {churn_rate:.2f}% 的客戶
→ 如果是月流失率，一年下來會流失約 {churn_rate * 12:.1f}% 的收入（單利估算）
→ 這就是為什麼流失率這麼致命

**📊 現在的戰況**：
{churn_status}

**🎯 這個數字告訴你**：
→ < 3% = 健康，產品有黏性 ✅
→ 3-5% = 還可以，但要注意 ⚠️
→ > 5% = 危險，得馬上處理 🚨

**為什麼流失率這麼重要？**
→ 獲得新客戶的成本 = 留住舊客戶的 5-10 倍
→ 流失率高 = 就算拉新客戶也是在補洞
''',

        'ltv_cac_calculation': '''**💰 LTV:CAC 是怎麼算出來的？**

🧮 **公式**：
```
LTV (客戶終身價值) = ARPU × 平均訂閱月數
CAC (獲客成本) = 總獲客支出 ÷ 新客戶數
LTV:CAC = LTV ÷ CAC
```

**舉例說明**：
• ARPU = $30/月
• 平均客戶訂閱 20 個月
→ **LTV = $30 × 20 = $600**

• 這個月花 $5,000 拉客戶（廣告、推薦獎勵等）
• 新增 50 個付費客戶
→ **CAC = $5,000 ÷ 50 = $100**

→ **LTV:CAC = $600 ÷ $100 = 6x**

**📊 現在的戰況**：
{ltv_cac_status}

**🎯 判斷標準**：
→ > 3x = 健康，可以加大獲客預算 ✅
→ 1-3x = 還可以，但要優化 ⚠️
→ < 1x = 虧錢，別再燒錢了 🚨

**商業上的意思**：
花 $100 拉一個客戶，這個客戶總共會付你 $600
→ 賺 6 倍，這個生意很健康
''',

        'arpu_calculation': '''**💵 ARPU 是怎麼算出來的？**

🧮 **公式很簡單**：
```
ARPU = 總 MRR ÷ 付費客戶數
```

**舉例說明**：
• 總 MRR = $5,000
• 付費客戶 = 100 人
→ **ARPU = $5,000 ÷ 100 = $50/人**

**📊 現在的戰況**：
{arpu_status}

**🎯 這個數字告訴你**：
→ ARPU 往上 = 客戶願意付更多錢 ✅
→ ARPU 持平 = OK，但有優化空間 ⚠️
→ ARPU 往下 = 客戶在降級或用便宜方案 🚨

**為什麼 ARPU 重要？**
提升 ARPU = 不用多找客戶也能長收入

就像咖啡店：
• 方案 A: 找更多客人進店（很累）
• 方案 B: 讓每個客人多買一杯（更容易）

**怎麼提升 ARPU**：
→ 推出 Premium 方案
→ 增加 add-on 功能
→ 漲價（如果產品夠好）
''',

        'conversion_calculation': '''**🎯 轉換率是怎麼算出來的？**

🧮 **公式**：
```
轉換率 = (付費客戶數 ÷ 總註冊用戶數) × 100%
```

**舉例說明**：
• 總共 1,000 人註冊
• 其中 200 人付費訂閱
→ **轉換率 = (200 ÷ 1,000) × 100% = 20%**

**📊 現在的戰況**：
{conversion_status}

**🎯 判斷標準**：
→ > 20% = 很健康，產品價值明確 ✅
→ 10-20% = 還可以，有優化空間 ⚠️
→ < 10% = 有問題，得檢討 🚨

**商業上的意思**：
轉換率每提升 1% = 多 1% 的人付錢
→ 這比拉新客戶便宜太多了

**為什麼轉換率低？**（通常是這三個原因）
→ 看不到價值（產品體驗不夠好）
→ 價格太貴（定價有問題）
→ 免費版太好用（沒有付費動機）
''',

        'mau_calculation': '''**👥 MAU 是怎麼算出來的？**

🧮 **定義**：
```
MAU = 過去 30 天內至少登入過一次的用戶數
```

**舉例說明**：
• 你有 1,000 個註冊用戶
• 過去 30 天內，600 人有登入使用
→ **MAU = 600**
→ **活躍率 = 60%**

**📊 現在的戰況**：
{mau_status}

**🎯 這個數字告訴你**：
→ MAU 往上 = 產品有黏性，用戶會回來 ✅
→ MAU 持平 = OK，但要注意留存 ⚠️
→ MAU 往下 = 產品在流失用戶 🚨

就像健身房：
• 辦卡的人很多（註冊用戶）
• 但真正在用的人才是 MAU
• MAU 越高 = 產品價值越高

**商業判斷**：
→ MAU 持續成長 = 產品 working
→ MAU 下降 = 該檢討產品體驗了
''',

        # === Funnel Tab Explanations ===
        'retention_rate_calc': '''**📊 首次到第二次掃描留存率 — 怎麼算的？**

🧮 **公式**：
```
留存率 = (第二次掃描用戶數 ÷ 首次掃描用戶數) × 100%
```

**💡 用你的實際數據計算**：

**步驟 1**：找出「至少掃描過 1 次」的用戶
→ 有 **{users_first_scan:,}** 人掃描過履歷（從 `scans` 表的 `user_id` 去重計算）

**步驟 2**：找出「掃描過 2 次以上」的用戶
→ 有 **{users_second_scan:,}** 人回來第二次掃描（從 `scans` 表 `groupby user_id` 後篩選 `count > 1` 的用戶）

**步驟 3**：計算留存率
→ 留存率 = {users_second_scan:,} ÷ {users_first_scan:,} × 100% = **{retention_rate:.1f}%**

**步驟 4**：計算流失用戶數
→ 流失用戶 = {users_first_scan:,} - {users_second_scan:,} = **{users_lost:,} 人**
→ 流失率 = {users_lost:,} ÷ {users_first_scan:,} × 100% = **{lost_percentage:.1f}%**

**📊 現在的戰況**：
{retention_status}

**💰 商業上的意思**：
這是產品「黏性」的第一道檢驗

→ **< 30% = 🚨 紅燈**
  產品首次體驗沒讓用戶看到價值
  → 70% 的人用一次就走了

→ **30-50% = ⚠️ 還可以**
  一半人會回來，一半不會
  → 有優化空間

→ **> 50% = ✅ 健康**
  大部分人會繼續用
  → 產品有黏性

**🎯 Jerry 的決策建議**：
如果留存率 < 30%：
→ **馬上行動**：優化首次掃描結果的呈現方式
→ **為什麼**：用戶第一次用就沒看到價值，當然不會再來
→ **怎麼做**：讓 AI 分析更精準、結果更具體、建議更可行

就像你去一家新餐廳：
• 第一次吃覺得普通 → 不會再去
• 第一次吃覺得很棒 → 會帶朋友來
''',

        'match_rate_calc': '''**🎯 平均匹配率 — 怎麼算的？**

🧮 **定義**：
```
平均匹配率 = 所有掃描的平均匹配分數
```

**舉例說明**：
• 用戶 A 掃描履歷，AI 給 85 分
• 用戶 B 掃描履歷，AI 給 65 分
• 用戶 C 掃描履歷，AI 給 72 分
→ **平均匹配率 = (85 + 65 + 72) ÷ 3 = 74%**

**📊 現在的戰況**：
當前平均匹配率：{match_rate:.1f}%

**💰 商業上的意思**：
這個數字直接決定用戶會不會付費

→ **> 75% = ✅ 很好**
  AI 分析夠精準，用戶會覺得有價值

→ **60-75% = ⚠️ 還可以**
  有改進空間，但不至於太差

→ **< 60% = 🚨 有問題**
  AI 判斷不準，用戶會流失

**🎯 Jerry 的決策建議**：
匹配率不是越高越好，關鍵是「準確」

→ **如果匹配率太高（> 85%）**：
  可能 AI 太寬鬆，用戶會懷疑可信度

→ **如果匹配率太低（< 65%）**：
  AI 太嚴格，用戶會失望離開

**最佳範圍：70-80%**
→ 用戶覺得「這個 AI 夠嚴謹」
→ 同時也看到「我有機會改進」

**實際行動**：
檢查匹配率低於 60 分的案例
→ 是 AI 判斷錯了？還是用戶履歷真的不適合？
→ 如果是 AI 錯了，優化算法
→ 如果是履歷問題，提供更具體的改進建議
''',

        'overall_conversion_calc': '''**🎯 總轉換率 — 怎麼算的？**

🧮 **公式**：
```
總轉換率 = (付費用戶數 ÷ 註冊用戶數) × 100%
```

**舉例說明**：
• 1,000 人註冊
• 200 人付費訂閱
→ **總轉換率 = 200 ÷ 1,000 × 100% = 20%**

**📊 現在的戰況**：
當前總轉換率：{conversion_rate:.1f}%

**💰 商業上的意思**：
這是你賺錢的核心指標

→ **> 20% = 🚀 非常健康**
  產品價值很明確，用戶願意買單
  → 每 5 個註冊就有 1 個付費

→ **10-20% = ✅ 健康**
  還不錯，但有優化空間
  → 每 10 個註冊有 1-2 個付費

→ **5-10% = ⚠️ 需要注意**
  大部分用戶不願意付費
  → 可能是價格、價值、或體驗問題

→ **< 5% = 🚨 紅燈**
  產品吸引力不足
  → 馬上檢討產品定位

**🎯 Jerry 的決策建議**：

**如果轉換率 < 10%，問三個問題**：

1️⃣ **用戶看得到價值嗎？**
   → 免費版體驗夠好嗎？
   → 付費版的差異夠明顯嗎？

2️⃣ **價格合理嗎？**
   → 跟競品比是貴還是便宜？
   → 用戶付得起嗎？

3️⃣ **購買流程順暢嗎？**
   → 付款步驟會不會太複雜？
   → 有沒有提供試用期？

**提升轉換率的三個槓桿**：
→ 提升產品價值（讓免費版更好用）
→ 降低付費門檻（提供試用、分期付款）
→ 優化轉換流程（減少步驟、增加信任感）

🧮 **為什麼轉換率提升很重要？**

**數學邏輯（用你的實際數據）**：
• 當前轉換率：{conversion_rate:.1f}%
• 假設有 1,000 個新用戶註冊
• 當前會轉換：1,000 × {conversion_rate:.1f}% = {current_converts:.0f} 人

**如果轉換率提升 1 個百分點（{conversion_rate:.1f}% → {new_conversion_rate:.1f}%）**：
• 新轉換人數：1,000 × {new_conversion_rate:.1f}% = {new_converts:.0f} 人
• 多出來的付費用戶：{new_converts:.0f} - {current_converts:.0f} = **{additional_converts:.0f} 人**

**用你的實際 ARPU = ${arpu:.2f}**：
• 額外收入 = {additional_converts:.0f} 人 × ${arpu:.2f} = **${additional_revenue:.0f}**
• 相對增長 = {additional_converts:.0f} ÷ {current_converts:.0f} × 100% = **{relative_growth:.1f}%**

→ 在你當前 {conversion_rate:.1f}% 的轉換率下，提升 1 個百分點 = 收入增長 ~{relative_growth:.0f}%
→ 比拉新客戶便宜太多了（獲客成本 = $0，只需優化體驗）
''',
        'total_revenue': '📊 **總收入**',
        'actions_this_week': '🎯 本週該做什麼？（按優先級排）',
        'high_priority': '🔴 馬上處理',
        'medium_priority': '🟡 這週搞定',
        'maintain_status': '🟢 繼續保持',
        'action': '**行動**',
        'reason': '為什麼',
        'next_step': '💡 下一步',
        'reduce_churn': '止血：降低流失率',
        'improve_economics': '優化：改善單位經濟',
        'accelerate_growth': '加速：推高收入成長',
        'metrics_excellent': '維持：指標都很健康',
        'view_anomalies': '🚨 查看異常警報（點擊展開）',
        'anomaly_help': '系統自動檢測指標異常｜可設定每日掃描 + Email/Slack 通知',
        'revenue_trend': 'MRR 持續強勁成長',
        'strategy_working': '成長策略奏效',
        'stable_growth': 'MRR 穩定成長',
        'maintain_pace': '維持當前節奏',
        'growth_slowed': 'MRR 成長放緩至',
        'need_new_engine': '需要新的成長引擎',
        'supporting_metrics': '#### 其他重要數字',
        'arpu': 'ARPU — 白話就是：每個客戶平均付多少錢？',
        'arpu_help': 'ARPU = Average Revenue Per User\n\n🧮 **怎麼算**：總收入 ÷ 付費客戶數\n\n💡 **舉例**：\n   100 個客戶付了 $5,000 → ARPU = $50/人\n\n📈 **為什麼這個數字重要**：\n\n提升 ARPU = 不用多找客戶也能長收入\n\n就像你在開咖啡店：\n• Option 1: 找更多客人進店（很累）\n• Option 2: 讓每個客人多買一點（更容易）\n\n**怎麼提升 ARPU**：\n   → 推出 Premium 方案\n   → 增加 add-on 功能\n   → 漲價（如果產品夠好）\n\n🎯 **目標**：ARPU 要持續往上',
        'conversion_rate': '轉換率 — 白話就是：100 個試用的，幾個願意付錢？',
        'conversion_help': '轉換率 = 免費用戶轉成付費用戶的比例\n\n🧮 **怎麼算**：付費客戶 ÷ 總註冊數 × 100\n\n💡 **舉例**：\n   • 1000 人註冊\n   • 200 人付費\n   • 轉換率 = 20%\n\n我先給你 benchmark：\n\n✅ **20% 以上 = 很健康**\n   → 產品價值很明確，用戶願意買單\n\n⚠️ **10-20% = 還可以**\n   → 有機會優化，空間不小\n\n🚨 **< 10% = 有問題**\n   → 產品吸引力不足，或定價/價值呈現有問題\n\n**商業上的意思**：\n轉換率每提升 1%，就是多 1% 的人付錢\n→ 這比拉新客戶便宜太多了\n\n你可能會問：怎麼提升？\n→ 先搞清楚為什麼 80% 的人不付費\n→ 通常是：看不到價值 or 價格太貴 or 體驗太差',
        'mau': 'MAU — 白話就是：每個月有多少人在用？',
        'mau_help': 'MAU = Monthly Active Users（月活躍用戶）\n\n📊 **怎麼算**：30 天內至少用過一次的人數\n\n💡 **為什麼這個數字重要**：\n\nMAU 往上 = 產品有黏性，用戶會回來\nMAU 下滑 = 產品在流失用戶，紅燈\n\n就像健身房：\n• 辦卡的人很多（註冊用戶）\n• 但真正在用的人才是 MAU\n• MAU 越高 = 產品價值越高\n\n**商業判斷**：\n   → MAU 持續成長 = 產品 working\n   → MAU 下降 = 該檢討產品體驗了\n\n🎯 **健康標準**：MAU 要穩定向上',
        'metric_definitions': '📖 指標定義與計算邏輯',

        # Funnel Tab
        # Funnel Tab - Critical Alerts
        'critical_alert': '🚨 關鍵警報',
        'churn_warning': '流失率警戒',
        'churn_at_warning': '當前流失率',
        'churn_impact': '影響分析',
        'churn_impact_text': '流失率已達到警戒水平，可能會影響未來的轉換表現和用戶留存。建議立即採取干預措施。',
        'immediate_action': '立即行動',
        'retention_analysis': '📊 留存率深度分析',
        'first_to_second_scan': '首次掃描 → 第二次掃描留存率',
        'retention_rate': '留存率',
        'users_returned': '回訪用戶',
        'users_lost': '流失用戶',
        'retention_insight': '洞察分析',
        'match_rate_analysis': '😕 誰對產品不滿意？為什麼他們會走？',
        'below_avg_match': '掃描結果不準確的用戶',
        'avg_match_rate': '履歷掃描準確率（整體平均）',
        'below_avg_users': '體驗不佳的用戶人數',
        'behavior_pattern': '商業影響',
        'match_rate_explanation': '**什麼是「匹配率」？**\n\n我先講人話版本：\n→ 就是我們的 AI 掃描履歷準不準\n\n分數越高 = AI 給的建議越精準、越實用\n分數低 = 用戶會覺得「這什麼爛東西」然後離開\n\n**商業上的意思**：\n這個分數直接影響用戶會不會繼續用、會不會付費',
        'optimization_suggestions': '💡 優化建議方案',
        'improve_onboarding_title': '1. 優化首次使用引導',
        'improve_onboarding_desc': '提供更清晰的引導流程，降低新用戶使用門檻',
        'improve_algorithm_title': '2. 改善匹配算法準確度',
        'improve_algorithm_desc': '提升履歷匹配準確性，增加用戶信任度',
        'show_value_title': '3. 增強免費版價值展示',
        'show_value_desc': '讓用戶在免費階段就能體驗到明確價值',
        'conversion_performance': '🎯 轉換率表現',
        'conversion_excellent': '✅ **轉換表現優異** — 從',
        'signups_to_paid': '註冊轉換出',
        'paid_users': '付費用戶',
        'conversion_fair': '⚠️ **轉換尚可** — 仍有提升空間，目標 >20%',
        'conversion_poor': '🚨 **轉換不佳** — 產品價值傳遞需加強',
        'revenue_potential': '💰 收入潛力',
        'per_1pct_improve': '每提升 1% 轉換',
        'potential_help': '估算每月額外收入',
        'conversion_value': '💡 優化轉換漏斗的商業價值',
        'biggest_bottleneck': '⚠️ 最大瓶頸',
        'stage_losing': '階段流失',
        'people': '人',
        'action_recommendation': '💡 建議行動',
        'problem': '**問題**',
        'action_plan': '**行動方案**',
        'expected_impact': '**預期影響**',
        'users_not_using': '用戶註冊後不使用產品',
        'users_try_once': '用戶嘗試一次就離開',
        'see_value_no_pay': '看到價值但不願付費',
        'best_segment': '轉換率最高',
        'focus_acquisition': '應集中獲客資源',
        'focus_firepower': '**集中火力**',
        'user_group': '用戶群',
        'action_increase': '行動: 提升此群體廣告預算 2-3x',
        'stop_waste': '**停止浪費**',
        'action_pause': '行動: 暫停此群體投放，重新評估產品適配性',
        'segments_similar': '所有區隔轉換率差距不大，可廣泛投放',

        # Channel Analysis
        'channel_roi_high': 'ROI',
        'expand_budget': '應立即擴大預算 3-5x',
        'losing_channel': '虧錢渠道，建議暫停',
        'best_performer': '表現最佳',
        'priority_channel': '優先投放',
        'channel_budget': '🎯 渠道預算建議',
        'scale_now': '🚀 立即加碼',
        'stop_now': '🛑 立即暫停',
        'maintain_current': '⚖️ 維持現狀',
        'profitable': '綠色 = 賺錢',
        'losing': '紅色 = 虧錢',
        'breakeven': '黃線 = 打平',

        # Common
        'excellent': '優秀',
        'normal': '正常',
        'needs_improve': '需改進',
        'target': '目標',
        'help': '幫助',
        'channel': '渠道',

        # Recommendations (Chinese)
        'view_details': '📊 查看詳情',
        'diagnosis': '**診斷**',
        'plain_language': '**白話**',
        'business_loss': '**商業損失**',
        'business_problem': '**問題**',
        'business_advantage': '**優勢**',
        'immediate_action': '**立即行動**',
        'two_paths': '**兩條路**',
        'growth_formula': '**成長公式**',
        'next_steps': '**下一步**',
        'why_important': '**為什麼重要**',
        'customers_leaving': '每個月有',
        'customers': '個客戶離開',
        'monthly_revenue_loss': '損失',
        'per_month': '/月收入',
        'spend_1_dollar': '花 $1 獲客，只賺回',
        'not_worth_it': '不夠划算',
        'customer_acquisition_expensive': '獲客太貴或客戶付費太少',
        'growth_too_slow': '成長太慢，距離 10% 目標差',
        'investor_concern': '投資人會質疑、難以融資',
        'company_healthy': '公司健康，可以繼續當前策略',
        'suitable_for_scale': '適合開始規模化投資',
        'consequence': '**後果**',

        # Anomaly Section
        'view_anomalies_title': '🚨 查看異常警報（點擊展開）',
        'anomaly_detection_info': '系統自動檢測指標異常｜可設定每日掃描 + Email/Slack 通知',
        'all_systems_normal': '所有系統正常',
        'no_anomalies': '未檢測到嚴重異常',

        # Revenue Trend
        'past_90_days': '過去 90 天趨勢 | 向上 = 健康成長 | 持平 = 需要關注',

        # Metric Definitions
        'metric_defs_title': '### 關鍵指標定義',
        'mrr_definition': '**MRR (Monthly Recurring Revenue)**',
        'mrr_def_desc': '**定義**: 每月可預期的經常性收入總和',
        'mrr_calculation': '**計算**: 所有活躍訂閱的月費加總',
        'mrr_importance': '**為什麼重要**: 衡量業務規模與可預測性的核心指標',
        'mrr_benchmark': '**健康基準**: 月成長率 >10% 為優秀',
        'churn_definition': '**流失率 (Churn Rate)**',
        'churn_def_desc': '**定義**: 在特定期間內取消訂閱的用戶百分比',
        'churn_calculation': '**計算**: (期間內流失用戶數 / 期初總用戶數) × 100%',
        'churn_importance': '**為什麼重要**: 直接影響收入增長和客戶終身價值',
        'churn_benchmark': '**健康基準**: <3% 為優秀，>5% 需立即改善',
        'ltv_cac_definition': '**LTV:CAC 比率**',
        'ltv_cac_def_desc': '**定義**: 客戶終身價值與獲客成本的比率',
        'ltv_cac_calculation': '**計算**: (平均客戶終身收入) / (平均獲客成本)',
        'ltv_cac_importance': '**為什麼重要**: 衡量單位經濟效益，決定成長可持續性',
        'ltv_cac_benchmark': '**健康基準**: >3x 為健康，<1x 表示每獲得一個客戶就虧錢',
        'arpu_definition': '**ARPU (Average Revenue Per User)**',
        'arpu_def_desc': '**定義**: 每位用戶的平均收入貢獻',
        'arpu_calculation': '**計算**: 總收入 / 總用戶數',
        'arpu_importance': '**為什麼重要**: 提升 ARPU 比增加用戶更容易擴展',
        'arpu_improve': '**如何改善**: 升級方案、追加銷售、價值包裝',
        'conversion_definition': '**轉換率 (Conversion Rate)**',
        'conversion_def_desc': '**定義**: 免費用戶轉為付費用戶的比例',
        'conversion_calculation': '**計算**: (付費用戶數 / 總註冊用戶數) × 100%',
        'conversion_importance': '**為什麼重要**: 決定獲客投資的回報效率',
        'conversion_benchmark': '**健康基準**: >20% 為優秀，<10% 需優化產品價值呈現',
        'data_update_freq': '**數據更新頻率**: 實時（每次刷新時重新計算）',
        'data_src': '**數據來源**: 模擬數據，用於示範',
        'data_owner': '**責任人**: 產品分析團隊',

        # Funnel Tab - Bottleneck Section
        'users_not_activating': '用戶註冊後不使用產品',
        'optimize_onboarding': '優化新手引導流程',
        'send_activation': '發送啟動郵件/推播',
        'lower_first_use': '降低首次使用門檻',
        'show_value_cases': '展示產品價值案例',
        'improve_activation': '每提升 10% 啟動率 =',
        'more_paid_users': '付費用戶',
        'users_leave_after_once': '用戶嘗試一次就離開',
        'analyze_satisfaction': '分析首次體驗滿意度',
        'increase_value': '增加產品價值點',
        'provide_incentives': '提供持續使用誘因',
        'improve_core_exp': '改善核心功能體驗',
        'improve_stickiness': '提升黏性可直接轉換更多付費',
        'see_value_no_pay': '看到價值但不願付費',
        'optimize_pricing': '優化定價策略',
        'limited_offer': '提供限時優惠',
        'strengthen_value': '強化付費價值呈現',
        'lower_payment_barrier': '降低付費門檻',
        'improve_willingness': '每提升 5% 付費意願 =',

        # Funnel Tab - Channel Performance
        'most_profitable_channel': '🏆 最賺錢的渠道（ROI）',
        'roi_label': 'ROI',
        'action_plan_roi': '💰 行動方案',
        'increase_budget': '立刻增加',
        'budget_multiplier': '預算 2-3 倍，ROI 這麼高說明還有成長空間',
        'healthiest_channel': '🏆 最健康的渠道（LTV:CAC）',
        'action_plan_ltv': '這個渠道的用戶終身價值最高，優先服務好這些客戶',
        'step_three': '### 第三步：完整數據表 - 所有渠道的健康檢查',
        'how_to_read': '**💡 如何解讀這張表？（從左到右）**',
        'total_users_desc': '**total_users**: 這個渠道帶來多少人？（量）',
        'conversions_desc': '**conversions**: 有多少人付費？（質）',
        'conversion_rate_desc': '**conversion_rate**: 轉換率 = conversions ÷ total_users（效率）',
        'cac_desc': '**avg_cac**: 平均獲客成本（成本）',
        'ltv_desc': '**avg_ltv**: 平均客戶終身價值（收益）',
        'ltv_cac_desc': '**ltv_cac_ratio**: 收益倍數 = LTV ÷ CAC（健康度，> 3x 才OK）',
        'roi_desc': '**roi**: 投資報酬率 = (LTV - CAC) ÷ CAC × 100%（賺不賺錢）',
        'mrr_desc': '**total_mrr**: 這個渠道貢獻的月收入（貢獻度）',
        'decision_logic': '**🎯 決策邏輯（按優先順序）**',
        'cut': '**砍掉**',
        'roi_negative': 'ROI < 100% 的渠道（賠錢）',
        'observe': '**觀察**',
        'ltv_cac_warning': 'LTV:CAC < 3x 的渠道（不健康）',
        'maintain': '**維持**',
        'ltv_cac_stable': 'LTV:CAC 3-10x 的渠道（穩定）',
        'scale_up': '**加碼**',
        'ltv_cac_excellent': 'LTV:CAC > 10x 且 ROI > 500% 的渠道（金礦！）',
        'channel_ltv_title': '各渠道 LTV:CAC 比率（越高越賺）',
        'ltv_cac_multiple': 'LTV:CAC 倍數',
        'healthy_threshold': '✅ 健康門檻 (3x)',
        'danger_line': '⚠️ 危險線 (1x)',
        'color_guide_ltv': '🟢 綠色 = 優秀 (>5x) ｜ 🟡 黃色 = 尚可 (3-5x) ｜ 🟠 橘色 = 警告 (1-3x) ｜ 🔴 紅色 = 危險 (<1x)',
        'channel_roi_title': '各渠道投資報酬率 ROI',
        'roi_pct': 'ROI (%)',
        'color_guide_roi': '👆 數字越大 = 賺越多｜< 100% = 賠錢',
        'channel_text': '渠道',
        'roi_over_300': 'ROI > 300% 表示花 $1 賺回 $3+',
        'action_scale': '**行動**: 提升預算至當前 3-5 倍',
        'roi_under_100': 'ROI < 100% = 每花 $1 虧錢',
        'action_stop': '**行動**: 暫停投放或大幅優化',
        'roi_100_300': 'ROI 100-300% = 有賺但空間有限',
        'action_optimize': '**行動**: 持續優化，尋找成長空間',

        # Cohort Tab
        'cohort_title': '👥 同期群留存分析 — 白話就是：用戶會不會一直用？',
        'cohort_what': '### 📖 這個頁面在看什麼？',
        'cohort_desc': '**Cohort Analysis（同期群分析）**\n\n我先講人話版本：\n→ 追蹤「同一時間註冊的用戶」在之後幾個月還剩多少人\n\n就像健身房：\n• 1 月辦卡 100 人\n• 2 月還在用的有 70 人（70% 留存）\n• 3 月還在用的有 50 人（50% 留存）\n\n**商業上的意思**：\n這個數字告訴你產品有沒有黏性、用戶會不會一直用',
        'cohort_why': '**為什麼這個重要？**',
        'cohort_reason1': '看產品「黏不黏」— 用戶會一直用 or 用完就丟？',
        'cohort_reason2': '找「黃金留存曲線」— 第 1 個月留存 75% = 健康，< 40% = 產品有問題',
        'cohort_reason3': '預測未來 — 這批用戶 3 個月後還剩多少人？',
        'cohort_value': '**商業價值在哪**',
        'cohort_value1': '💰 **留存率每提升 5% = LTV 增加 20%+**',
        'cohort_value2': '🎯 **第 1 個月留存率是最重要的數字**\n\n我先給你 benchmark：\n• > 70% = 產品很黏，繼續做\n• 40-70% = 還可以，有優化空間\n• < 40% = 產品有問題，得重新設計\n\n為什麼第 1 個月這麼重要？\n→ 用戶在第一次體驗就決定要不要繼續用\n→ 第 1 個月流失 = 後面再也拉不回來',
        'cohort_heatmap': '🔥 留存熱力圖 - 顏色越深 = 留存越好',
        'cohort_axis': '👇 橫軸 = 註冊後幾個月｜縱軸 = 哪個月註冊的用戶',
        'cohort_chart_title': '各同期群用戶留存率 (%)',
        'retention_pct': '留存率 %',
        'months_after': '註冊後經過幾個月',
        'cohort_month': '註冊月份（同期群）',
        'month_n': '第',
        'month_unit': '個月',
        'how_to_read_heatmap': '**🔍 如何解讀熱力圖？**',
        'month_0_desc': '**第 0 個月（最左邊）**: 一定是 100%（所有人都剛註冊）',
        'month_1_desc': '**第 1 個月**: 最關鍵！> 70% 優秀，40-70% 正常，< 40% 危險',
        'month_3_desc': '**第 3 個月**: 穩定期指標，> 50% 表示產品有長期價值',
        'color_deeper': '**顏色越深藍**: 留存率越高，產品越黏',
        'color_lighter': '**顏色越淺**: 用戶流失嚴重',
        'key_retention': '📌 關鍵留存指標',
        'avg_month_1': '平均第 1 個月留存率',
        'most_important': '💡 最重要！> 70% 優秀',
        'product_sticky': '✅ 產品黏性優秀！',
        'can_improve': '⚠️ 還可以，但有進步空間',
        'retention_alert': '🚨 警報！留存率過低',
        'avg_month_3': '平均第 3 個月留存率',
        'long_term_value': '💡 長期價值指標',
        'user_ltv': '✅ 用戶有長期價值',
        'churn_too_fast': '⚠️ 用戶流失太快',
        'latest_cohort': '最新一批用戶數',
        'new_users_month': '💡 這個月新增多少人',
        'action_based_retention': '🎯 基於當前留存率的行動建議',
        'month_1_retention': '**第 1 個月留存',
        'if_over_70': '如果 > 70%: 產品很黏，加大獲客預算',
        'if_40_70': '如果 40-70%: 優化新手引導和首次體驗',
        'if_under_40': '如果 < 40%: 產品核心價值有問題，需要重新設計',
        'business_impact': '**💰 商業影響**',
        'retention_lift_value': '第 1 個月留存每提升 10% = LTV 增加約 $100-200/用戶',

        # AI Tab
        'ai_title': '🤖 AI 數據助手 — 用白話問，AI 用白話答',
        'ai_unavailable': '⚠️ AI 查詢功能目前無法使用',
        'ai_enable': '啟用方法：',
        'ai_step1': '1. 到 https://console.anthropic.com 取得 API 金鑰',
        'ai_step2': '2. 將金鑰加入 .env 檔案：ANTHROPIC_API_KEY=your_key_here',
        'ai_step3': '3. 重新啟動儀表板',
        'ai_what': '### 📖 這是幹嘛的？',
        'ai_desc': '**AI 數據助手**\n\n我先說為什麼你需要這個：\n→ 不用懂 SQL、不用寫程式\n→ 直接用白話問問題\n→ AI 會分析數據然後用人話回答\n\n就像有個數據分析師隨時在旁邊待命。',
        'ai_why': '**為什麼這個有用？**',
        'ai_reason1': '你不用等資料團隊，自己就能找答案',
        'ai_reason2': 'AI 會把所有數據結合起來給你洞察',
        'ai_reason3': '會自動給你行動建議，不只是數字',
        'ai_value': '**商業價值**',
        'ai_value1': '💰 **省下 80% 的數據查詢時間** — 不用等人',
        'ai_value2': '🎯 **數據民主化** — 任何人都能自己找答案',
        'try_questions': '**💬 試試這些問題（中英文都可以）**',
        'q1': '我們的流失率多少？該擔心嗎？',
        'q2': 'MRR 在長還是在掉？',
        'q3': '哪個獲客渠道 ROI 最高？應該加碼哪個？',
        'q4': '為什麼轉換率這麼低？卡在哪個步驟？',
        'q5': '推薦渠道 vs 付費廣告，哪個比較划算？',
        'q6': '免費→付費轉換率有沒有在掉？問題在哪？',
        'q7': '哪個用戶群 LTV 最高？我們該 focus 誰？',
        'auto_insights': '✨ 自動生成商業洞察',
        'auto_insights_desc': '👇 AI 會自動分析你的數據，找出 3-5 個最重要的洞察',
        'generate_insights': '🔄 生成最新洞察',
        'ai_analyzing': 'AI 正在分析你的數據...',
        'insight_label': '洞察',
        'insight_text': '**洞察**',
        'business_impact_label': '**商業影響**',
        'recommended_actions': '**建議行動**',
        'unexpected_format': '意外的洞察格式',
        'unexpected_response': 'AI 回傳了意外的格式。原始回應:',
        'insight_error': '生成洞察時發生錯誤',
        'unknown_error': '未知錯誤',
        'ask_ai': '💬 問 AI 問題',
        'ask_ai_desc': '👇 用白話文問，AI 會用白話文答',
        'your_question': '你的問題:',
        'question_placeholder': '例如: 什麼在影響我們的流失率？',
        'ask_ai_button': '🤖 問 AI 助手',
        'ai_thinking': 'AI 思考中...',
        'ai_answer': '### 💡 AI 的回答:',
        'metrics_used': '📊 AI 參考的指標',
        'related_anomalies': '⚠️ 相關異常',
        'enter_question': '請先輸入問題',
        'metric_explainer': '📖 指標解釋器',
        'metric_explainer_desc': '👇 不懂某個指標？讓 AI 用白話解釋給你聽',
        'select_metric': '選擇一個指標來深入了解:',
        'explain_button': '🔍 解釋這個指標',
        'ai_generating': 'AI 正在生成解釋...',
        'ai_explanation': '### 📚 AI 的解釋:',
        'error_label': '錯誤',
        'metric_mrr': 'MRR（月經常性收入）',
        'metric_arpu': 'ARPU（平均客單價）',
        'metric_churn': 'Churn Rate（流失率）',
        'metric_conversion': '轉換率',
        'metric_ltv': 'LTV（客戶終身價值）',
        'metric_cac': 'CAC（獲客成本）',
        'metric_ltv_cac': 'LTV:CAC 比率',

        # Sidebar Health Check
        'health_quick': '🏥 健康快檢',
        'mrr_strong': '🟢 MRR 成長強勁',
        'mrr_stable': '🟡 MRR 穩定成長',
        'mrr_slow': '🔴 MRR 成長緩慢',
        'churn_excellent_status': '🟢 流失率優秀',
        'churn_normal_status': '🟡 流失率正常',
        'churn_high_status': '🔴 流失率過高',
    },

    'en': {
        # Header
        'data_status': '📊 Data Status',
        'real_time_update': '✅ Real-time',
        'update_time': 'Updated at',
        'refresh_data': '🔄 Refresh Data',
        'refresh_help': 'Reload latest data',

        # Sidebar
        'control_panel': '⚙️ Control Panel',
        'quick_actions': '⚡ Quick Actions',
        'export_report': '📥 Export Report',
        'export_help': 'Export current data as CSV',
        'export_dev': 'Export feature in development...',
        'email_report': '📧 Email Report',
        'email_help': 'Send report to your email',
        'email_dev': 'Email feature in development...',
        'data_filter': '🎛️ Data Filters',
        'time_range': 'Time Range',
        'time_range_help': 'Select time range to view',
        'all_data': 'All Data',
        'last_7_days': 'Last 7 Days',
        'last_30_days': 'Last 30 Days',
        'last_90_days': 'Last 90 Days',
        'last_year': 'Last Year',
        'health_check': '🏥 Health Check',
        'mrr_growth_strong': '🟢 Strong MRR Growth',
        'mrr_growth_stable': '🟡 Stable MRR Growth',
        'mrr_growth_slow': '🔴 Slow MRR Growth',
        'churn_excellent': '🟢 Excellent Churn Rate',
        'churn_normal': '🟡 Normal Churn Rate',
        'churn_high': '🔴 High Churn Rate',
        'basic_stats': '📊 Basic Statistics',
        'total_users': 'Total Users',
        'total_users_help': 'Total registered users',
        'active_subs': 'Active Subscriptions',
        'active_subs_help': 'Current paying subscriptions',
        'total_scans': 'Total Scans',
        'total_scans_help': 'Total resume scans by all users',
        'about_dashboard': 'ℹ️ About Dashboard',
        'features': '**Features**',
        'feature_1': '🎯 Real-time SaaS Metrics',
        'feature_2': '📈 Smart Anomaly Detection',
        'feature_3': '🤖 AI Data Assistant',
        'feature_4': '🔔 Auto Alert System',
        'data_source': '**Data Source**: Simulated Data',
        'update_freq': '**Update Frequency**: Real-time',
        'tip': '💡 **Tip**: Use the refresh button at top to update cache',

        # Tabs
        'tab_overview': '📊 Overview',
        'tab_funnel': '🎯 Conversion Funnel',
        'tab_cohort': '👥 Cohort Analysis',
        'tab_ai': '🤖 AI Assistant',

        # Overview Tab
        # Project Context Note Pad (STAR + 5W1H)
        'project_context_note': '''
## 🤔 **If You Can't Answer These 4 Questions in 30 Seconds, You Need This Dashboard**

---

### 🎯 **SITUATION (Context)**

**WHO** uses this product?
→ **JobMetrics Pro** users — job seekers using AI resume scanning to optimize resumes

**WHAT** type of business is this?
→ **SaaS Subscription Model** — users sign up → free trial scans → paid subscription

**WHERE** does the data come from?
→ From 4 core data tables: `users` (signups), `scans` (behavior), `subscriptions` (status), `revenue` (financials)

**WHEN** is this business stage?
→ **Growth Phase** — 10,000 users, 2,500+ paid subscriptions, $92K+ monthly revenue

---

### 🚨 **TASK (Challenge)**

**WHY** do we need this dashboard?
→ **Decision Paralysis**: Data exists but scattered across tables, can't quickly answer critical questions:
  • 💰 Is revenue growing or declining?
  • 📉 Why are users churning?
  • 🎯 Which funnel stage has the lowest conversion?
  • 💡 What should we optimize next?

**Goal**: Build a "self-service analytics dashboard" enabling decision-makers to find answers and take action in **30 seconds**

---

### ⚙️ **ACTION (Solution)**

**HOW** did we solve it?
1. **📊 Data Integration** — Combined 4 tables into key SaaS metrics (MRR, churn, LTV, conversion, etc.)
2. **🎨 Visual Design** — Used funnels, trends, comparison cards to make complex data instantly clear
3. **🤖 AI Insights** — Built-in AI Query engine for natural language questions with data-driven recommendations
4. **🧮 Jerry-Style Explanations** — Every number includes "how it's calculated" and "why it matters"

**Core Modules**:
→ **Overview** — Understand business health in 3 seconds
→ **Funnel** — Identify conversion bottlenecks
→ **Revenue** — Track revenue trends and anomalies
→ **AI Insights** — Ask questions in plain English, get actionable recommendations

---

### 🎉 **RESULT (Impact)**

**What can this dashboard do for you?**

✅ **Fast Decisions** — Understand core metrics in 30 seconds, no SQL or BI tools needed
✅ **Find Bottlenecks** — Funnel analysis pinpoints exactly "where users drop off"
✅ **Data-Driven** — Every recommendation based on real calculations, not guesswork
✅ **Action-Oriented** — Tells you not just "what happened" but "what to do about it"

**💡 Design Philosophy**:
→ **Jerry Style** = The "why" behind numbers matters more than numbers themselves
→ **Self-Service** = Non-technical users can explore data independently
→ **Decision-Driven** = Every chart answers a specific business question

---

**📌 Usage Tips**:
1. Start with **Overview** to grasp overall health
2. Check **Funnel** to find conversion bottlenecks
3. Use **AI Insights** to ask "what should I optimize?"
''',

        'revenue_status': '💰 Monthly Revenue Status',
        'strong_growth': '✅ **Strong Growth**: MRR increased by',
        'continue_invest': 'Continue investing in growth',
        'growth_slowing': '⚠️ **Growth Slowing**: MRR increased by',
        'need_attention': 'Needs attention',
        'growth_stalled': '🚨 **Growth Stalled**: MRR only increased by',
        'take_action': 'Take immediate action',
        'key_health': '💊 Company Health Check (These two numbers determine survival)',
        'churn_rate': 'How many customers stopped paying?',
        'churn_help': '📉 Out of 100 paying customers, how many canceled this month?\n\n💸 Business Impact: 3% churn = losing 3% revenue monthly\n\n✅ Healthy Target: < 3% (max 3 out of 100 customers leave)\n⚠️ Warning: > 5% (starts hurting growth)',
        'unit_economics': 'How much money can you make from each customer?',
        'ltv_cac_help': '💰 Plain English: Spend $100 to get a customer, how much will they pay you total?\n\n✅ Healthy Target: At least $300 (earn 3x back)\n⚠️ Warning: < $100 (losing money)\n\n🎯 Goal: For every $1 spent on acquisition, earn at least $3 back',
        'current_mrr': '💵 How much will all customers pay us this month?',
        'current_mrr_help': '🔄 MRR = Monthly Recurring Revenue = Predictable monthly income\n\n💡 Plain English: If all paying customers don\'t cancel, how much money comes in next month?\n\n📈 Why it matters:\n• Predictable: Know how much money is coming\n• Scalable: Each new customer increases MRR\n• Trackable: See growth or decline daily',
        'total_revenue': '📊 **Total Revenue**',
        'actions_this_week': '🎯 Actions for This Week',
        'high_priority': '🔴 High Priority',
        'medium_priority': '🟡 Medium Priority',
        'maintain_status': '🟢 Maintain Status',
        'action': '**Action**',
        'reason': 'Reason',
        'next_step': '💡 Next Step',
        'reduce_churn': 'Reduce Churn Rate',
        'improve_economics': 'Improve Unit Economics',
        'accelerate_growth': 'Accelerate Revenue Growth',
        'metrics_excellent': 'Metrics Performing Well',
        'view_anomalies': '🚨 View Anomaly Alerts (Click to Expand)',
        'anomaly_help': 'Auto-detect anomalies | Daily scan + Email/Slack alerts available',
        'revenue_trend': 'Strong MRR Growth Continues',
        'strategy_working': 'Growth strategy working',
        'stable_growth': 'Stable MRR Growth',
        'maintain_pace': 'Maintain current pace',
        'growth_slowed': 'MRR Growth Slowed to',
        'need_new_engine': 'Need new growth engine',
        'supporting_metrics': '#### Supporting Metrics',
        'arpu': 'How much does each customer pay monthly on average?',
        'arpu_help': '💰 ARPU = Average Revenue Per User\n\n🧮 Calculation: Total monthly revenue ÷ Number of paying customers\n\n💡 Example:\n• 100 customers paid $5,000\n• ARPU = $50/person\n\n📈 Why it matters:\n• Increase ARPU = More revenue without finding new customers\n• Methods: Launch premium tiers, add-on features\n\n🎯 Goal: Continuously increase (through product upgrades, value-added services)',
        'conversion_rate': 'Out of 100 free users, how many will pay?',
        'conversion_help': '🔄 Conversion Rate = Free to paid conversion\n\n🧮 Calculation: (Paid users ÷ Total signups) × 100\n\n💡 Example:\n• 1,000 people signed up\n• 200 became paying customers\n• Conversion rate = 20%\n\n📈 Why it matters:\n• Higher conversion = Better product-market fit\n• More efficient = Less acquisition cost per customer\n\n🎯 Healthy Target: > 20% (1 in 5 converts)',
        'mau': 'How many people use our product monthly?',
        'mau_help': '👥 MAU = Monthly Active Users = People who used the product this month\n\n💡 What counts as "active": Performed at least one resume scan\n\n📈 Why it matters:\n• More users = More conversion opportunities\n• Retention indicator = Are users coming back?\n• Growth metric = Is the product gaining traction?\n\n🎯 Goal: Steady increase + high retention rate',
        'metric_definitions': '📖 Metric Definitions & Calculation Logic',

        # Funnel Tab - Critical Alerts
        'critical_alert': '🚨 Critical Alert',
        'churn_warning': 'Churn Rate Warning',
        'churn_at_warning': 'Current Churn Rate',
        'churn_impact': 'Impact Analysis',
        'churn_impact_text': 'Churn rate has reached warning level, which may impact future conversion performance and user retention. Immediate intervention recommended.',
        'immediate_action': 'Immediate Action Required',
        'retention_analysis': '📊 Deep Retention Analysis',
        'first_to_second_scan': 'First Scan → Second Scan Retention',
        'retention_rate': 'Retention Rate',
        'users_returned': 'Users Returned',
        'users_lost': 'Users Lost',
        'retention_insight': 'Insight Analysis',
        'match_rate_analysis': '😕 Who\'s Unhappy? Why Are They Leaving?',
        'below_avg_match': 'Users Getting Inaccurate Scan Results',
        'avg_match_rate': 'Resume Scan Accuracy (Overall Average)',
        'below_avg_users': 'Users Having Poor Experience',
        'behavior_pattern': 'Business Impact',
        'match_rate_explanation': '**What is "Match Rate"?** Simply put, it\'s how accurate our AI resume scanning is. Higher scores mean the AI gives more precise and useful recommendations.',
        'optimization_suggestions': '💡 Optimization Recommendations',
        'improve_onboarding_title': '1. Improve First-Time User Onboarding',
        'improve_onboarding_desc': 'Provide clearer guidance to reduce friction for new users',
        'improve_algorithm_title': '2. Enhance Match Algorithm Accuracy',
        'improve_algorithm_desc': 'Improve resume matching accuracy to build user trust',
        'show_value_title': '3. Strengthen Free Tier Value Proposition',
        'show_value_desc': 'Let users experience clear value during free trial',
        # Funnel Tab
        'conversion_performance': '🎯 Conversion Performance',
        'conversion_excellent': '✅ **Excellent Conversion** — From',
        'signups_to_paid': 'signups converted to',
        'paid_users': 'paid users',
        'conversion_fair': '⚠️ **Fair Conversion** — Room for improvement, target >20%',
        'conversion_poor': '🚨 **Poor Conversion** — Need to improve value proposition',
        'revenue_potential': '💰 Revenue Potential',
        'per_1pct_improve': 'Per 1% Improvement',
        'potential_help': 'Estimated monthly revenue gain',
        'conversion_value': '💡 Value of optimizing conversion funnel',
        'biggest_bottleneck': '⚠️ Biggest Bottleneck',
        'stage_losing': 'stage losing',
        'people': 'users',
        'action_recommendation': '💡 Recommended Actions',
        'problem': '**Problem**',
        'action_plan': '**Action Plan**',
        'expected_impact': '**Expected Impact**',
        'users_not_using': 'Users not using product after signup',
        'users_try_once': 'Users trying once then leaving',
        'see_value_no_pay': 'Users see value but won\'t pay',
        'best_segment': 'Highest Conversion',
        'focus_acquisition': 'Focus acquisition here',
        'focus_firepower': '**Focus Resources**',
        'user_group': 'User Group',
        'action_increase': 'Action: Increase ad budget for this segment 2-3x',
        'stop_waste': '**Stop Wasting**',
        'action_pause': 'Action: Pause this segment, reassess product-market fit',
        'segments_similar': 'All segments have similar conversion, can target broadly',

        # Channel Analysis
        'channel_roi_high': 'ROI',
        'expand_budget': 'Scale budget 3-5x immediately',
        'losing_channel': 'Losing money, recommend pause',
        'best_performer': 'Best Performer',
        'priority_channel': 'Priority Channel',
        'channel_budget': '🎯 Channel Budget Recommendations',
        'scale_now': '🚀 Scale Now',
        'stop_now': '🛑 Stop Now',
        'maintain_current': '⚖️ Maintain',
        'profitable': 'Green = Profitable',
        'losing': 'Red = Losing',
        'breakeven': 'Yellow = Break-even',

        # Common
        'excellent': 'Excellent',
        'normal': 'Normal',
        'needs_improve': 'Needs Improvement',
        'target': 'Target',
        'help': 'Help',
        'channel': 'Channel',

        # Recommendations (English)
        'view_details': '📊 View Details',
        'diagnosis': '**Diagnosis**',
        'plain_language': '**In Plain Terms**',
        'business_loss': '**Business Loss**',
        'business_problem': '**Problem**',
        'business_advantage': '**Advantage**',
        'immediate_action': '**Immediate Action**',
        'two_paths': '**Two Paths**',
        'growth_formula': '**Growth Formula**',
        'next_steps': '**Next Steps**',
        'why_important': '**Why It Matters**',
        'customers_leaving': 'Every month',
        'customers': 'customers leave',
        'monthly_revenue_loss': 'Losing',
        'per_month': '/month in revenue',
        'spend_1_dollar': 'Spend $1 to acquire, only get back',
        'not_worth_it': 'not worth it',
        'customer_acquisition_expensive': 'CAC too high or customer value too low',
        'growth_too_slow': 'Growth too slow, missing 10% target by',
        'investor_concern': 'Investors will question, hard to fundraise',
        'company_healthy': 'Company is healthy, continue current strategy',
        'suitable_for_scale': 'Good time to scale investment',
        'consequence': '**Consequence**',

        # Anomaly Section
        'view_anomalies_title': '🚨 View Anomaly Alerts (Click to Expand)',
        'anomaly_detection_info': 'Auto-detect anomalies | Daily scan + Email/Slack alerts available',
        'all_systems_normal': 'All systems normal',
        'no_anomalies': 'No critical anomalies detected',

        # Revenue Trend
        'past_90_days': 'Past 90 days trend | Up = healthy growth | Flat = needs attention',

        # Metric Definitions
        'metric_defs_title': '### Key Metric Definitions',
        'mrr_definition': '**MRR (Monthly Recurring Revenue)**',
        'mrr_def_desc': '**Definition**: Total predictable monthly recurring revenue',
        'mrr_calculation': '**Calculation**: Sum of all active subscription monthly fees',
        'mrr_importance': '**Why Important**: Core metric for measuring business scale and predictability',
        'mrr_benchmark': '**Healthy Benchmark**: >10% monthly growth is excellent',
        'churn_definition': '**Churn Rate**',
        'churn_def_desc': '**Definition**: Percentage of users who cancel subscription in a period',
        'churn_calculation': '**Calculation**: (Users lost in period / Total users at start) × 100%',
        'churn_importance': '**Why Important**: Directly impacts revenue growth and customer lifetime value',
        'churn_benchmark': '**Healthy Benchmark**: <3% is excellent, >5% needs immediate improvement',
        'ltv_cac_definition': '**LTV:CAC Ratio**',
        'ltv_cac_def_desc': '**Definition**: Ratio of customer lifetime value to acquisition cost',
        'ltv_cac_calculation': '**Calculation**: (Average customer lifetime revenue) / (Average acquisition cost)',
        'ltv_cac_importance': '**Why Important**: Measures unit economics and growth sustainability',
        'ltv_cac_benchmark': '**Healthy Benchmark**: >3x is healthy, <1x means losing money on each customer',
        'arpu_definition': '**ARPU (Average Revenue Per User)**',
        'arpu_def_desc': '**Definition**: Average revenue contribution per user',
        'arpu_calculation': '**Calculation**: Total revenue / Total users',
        'arpu_importance': '**Why Important**: Easier to scale by increasing ARPU than adding users',
        'arpu_improve': '**How to Improve**: Upgrade plans, upsells, value packaging',
        'conversion_definition': '**Conversion Rate**',
        'conversion_def_desc': '**Definition**: Percentage of free users converting to paid',
        'conversion_calculation': '**Calculation**: (Paid users / Total registered users) × 100%',
        'conversion_importance': '**Why Important**: Determines ROI of acquisition investment',
        'conversion_benchmark': '**Healthy Benchmark**: >20% is excellent, <10% needs value prop optimization',
        'data_update_freq': '**Data Update Frequency**: Real-time (recalculated on each refresh)',
        'data_src': '**Data Source**: Simulated data for demo purposes',
        'data_owner': '**Owner**: Product Analytics Team',

        # Funnel Tab - Bottleneck Section
        'users_not_activating': 'Users not using product after signup',
        'optimize_onboarding': 'Optimize onboarding flow',
        'send_activation': 'Send activation emails/push notifications',
        'lower_first_use': 'Lower first-use barriers',
        'show_value_cases': 'Show product value examples',
        'improve_activation': 'Every 10% activation improvement =',
        'more_paid_users': 'paid users',
        'users_leave_after_once': 'Users try once then leave',
        'analyze_satisfaction': 'Analyze first-time satisfaction',
        'increase_value': 'Add more value points',
        'provide_incentives': 'Provide continued usage incentives',
        'improve_core_exp': 'Improve core feature experience',
        'improve_stickiness': 'Improving stickiness can directly convert more paid users',
        'see_value_no_pay': 'Users see value but won\'t pay',
        'optimize_pricing': 'Optimize pricing strategy',
        'limited_offer': 'Offer limited-time deals',
        'strengthen_value': 'Strengthen paid value proposition',
        'lower_payment_barrier': 'Lower payment barriers',
        'improve_willingness': 'Every 5% willingness improvement =',

        # Funnel Tab - Channel Performance
        'most_profitable_channel': '🏆 Most Profitable Channel (ROI)',
        'roi_label': 'ROI',
        'action_plan_roi': '💰 Action Plan',
        'increase_budget': 'Immediately increase',
        'budget_multiplier': 'budget 2-3x, such high ROI indicates growth headroom',
        'healthiest_channel': '🏆 Healthiest Channel (LTV:CAC)',
        'action_plan_ltv': 'This channel has highest user LTV, prioritize serving these customers',
        'step_three': '### Step 3: Complete Data Table - Health Check for All Channels',
        'how_to_read': '**💡 How to Read This Table? (Left to Right)**',
        'total_users_desc': '**total_users**: How many people does this channel bring? (Volume)',
        'conversions_desc': '**conversions**: How many people paid? (Quality)',
        'conversion_rate_desc': '**conversion_rate**: Conversion = conversions ÷ total_users (Efficiency)',
        'cac_desc': '**avg_cac**: Average customer acquisition cost (Cost)',
        'ltv_desc': '**avg_ltv**: Average customer lifetime value (Revenue)',
        'ltv_cac_desc': '**ltv_cac_ratio**: Revenue multiple = LTV ÷ CAC (Health, > 3x is OK)',
        'roi_desc': '**roi**: Return on investment = (LTV - CAC) ÷ CAC × 100% (Profitability)',
        'mrr_desc': '**total_mrr**: Monthly revenue from this channel (Contribution)',
        'decision_logic': '**🎯 Decision Logic (By Priority)**',
        'cut': '**Cut**',
        'roi_negative': 'Channels with ROI < 100% (Losing money)',
        'observe': '**Watch**',
        'ltv_cac_warning': 'Channels with LTV:CAC < 3x (Unhealthy)',
        'maintain': '**Maintain**',
        'ltv_cac_stable': 'Channels with LTV:CAC 3-10x (Stable)',
        'scale_up': '**Scale Up**',
        'ltv_cac_excellent': 'Channels with LTV:CAC > 10x and ROI > 500% (Gold mine!)',
        'channel_ltv_title': 'LTV:CAC Ratio by Channel (Higher = More Profitable)',
        'ltv_cac_multiple': 'LTV:CAC Multiple',
        'healthy_threshold': '✅ Healthy Threshold (3x)',
        'danger_line': '⚠️ Danger Line (1x)',
        'color_guide_ltv': '🟢 Green = Excellent (>5x) | 🟡 Yellow = OK (3-5x) | 🟠 Orange = Warning (1-3x) | 🔴 Red = Danger (<1x)',
        'channel_roi_title': 'ROI by Channel',
        'roi_pct': 'ROI (%)',
        'color_guide_roi': '👆 Higher = More Profit | < 100% = Losing Money',
        'channel_text': 'Channel',
        'roi_over_300': 'ROI > 300% means spend $1 earn back $3+',
        'action_scale': '**Action**: Scale budget to 3-5x current',
        'roi_under_100': 'ROI < 100% = Losing $1 for every $1 spent',
        'action_stop': '**Action**: Pause or heavily optimize',
        'roi_100_300': 'ROI 100-300% = Profitable but limited upside',
        'action_optimize': '**Action**: Continue optimizing, find growth opportunities',

        # Cohort Tab
        'cohort_title': '👥 Cohort Retention Analysis - Do Users Keep Using?',
        'cohort_what': '### 📖 What is This Page About?',
        'cohort_desc': '**Cohort Analysis** - Track retention rates for users who signed up at the same time over subsequent months.',
        'cohort_why': '**Why Important?**',
        'cohort_reason1': 'See if product is "sticky": Do users keep using it or abandon it?',
        'cohort_reason2': 'Find the "golden retention curve": Month 1 retention of 75% = healthy, < 40% = product issues',
        'cohort_reason3': 'Predict future: How many users will remain after 3 months?',
        'cohort_value': '**Business Value**',
        'cohort_value1': '💰 **Every 5% retention increase = 20%+ LTV increase**',
        'cohort_value2': '🎯 **Month 1 retention is the most critical metric** - Determines product survival',
        'cohort_heatmap': '🔥 Retention Heatmap - Darker = Better Retention',
        'cohort_axis': '👇 X-axis = Months after signup | Y-axis = Cohort signup month',
        'cohort_chart_title': 'User Retention by Cohort (%)',
        'retention_pct': 'Retention %',
        'months_after': 'Months After Signup',
        'cohort_month': 'Signup Month (Cohort)',
        'month_n': 'Month',
        'month_unit': '',
        'how_to_read_heatmap': '**🔍 How to Read the Heatmap?**',
        'month_0_desc': '**Month 0 (Leftmost)**: Always 100% (everyone just signed up)',
        'month_1_desc': '**Month 1**: Most critical! > 70% excellent, 40-70% normal, < 40% danger',
        'month_3_desc': '**Month 3**: Stability indicator, > 50% shows long-term product value',
        'color_deeper': '**Darker blue**: Higher retention, stickier product',
        'color_lighter': '**Lighter**: Severe user churn',
        'key_retention': '📌 Key Retention Metrics',
        'avg_month_1': 'Average Month 1 Retention',
        'most_important': '💡 Most important! > 70% excellent',
        'product_sticky': '✅ Excellent product stickiness!',
        'can_improve': '⚠️ OK, but room for improvement',
        'retention_alert': '🚨 Alert! Retention rate too low',
        'avg_month_3': 'Average Month 3 Retention',
        'long_term_value': '💡 Long-term value indicator',
        'user_ltv': '✅ Users have long-term value',
        'churn_too_fast': '⚠️ Users churning too fast',
        'latest_cohort': 'Latest Cohort Size',
        'new_users_month': '💡 New users this month',
        'action_based_retention': '🎯 Action Recommendations Based on Current Retention',
        'month_1_retention': '**Month 1 Retention',
        'if_over_70': 'If > 70%: Product is sticky, increase acquisition budget',
        'if_40_70': 'If 40-70%: Optimize onboarding and first-time experience',
        'if_under_40': 'If < 40%: Core product value issue, needs redesign',
        'business_impact': '**💰 Business Impact**',
        'retention_lift_value': 'Every 10% Month 1 retention increase = ~$100-200/user LTV increase',

        # AI Tab
        'ai_title': '🤖 AI Data Assistant - Ask Data in Plain English',
        'ai_unavailable': '⚠️ AI Query Feature Currently Unavailable',
        'ai_enable': 'To Enable:',
        'ai_step1': '1. Get API key at https://console.anthropic.com',
        'ai_step2': '2. Add key to .env file: ANTHROPIC_API_KEY=your_key_here',
        'ai_step3': '3. Restart dashboard',
        'ai_what': '### 📖 What Does This Page Do?',
        'ai_desc': '**AI Data Assistant** - Ask data questions in plain language, AI analyzes and answers in plain terms.',
        'ai_why': '**Why Important?**',
        'ai_reason1': 'No need for SQL or coding, just ask questions',
        'ai_reason2': 'AI combines all data to give insights',
        'ai_reason3': 'Auto-generate action recommendations',
        'ai_value': '**Business Value**',
        'ai_value1': '💰 **Reduce 80% of data query time** - No waiting for data team',
        'ai_value2': '🎯 **Democratize data** - Anyone can find answers',
        'try_questions': '**💬 Try These Questions (English or Chinese)**',
        'q1': 'What is our churn rate? Should I worry?',
        'q2': 'How is MRR trending?',
        'q3': 'Which acquisition channel has highest ROI?',
        'q4': 'Why is conversion rate so low?',
        'q5': 'Referrals vs paid ads, which is better value?',
        'q6': 'Is our free-to-paid conversion rate declining? Which step is the bottleneck?',
        'q7': 'Which user segment (job seeker / career switcher / university students) contributes the most LTV? Which should we prioritize?',
        'auto_insights': '✨ Auto-Generated Business Insights',
        'auto_insights_desc': '👇 AI will analyze your data and find 3-5 most important insights',
        'generate_insights': '🔄 Generate Latest Insights',
        'ai_analyzing': 'AI is analyzing your data...',
        'insight_label': 'Insight',
        'insight_text': '**Insight**',
        'business_impact_label': '**Business Impact**',
        'recommended_actions': '**Recommended Actions**',
        'unexpected_format': 'Unexpected insight format',
        'unexpected_response': 'AI returned unexpected format. Raw response:',
        'insight_error': 'Error generating insights',
        'unknown_error': 'Unknown error',
        'ask_ai': '💬 Ask AI a Question',
        'ask_ai_desc': '👇 Ask in plain language, AI answers in plain language',
        'your_question': 'Your Question:',
        'question_placeholder': 'e.g., What is affecting our churn rate?',
        'ask_ai_button': '🤖 Ask AI Assistant',
        'ai_thinking': 'AI is thinking...',
        'ai_answer': '### 💡 AI\'s Answer:',
        'metrics_used': '📊 Metrics AI Referenced',
        'related_anomalies': '⚠️ Related Anomalies',
        'enter_question': 'Please enter a question first',
        'metric_explainer': '📖 Metric Explainer',
        'metric_explainer_desc': '👇 Don\'t understand a metric? Let AI explain in plain terms',
        'select_metric': 'Select a metric to learn more:',
        'explain_button': '🔍 Explain This Metric',
        'ai_generating': 'AI is generating explanation...',
        'ai_explanation': '### 📚 AI\'s Explanation:',
        'error_label': 'Error',
        'metric_mrr': 'MRR (Monthly Recurring Revenue)',
        'metric_arpu': 'ARPU (Average Revenue Per User)',
        'metric_churn': 'Churn Rate',
        'metric_conversion': 'Conversion Rate',
        'metric_ltv': 'LTV (Lifetime Value)',
        'metric_cac': 'CAC (Customer Acquisition Cost)',
        'metric_ltv_cac': 'LTV:CAC Ratio',

        # Sidebar Health Check
        'health_quick': '🏥 Quick Health Check',
        'mrr_strong': '🟢 Strong MRR Growth',
        'mrr_stable': '🟡 Stable MRR Growth',
        'mrr_slow': '🔴 Slow MRR Growth',
        'churn_excellent_status': '🟢 Excellent Churn Rate',
        'churn_normal_status': '🟡 Normal Churn Rate',
        'churn_high_status': '🔴 High Churn Rate',
    }
}

def get_text(key, lang='zh'):
    """Get translated text by key and language"""
    return LANGUAGES.get(lang, LANGUAGES['zh']).get(key, key)
