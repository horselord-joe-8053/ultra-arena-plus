#!/bin/bash

# Ultra Arena Main RESTful Server Stop Script
# This script stops the RESTful server gracefully

set -e

# Configuration
PID_FILE="server.pid"
LOG_DIR="logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Stopping Ultra Arena Main RESTful Server...${NC}"

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    echo -e "${YELLOW}No PID file found. Server may not be running.${NC}"
    exit 0
fi

# Read PID from file
PID=$(cat "$PID_FILE")

# Check if process is running
if ! ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${YELLOW}Process with PID $PID is not running. Removing stale PID file.${NC}"
    rm -f "$PID_FILE"
    exit 0
fi

echo -e "${YELLOW}Found server process with PID: $PID${NC}"

# Try graceful shutdown first
echo -e "${YELLOW}Sending SIGTERM to process $PID...${NC}"
kill -TERM "$PID"

# Wait for graceful shutdown (up to 10 seconds)
for i in {1..10}; do
    if ! ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Server stopped gracefully${NC}"
        rm -f "$PID_FILE"
        exit 0
    fi
    sleep 1
done

# Force kill if still running
echo -e "${YELLOW}Server did not stop gracefully. Force killing...${NC}"
kill -KILL "$PID"

# Wait a moment and check
sleep 2
if ! ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Server stopped forcefully${NC}"
    rm -f "$PID_FILE"
else
    echo -e "${RED}✗ Failed to stop server${NC}"
    echo -e "${YELLOW}You may need to manually kill the process: kill -9 $PID${NC}"
    exit 1
fi 