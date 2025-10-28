#!/bin/bash
# 🚀 Start Dashboard with Secure API Proxy
# This script starts both the proxy server and dashboard together

set -e  # Exit on error

echo "======================================================================"
echo "🔐 JobMetrics Pro - Starting with Secure API Proxy"
echo "======================================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: .env file not found!${NC}"
    echo -e "${YELLOW}📝 Creating .env from template...${NC}"

    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ .env created from .env.example${NC}"
        echo -e "${YELLOW}⚠️  Please edit .env and add your real API key!${NC}"
        echo ""
        echo "Edit this file: .env"
        echo "Add your key: ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE"
        echo ""
        exit 1
    else
        echo -e "${RED}❌ .env.example not found either!${NC}"
        exit 1
    fi
fi

# Check if API key is set
if ! grep -q "ANTHROPIC_API_KEY=sk-ant-api03-" .env; then
    echo -e "${RED}❌ Error: ANTHROPIC_API_KEY not set in .env${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env and add your real API key${NC}"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${BLUE}🐍 Python version: $python_version${NC}"

# Check if required packages are installed
echo -e "${BLUE}📦 Checking dependencies...${NC}"
if ! python3 -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Flask not installed. Installing dependencies...${NC}"
    pip3 install -r requirements.txt
fi

if ! python3 -c "import flask_cors" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Flask-CORS not installed. Installing...${NC}"
    pip3 install flask-cors
fi

echo -e "${GREEN}✅ All dependencies installed${NC}"
echo ""

# Create log directory
mkdir -p logs

# Function to cleanup background processes
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down servers...${NC}"

    # Kill proxy server
    if [ ! -z "$PROXY_PID" ]; then
        kill $PROXY_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Proxy server stopped${NC}"
    fi

    # Kill dashboard
    if [ ! -z "$DASHBOARD_PID" ]; then
        kill $DASHBOARD_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Dashboard stopped${NC}"
    fi

    echo -e "${GREEN}✅ Cleanup complete${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

echo "======================================================================"
echo "🔧 Starting Services"
echo "======================================================================"
echo ""

# Start API proxy server
echo -e "${BLUE}1. Starting API Proxy Server (port 5001)...${NC}"
python3 api_proxy.py > logs/proxy.log 2>&1 &
PROXY_PID=$!

# Wait for proxy to start
echo -e "${YELLOW}   Waiting for proxy to initialize...${NC}"
sleep 3

# Check if proxy is running
if ! kill -0 $PROXY_PID 2>/dev/null; then
    echo -e "${RED}❌ Proxy server failed to start!${NC}"
    echo -e "${YELLOW}📋 Check logs/proxy.log for details${NC}"
    tail -20 logs/proxy.log
    exit 1
fi

# Test proxy health
if curl -s http://localhost:5001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Proxy server is healthy (http://localhost:5001)${NC}"
else
    echo -e "${RED}❌ Proxy server not responding to health check${NC}"
    kill $PROXY_PID 2>/dev/null || true
    exit 1
fi

echo ""

# Start Streamlit dashboard
echo -e "${BLUE}2. Starting Streamlit Dashboard (port 8501)...${NC}"
streamlit run src/dashboard/dashboard.py --server.port 8501 > logs/dashboard.log 2>&1 &
DASHBOARD_PID=$!

# Wait for dashboard to start
echo -e "${YELLOW}   Waiting for dashboard to initialize...${NC}"
sleep 5

# Check if dashboard is running
if ! kill -0 $DASHBOARD_PID 2>/dev/null; then
    echo -e "${RED}❌ Dashboard failed to start!${NC}"
    echo -e "${YELLOW}📋 Check logs/dashboard.log for details${NC}"
    tail -20 logs/dashboard.log
    cleanup
    exit 1
fi

echo -e "${GREEN}✅ Dashboard is starting up (http://localhost:8501)${NC}"
echo ""

echo "======================================================================"
echo "🎉 All Services Started Successfully!"
echo "======================================================================"
echo ""
echo -e "${GREEN}📊 Dashboard:${NC}      http://localhost:8501"
echo -e "${GREEN}🔐 API Proxy:${NC}      http://localhost:5001"
echo -e "${GREEN}📋 Proxy Logs:${NC}     tail -f logs/proxy.log"
echo -e "${GREEN}📋 Dashboard Logs:${NC} tail -f logs/dashboard.log"
echo ""
echo "======================================================================"
echo "🔒 Security Status"
echo "======================================================================"
echo -e "${GREEN}✅${NC} API key stored server-side only (in api_proxy.py)"
echo -e "${GREEN}✅${NC} Rate limiting active (30 requests/60 seconds per IP)"
echo -e "${GREEN}✅${NC} CORS protection enabled"
echo -e "${GREEN}✅${NC} Request validation active"
echo -e "${GREEN}✅${NC} All requests logged"
echo ""
echo "======================================================================"
echo "📝 Usage Instructions"
echo "======================================================================"
echo ""
echo "1. Open browser: http://localhost:8501"
echo "2. Use the dashboard normally"
echo "3. AI queries go through secure proxy (transparent to you)"
echo "4. Press Ctrl+C to stop all services"
echo ""
echo "======================================================================"
echo "🔍 Monitoring"
echo "======================================================================"
echo ""
echo "Check rate limit status:"
echo "  curl http://localhost:5001/api/rate-limit-status"
echo ""
echo "Test proxy directly:"
echo "  curl -X POST http://localhost:5001/api/query \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"question\":\"test\",\"context\":{}}'"
echo ""
echo "======================================================================"
echo ""
echo -e "${YELLOW}⏳ Services running... Press Ctrl+C to stop${NC}"
echo ""

# Keep script running
wait $DASHBOARD_PID

# Cleanup on exit
cleanup
