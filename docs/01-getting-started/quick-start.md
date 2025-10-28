# 🚀 如何運行 JobMetrics Pro Dashboard

## ✅ 已修復的問題

所有導入錯誤和函數參數問題已經修復！Dashboard 現在可以正常運行。

## 🎯 快速啟動（推薦）

使用啟動腳本：

```bash
./run_dashboard.sh
```

## 📝 手動啟動方式

如果啟動腳本不工作，使用以下命令：

```bash
cd src
streamlit run dashboard/dashboard.py
```

## 🌐 訪問 Dashboard

啟動後，在瀏覽器打開：

```
http://localhost:8501
```

## 🔧 已修復的技術問題

### 1. Import 路徑錯誤 ✅
- **問題**: `ModuleNotFoundError: No module named 'core'`
- **解決方案**: 添加了 `sys.path` 配置，確保 Python 能找到 core 模組

### 2. 函數參數不匹配 ✅
- `render_funnel_tab()` - 添加 `periods` 參數
- `render_cohort_tab()` - 添加 `periods` 參數
- 所有函數調用已更新匹配新簽名

### 3. 日期範圍適配 ✅
- 添加了 `get_adaptive_periods()` 函數
- 所有指標現在根據選擇的日期範圍自動調整
- 7天、30天、90天、1年、全部數據 - 完全支持

## 📊 新增功能

### 性能優化
- ✅ 5分鐘緩存 - 加快加載速度
- ✅ 智能數據過濾

### 比較視圖
- ✅ 本期 vs 上期對比
- ✅ Delta 百分比顯示
- ✅ 顏色編碼指示器

### 交互式篩選
- ✅ 訂閱方案篩選
- ✅ 獲客渠道篩選
- ✅ 活動篩選計數器
- ✅ 一鍵清除所有篩選

### 自定義日期範圍
- 🔄 UI 已添加（功能開發中）

## ❗ 故障排除

### 如果仍然看到 Import 錯誤：

```bash
# 確保在正確的目錄
cd "/Users/jerrylaivivemachi/DS PROJECT/self-help databboard"

# 設置 PYTHONPATH
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"

# 運行 dashboard
cd src
streamlit run dashboard/dashboard.py
```

### 如果看到數據文件錯誤：

確保以下文件存在：
- `data/users.csv`
- `data/subscriptions.csv`
- `data/scans.csv`
- `data/revenue.csv`

如果缺失，運行：
```bash
python data_generator.py
```

## 🎉 完成！

Dashboard 現在應該正常運行，所有功能都可用！

有任何問題請告訴我 😊
