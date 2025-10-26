#!/bin/bash

# Quick launch script for JobMetrics Pro Dashboard

echo "🚀 Launching JobMetrics Pro Dashboard..."
echo ""

# Check if data exists
if [ ! -d "data" ] || [ ! -f "data/users.csv" ]; then
    echo "📊 Generating sample data first..."
    python data_generator.py
    echo ""
fi

# Launch dashboard
echo "🎯 Starting dashboard on http://localhost:8501"
echo ""
streamlit run dashboard.py
