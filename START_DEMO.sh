#!/bin/bash

# JobMetrics Pro - Quick Demo Launcher
# This script helps you quickly start the dashboard for demo

echo "=========================================="
echo "  JobMetrics Pro - Demo Launcher"
echo "=========================================="
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Check if data exists
if [ ! -f "data/users.csv" ]; then
    echo "❌ Data files not found!"
    echo "   Generating sample data..."
    python3 data_generator.py
    echo "✅ Data generated!"
    echo ""
fi

# Check dependencies
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit not installed!"
    echo "   Installing dependencies..."
    pip3 install -r requirements.txt
    echo "✅ Dependencies installed!"
    echo ""
fi

echo "=========================================="
echo "  Starting Dashboard..."
echo "=========================================="
echo ""
echo "📊 Dashboard will open at: http://localhost:8501"
echo ""
echo "🎯 Demo Tips:"
echo "   1. Navigate to 'Overview' tab first"
echo "   2. Show the Health Check and key metrics"
echo "   3. Point out the Revenue by Plan pie chart"
echo "   4. Switch to 'Conversion Funnel' tab"
echo "   5. Explain user segments and channel performance"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""
echo "=========================================="
echo ""

# Start Streamlit
streamlit run dashboard.py
