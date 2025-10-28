"""
每日異常自動檢測腳本
Daily Anomaly Detection Scheduler

此腳本會：
1. 每天自動執行異常檢測
2. 發送郵件/Slack 通知
3. 記錄異常歷史到 JSON 檔案
"""
import sys
from pathlib import Path
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 將專案目錄加入 Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.analytics import SaaSAnalytics
from src.core import config


class DailyAnomalyChecker:
    """每日異常檢測器"""

    def __init__(self):
        self.analytics = SaaSAnalytics()
        self.log_file = project_root / 'data' / 'anomaly_history.json'
        self.log_file.parent.mkdir(exist_ok=True)

    def run_check(self):
        """執行異常檢測"""
        print(f"\n{'='*60}")
        print(f"🔍 開始每日異常掃描 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        # 執行異常檢測
        anomalies = self.analytics.detect_anomalies()

        # 準備報告
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_anomalies': len(anomalies),
            'critical_count': len([a for a in anomalies if a['severity'] == 'critical']),
            'warning_count': len([a for a in anomalies if a['severity'] == 'warning']),
            'anomalies': anomalies
        }

        # 儲存到歷史記錄
        self._save_to_history(report)

        # 顯示結果
        self._print_report(report)

        # 發送通知（如果有異常）
        if anomalies:
            self._send_notifications(report)

        print(f"\n{'='*60}")
        print(f"✅ 異常掃描完成")
        print(f"{'='*60}\n")

        return report

    def _save_to_history(self, report):
        """儲存異常記錄到 JSON 檔案"""
        history = []

        # 讀取現有記錄
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except:
                history = []

        # 加入新記錄
        history.append(report)

        # 只保留最近 90 天的記錄
        history = history[-90:]

        # 寫回檔案
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

        print(f"📝 異常記錄已儲存到: {self.log_file}")

    def _print_report(self, report):
        """印出報告到終端機"""
        anomalies = report['anomalies']

        if not anomalies:
            print("✅ 太好了！所有指標都正常，沒有發現異常")
            return

        print(f"⚠️  發現 {len(anomalies)} 個異常：\n")

        # 先顯示 critical
        critical = [a for a in anomalies if a['severity'] == 'critical']
        if critical:
            print("🚨 【危急異常】需要立即處理：")
            for a in critical:
                print(f"   - {a['metric']}: {a['message']}")
                print(f"     當前值: {a['value']}\n")

        # 再顯示 warning
        warnings = [a for a in anomalies if a['severity'] == 'warning']
        if warnings:
            print("⚠️  【警告異常】需要注意：")
            for a in warnings:
                print(f"   - {a['metric']}: {a['message']}")
                print(f"     當前值: {a['value']}\n")

    def _send_notifications(self, report):
        """發送通知"""
        print("\n📧 準備發送通知...")

        # Email 通知
        if config.EMAIL_NOTIFICATIONS_ENABLED:
            self._send_email(report)
        else:
            print("   ℹ️  郵件通知未啟用（在 config.py 設定 EMAIL_NOTIFICATIONS_ENABLED）")

        # Slack 通知
        if hasattr(config, 'SLACK_WEBHOOK_URL') and config.SLACK_WEBHOOK_URL:
            self._send_slack(report)
        else:
            print("   ℹ️  Slack 通知未設定（在 .env 加入 SLACK_WEBHOOK_URL）")

    def _send_email(self, report):
        """發送郵件通知"""
        try:
            # 建立郵件內容
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"⚠️ JobMetrics Pro 異常警報 - {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = config.EMAIL_FROM
            msg['To'] = config.EMAIL_TO

            # HTML 郵件內容
            html_content = self._generate_email_html(report)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # 發送郵件
            with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
                server.starttls()
                server.login(config.SMTP_USER, config.SMTP_PASSWORD)
                server.send_message(msg)

            print(f"   ✅ 郵件已發送到: {config.EMAIL_TO}")

        except Exception as e:
            print(f"   ❌ 郵件發送失敗: {str(e)}")

    def _send_slack(self, report):
        """發送 Slack 通知"""
        try:
            import requests

            # 建立 Slack 訊息
            slack_message = self._generate_slack_message(report)

            # 發送到 Slack
            response = requests.post(
                config.SLACK_WEBHOOK_URL,
                json=slack_message,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                print(f"   ✅ Slack 通知已發送")
            else:
                print(f"   ❌ Slack 發送失敗: {response.text}")

        except Exception as e:
            print(f"   ❌ Slack 通知發送失敗: {str(e)}")

    def _generate_email_html(self, report):
        """生成郵件 HTML 內容"""
        anomalies = report['anomalies']

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #ff4444; color: white; padding: 20px; }}
                .critical {{ background-color: #ffebee; border-left: 4px solid #f44336; padding: 10px; margin: 10px 0; }}
                .warning {{ background-color: #fff8e1; border-left: 4px solid #ffc107; padding: 10px; margin: 10px 0; }}
                .metric-name {{ font-weight: bold; font-size: 16px; }}
                .metric-value {{ color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>⚠️ JobMetrics Pro 異常警報</h1>
                <p>檢測時間: {report['timestamp']}</p>
            </div>

            <div style="padding: 20px;">
                <h2>📊 異常摘要</h2>
                <ul>
                    <li>總異常數: {report['total_anomalies']}</li>
                    <li>危急: {report['critical_count']}</li>
                    <li>警告: {report['warning_count']}</li>
                </ul>

                <h2>🔍 詳細異常</h2>
        """

        for a in anomalies:
            severity_class = 'critical' if a['severity'] == 'critical' else 'warning'
            icon = '🚨' if a['severity'] == 'critical' else '⚠️'

            html += f"""
                <div class="{severity_class}">
                    <div class="metric-name">{icon} {a['metric']}</div>
                    <div>{a['message']}</div>
                    <div class="metric-value">當前值: {a['value']}</div>
                </div>
            """

        html += """
                <hr>
                <p style="color: #666;">
                    此郵件由 JobMetrics Pro 每日自動掃描系統產生<br>
                    如需查看完整 dashboard: <a href="http://localhost:8502">http://localhost:8502</a>
                </p>
            </div>
        </body>
        </html>
        """

        return html

    def _generate_slack_message(self, report):
        """生成 Slack 訊息"""
        anomalies = report['anomalies']

        # 建立附件區塊
        attachments = []

        for a in anomalies:
            color = 'danger' if a['severity'] == 'critical' else 'warning'
            icon = '🚨' if a['severity'] == 'critical' else '⚠️'

            attachments.append({
                'color': color,
                'title': f"{icon} {a['metric']}",
                'text': a['message'],
                'fields': [
                    {
                        'title': '當前值',
                        'value': a['value'],
                        'short': True
                    }
                ]
            })

        message = {
            'text': f"⚠️ *JobMetrics Pro 異常警報* - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            'attachments': attachments
        }

        return message


def main():
    """主程式"""
    checker = DailyAnomalyChecker()
    checker.run_check()


if __name__ == "__main__":
    main()
