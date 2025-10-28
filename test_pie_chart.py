#!/usr/bin/env python3
"""
測試圓餅圖獨立運行
"""
import streamlit as st
import sys
sys.path.insert(0, '/Users/jerrylaivivemachi/DS PROJECT/self-help databboard/src/core')

from analytics import SaaSAnalytics
import plotly.express as px

st.set_page_config(page_title="圓餅圖測試", layout="wide")

st.title("🧪 圓餅圖測試頁面")

st.write("---")

# 加載數據
analytics = SaaSAnalytics()
revenue_by_plan = analytics.get_revenue_by_plan()

# 顯示原始數據
st.subheader("📊 原始數據")
st.dataframe(revenue_by_plan)

st.write("---")

# 測試 1: 基本圓餅圖
st.subheader("測試 1: 基本圓餅圖")
col1, col2 = st.columns([2, 1])

with col1:
    st.write("左側欄位（模擬 MRR Trend 位置）")
    st.write("這裡通常是折線圖")

with col2:
    st.write("💰 Revenue by Plan")
    fig1 = px.pie(
        revenue_by_plan,
        values='mrr',
        names='plan_type',
        title='MRR Distribution'
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

st.write("---")

# 測試 2: 全寬圓餅圖
st.subheader("測試 2: 全寬圓餅圖（確保可見）")
fig2 = px.pie(
    revenue_by_plan,
    values='mrr',
    names='plan_type',
    title='MRR Distribution (Full Width)'
)
fig2.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig2, use_container_width=True)

st.write("---")

# 測試 3: 指定高度
st.subheader("測試 3: 指定高度的圓餅圖")
fig3 = px.pie(
    revenue_by_plan,
    values='mrr',
    names='plan_type',
    title='MRR Distribution (Height 400px)',
    height=400
)
fig3.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig3, use_container_width=True)

st.write("---")

# 診斷訊息
st.subheader("🔍 診斷訊息")
st.write(f"- 數據筆數: {len(revenue_by_plan)}")
st.write(f"- Plotly 可用: ✅")
st.write(f"- 數據有效: ✅")
st.write(f"- 欄位正確: ✅")

st.success("如果你看到上面 3 個圓餅圖，代表 Plotly 圖表功能正常！")
st.info("如果在 dashboard.py 看不到，可能是佈局或滾動問題。")
