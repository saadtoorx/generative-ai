#!/bin/bash

# Medical Notes Structuring Assistant - Startup Script
# This script starts both the backend (FastAPI) and frontend (Streamlit) servers

echo "=========================================="
echo "  Medical Notes Structuring Assistant"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Ollama is running
echo -e "${YELLOW}[1/4] Checking Ollama status...${NC}"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Ollama is running${NC}"
else
    echo -e "${RED}✗ Ollama is not running. Please start Ollama first.${NC}"
    echo "  Run: ollama serve"
    echo ""
fi

# Navigate to project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo -e "${YELLOW}[2/4] Starting Backend Server (FastAPI)...${NC}"
echo "  Backend will be available at: http://localhost:8000"
echo "  API Documentation at: http://localhost:8000/docs"

# Start backend in background
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

echo ""
echo -e "${YELLOW}[3/4] Starting Frontend Server (Streamlit)...${NC}"
echo "  Frontend will be available at: http://localhost:8501"

# Start frontend in background
cd frontend
streamlit run app.py --server.port 8501 &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}[4/4] Both servers started successfully!${NC}"
echo ""
echo "=========================================="
echo "  Access Points:"
echo "  - Frontend: http://localhost:8501"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "=========================================="
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}Servers stopped. Goodbye!${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT SIGTERM

# Wait for processes
wait
