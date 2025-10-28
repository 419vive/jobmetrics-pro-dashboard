#!/bin/bash

# JobMetrics Pro Dashboard Launcher
# This script ensures the dashboard runs with correct paths

echo "🚀 Starting JobMetrics Pro Dashboard..."
echo ""

# Navigate to src directory
cd "$(dirname "$0")/src"

# Set PYTHONPATH to include src directory
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Run Streamlit
streamlit run dashboard/dashboard.py

# Note: Dashboard will be available at http://localhost:8501
