# 每日異常自動檢測 - 設定指南

## ✅ 已完成功能

你現在擁有一個**真正的每日自動掃描系統**！

### 系統包含：

1. **`daily_anomaly_checker.py`** - 核心檢測腳本
   - 自動執行異常檢測
   - 發送 Email/Slack 通知
   - 儲存異常歷史記錄（data/anomaly_history.json）

2. **通知系統**
   - 📧 Email 通知（HTML 格式）
   - 💬 Slack 通知（Webhook）
   - 📝 JSON 歷史記錄（保留 90 天）

3. **配置系統**
   - 所有設定都透過 `.env` 檔案或環境變數

---

## 🚀 快速開始

### 步驟 1: 測試腳本

先手動執行一次，確認功能正常：

```bash
cd "/Users/jerrylaivivemachi/DS PROJECT/self-help databboard"
python daily_anomaly_checker.py
```

你應該會看到類似這樣的輸出：

```
============================================================
🔍 開始每日異常掃描 - 2025-01-27 10:00:00
============================================================

📝 異常記錄已儲存到: /path/to/data/anomaly_history.json
⚠️  發現 2 個異常：

🚨 【危急異常】需要立即處理：
   - Churn Rate: 流失率 (8.50%) exceeds critical threshold
     當前值: 8.50%

⚠️  【警告異常】需要注意：
   - Conversion Rate: 轉換率 (1.80%) below warning threshold
     當前值: 1.80%

📧 準備發送通知...
   ℹ️  郵件通知未啟用（在 config.py 設定 EMAIL_NOTIFICATIONS_ENABLED）
   ℹ️  Slack 通知未設定（在 .env 加入 SLACK_WEBHOOK_URL）

============================================================
✅ 異常掃描完成
============================================================
```

---

### 步驟 2: 設定通知（選擇性）

#### A. Email 通知

在 `.env` 檔案加入以下設定：

```bash
# Email Notifications
EMAIL_NOTIFICATIONS_ENABLED=true
EMAIL_FROM=alerts@yourcompany.com
EMAIL_TO=your.email@gmail.com

# SMTP Settings (Gmail 範例)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=your_app_password  # 使用 Gmail App Password
```

**Gmail App Password 取得方式**：
1. 到 Google Account: https://myaccount.google.com/security
2. 開啟「兩步驟驗證」
3. 搜尋「App passwords」
4. 建立一個給「Mail」用的密碼
5. 複製密碼到 `.env`

#### B. Slack 通知

1. 建立 Slack Incoming Webhook：
   - 到 https://api.slack.com/apps
   - 建立新 App
   - 啟用 "Incoming Webhooks"
   - 選擇要發送的 channel
   - 複製 Webhook URL

2. 在 `.env` 加入：

```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

---

### 步驟 3: 設定每日自動執行

#### 選項 A: macOS/Linux cron (推薦)

1. 打開 crontab 編輯器：
```bash
crontab -e
```

2. 加入以下行（每天早上 9:00 執行）：
```cron
0 9 * * * cd "/Users/jerrylaivivemachi/DS PROJECT/self-help databboard" && /usr/bin/python3 daily_anomaly_checker.py >> /tmp/anomaly_checker.log 2>&1
```

**其他時間範例**：
- 每天早上 8:00: `0 8 * * *`
- 每天中午 12:00: `0 12 * * *`
- 每小時: `0 * * * *`
- 每 6 小時: `0 */6 * * *`

3. 驗證 cron job：
```bash
crontab -l
```

4. 檢查 log：
```bash
tail -f /tmp/anomaly_checker.log
```

#### 選項 B: macOS launchd（更可靠）

1. 創建 plist 檔案：
```bash
nano ~/Library/LaunchAgents/com.jobmetrics.anomaly-checker.plist
```

2. 加入以下內容：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jobmetrics.anomaly-checker</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/jerrylaivivemachi/DS PROJECT/self-help databboard/daily_anomaly_checker.py</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>/tmp/anomaly_checker.log</string>

    <key>StandardErrorPath</key>
    <string>/tmp/anomaly_checker_error.log</string>

    <key>WorkingDirectory</key>
    <string>/Users/jerrylaivivemachi/DS PROJECT/self-help databboard</string>
</dict>
</plist>
```

3. 載入並啟動：
```bash
launchctl load ~/Library/LaunchAgents/com.jobmetrics.anomaly-checker.plist
```

4. 檢查狀態：
```bash
launchctl list | grep anomaly
```

5. 手動測試執行：
```bash
launchctl start com.jobmetrics.anomaly-checker
```

#### 選項 C: 簡單排程腳本（開發用）

創建一個 Python 排程腳本 `run_scheduler.py`：

```python
import schedule
import time
from daily_anomaly_checker import DailyAnomalyChecker

def job():
    checker = DailyAnomalyChecker()
    checker.run_check()

# 每天早上 9:00 執行
schedule.every().day.at("09:00").do(job)

print("📅 排程已啟動！每天早上 9:00 會執行異常檢測")
print("按 Ctrl+C 停止")

while True:
    schedule.run_pending()
    time.sleep(60)
```

然後在背景執行：
```bash
nohup python run_scheduler.py &
```

---

## 📊 查看異常歷史

異常記錄會自動儲存到：
```
data/anomaly_history.json
```

格式範例：
```json
[
  {
    "timestamp": "2025-01-27T09:00:00",
    "total_anomalies": 2,
    "critical_count": 1,
    "warning_count": 1,
    "anomalies": [
      {
        "metric": "Churn Rate",
        "value": "8.50%",
        "severity": "critical",
        "message": "流失率 (8.50%) exceeds critical threshold"
      }
    ]
  }
]
```

你可以用 Python 分析：
```python
import json

with open('data/anomaly_history.json') as f:
    history = json.load(f)

# 顯示最近 7 天的異常趨勢
recent = history[-7:]
for record in recent:
    print(f"{record['timestamp']}: {record['total_anomalies']} 個異常")
```

---

## 🔧 進階設定

### 客製化閾值

在 `src/core/config.py` 調整：

```python
THRESHOLDS = {
    "churn_rate": {"warning": 0.05, "critical": 0.08},
    "conversion_rate": {"warning": 0.02, "critical": 0.01},
    "avg_match_rate": {"warning": 0.65, "critical": 0.60},
    "mrr_growth": {"warning": -0.05, "critical": -0.10},
}
```

### 客製化通知訊息

編輯 `daily_anomaly_checker.py` 中的：
- `_generate_email_html()` - Email 樣式
- `_generate_slack_message()` - Slack 訊息格式

---

## 🎯 確認運作

### 手動測試
```bash
python daily_anomaly_checker.py
```

### 檢查 log
```bash
# cron log
tail -f /tmp/anomaly_checker.log

# launchd log
tail -f /tmp/anomaly_checker.log
tail -f /tmp/anomaly_checker_error.log
```

### 檢查異常記錄
```bash
cat data/anomaly_history.json | python -m json.tool
```

---

## ❓ 常見問題

### Q: 為什麼沒收到通知？

A: 檢查：
1. `.env` 檔案設定是否正確
2. Gmail 是否啟用了 App Password
3. Slack Webhook URL 是否有效
4. 手動執行 `python daily_anomaly_checker.py` 看錯誤訊息

### Q: cron job 沒有執行？

A: 檢查：
1. `crontab -l` 確認設定
2. 檢查 log: `tail -f /tmp/anomaly_checker.log`
3. 確認 Python 路徑: `which python3`
4. 測試手動執行是否成功

### Q: 如何停止自動掃描？

A:
```bash
# 停止 cron
crontab -e  # 刪除或註解掉該行

# 停止 launchd
launchctl unload ~/Library/LaunchAgents/com.jobmetrics.anomaly-checker.plist
```

---

## 📝 最後一步：更新 Dashboard 說明

現在你可以驕傲地說：

> ✅ **「系統每天早上 9:00 自動掃描，有問題會發通知！」**

這是**真的**！🎉
