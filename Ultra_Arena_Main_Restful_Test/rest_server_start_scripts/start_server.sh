#!/bin/bash

# Ultra Arena Main RESTful Server Startup Script
# This script starts the RESTful server in the background
# 
# Usage: ./start_server.sh [--run_profile PROFILE_NAME]
# 
# Arguments:
#   --run_profile PROFILE_NAME  Profile to use (default: default_profile_restful)

set -e

# Configuration
SERVER_DIR="../Ultra_Arena_Main_Restful"
SERVER_SCRIPT="server.py"
LOG_DIR="logs"
PID_FILE="server.pid"
PORT=5002
DEFAULT_PROFILE="default_profile_restful"

# Parse command line arguments
RUN_PROFILE="$DEFAULT_PROFILE"

while [[ $# -gt 0 ]]; do
    case $1 in
        --run_profile)
            RUN_PROFILE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--run_profile PROFILE_NAME]"
            exit 1
            ;;
    esac
done

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Ultra Arena Main RESTful Server Startup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${YELLOW}Configuration:${NC}"
echo -e "  Profile: ${GREEN}$RUN_PROFILE${NC}"
echo -e "  Port: ${GREEN}$PORT${NC}"
echo ""

# Check if server directory exists
if [ ! -d "$SERVER_DIR" ]; then
    echo -e "${RED}Error: Server directory not found: $SERVER_DIR${NC}"
    exit 1
fi

# Check if server script exists
if [ ! -f "$SERVER_DIR/$SERVER_SCRIPT" ]; then
    echo -e "${RED}Error: Server script not found: $SERVER_DIR/$SERVER_SCRIPT${NC}"
    exit 1
fi

# Check if profile directory exists
PROFILE_DIR="$SERVER_DIR/run_profiles/$RUN_PROFILE"
if [ ! -d "$PROFILE_DIR" ]; then
    echo -e "${RED}Error: Profile directory not found: $PROFILE_DIR${NC}"
    echo -e "${YELLOW}Available profiles:${NC}"
    if [ -d "$SERVER_DIR/run_profiles" ]; then
        ls -1 "$SERVER_DIR/run_profiles" | sed 's/^/  - /'
    fi
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Check if server is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}Server is already running with PID: $PID${NC}"
        echo -e "${GREEN}Server URL: http://localhost:$PORT${NC}"
        exit 0
    else
        echo -e "${YELLOW}Removing stale PID file${NC}"
        rm -f "$PID_FILE"
    fi
fi

# Check if port is available
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${RED}Error: Port $PORT is already in use${NC}"
    echo "Please stop the service using port $PORT or change the port in this script"
    exit 1
fi

# Change to server directory
cd "$SERVER_DIR"

# Start the server in background with profile
echo -e "${YELLOW}Starting server on port $PORT with profile: $RUN_PROFILE${NC}"
PORT=$PORT RUN_PROFILE=$RUN_PROFILE nohup python3 "$SERVER_SCRIPT" > "../Ultra_Arena_Main_Restful_Test/$LOG_DIR/server.log" 2>&1 &
SERVER_PID=$!

# Save PID to file
echo $SERVER_PID > "../Ultra_Arena_Main_Restful_Test/$PID_FILE"

# Wait a moment for server to start
sleep 3

# Check if server started successfully
if ps -p "$SERVER_PID" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Server started successfully!${NC}"
    echo -e "${GREEN}✓ PID: $SERVER_PID${NC}"
    echo -e "${GREEN}✓ Port: $PORT${NC}"
    echo -e "${GREEN}✓ URL: http://localhost:$PORT${NC}"
    echo -e "${GREEN}✓ Logs: $LOG_DIR/server.log${NC}"
    echo -e "${GREEN}✓ Profile: $RUN_PROFILE${NC}"
    echo ""
    echo -e "${YELLOW}Available endpoints:${NC}"
    echo "  GET  http://localhost:$PORT/health"
    echo "  POST http://localhost:$PORT/api/process"
    echo "  POST http://localhost:$PORT/api/process/combo"
    echo "  GET  http://localhost:$PORT/api/combos"
    echo "  GET  http://localhost:$PORT/api/profiles"
    echo ""
    echo -e "${YELLOW}To stop the server, run: ./server/stop_server.sh${NC}"
else
    echo -e "${RED}✗ Failed to start server${NC}"
    echo -e "${YELLOW}Check logs: $LOG_DIR/server.log${NC}"
    exit 1
fi 