#!/bin/bash

# CodeRoot Bot Production Startup Script
# This script starts the application with proper error handling and logging

set -e

echo "🚀 Starting CodeRoot Bot..."
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

APP_BINARY="./app"
LOG_DIR="logs"
LOG_FILE="$LOG_DIR/app.log"
PID_FILE="$LOG_DIR/app.pid"

# Create logs directory if it doesn't exist
mkdir -p $LOG_DIR

# Function to check if app is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null 2>&1; then
            return 0
        else
            rm -f $PID_FILE
            return 1
        fi
    fi
    return 1
}

# Function to stop the application
stop_app() {
    echo -e "${YELLOW}🛑 Stopping application...${NC}"
    if [ -f "$PID_FILE" ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null 2>&1; then
            kill $PID
            sleep 2
            if ps -p $PID > /dev/null 2>&1; then
                echo -e "${RED}Force killing application...${NC}"
                kill -9 $PID
            fi
            rm -f $PID_FILE
            echo -e "${GREEN}✅ Application stopped${NC}"
        else
            echo -e "${YELLOW}⚠️  Application was not running${NC}"
            rm -f $PID_FILE
        fi
    else
        echo -e "${YELLOW}⚠️  No PID file found${NC}"
    fi
}

# Function to start the application
start_app() {
    echo -e "${BLUE}📋 Pre-flight checks:${NC}"
    
    # Check if binary exists
    if [ ! -f "$APP_BINARY" ]; then
        echo -e "${RED}❌ Error: Application binary not found at $APP_BINARY${NC}"
        echo "Run './deploy.sh' first to build the application"
        exit 1
    fi
    echo -e "${GREEN}✅ Binary found${NC}"
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}⚠️  .env file not found${NC}"
        echo "Copy .env.example to .env and configure your environment variables"
        if [ ! -f ".env.example" ]; then
            echo -e "${RED}❌ Error: .env.example not found${NC}"
            exit 1
        fi
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Please edit .env file with your actual configuration before running again${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Environment file found${NC}"
    
    # Load environment variables
    source .env
    
    # Check required environment variables
    if [ -z "$BOT_TOKEN" ] || [ "$BOT_TOKEN" = "your_telegram_bot_token_here" ]; then
        echo -e "${RED}❌ Error: BOT_TOKEN not configured${NC}"
        echo "Please set your Telegram bot token in .env file"
        exit 1
    fi
    echo -e "${GREEN}✅ BOT_TOKEN configured${NC}"
    
    if [ -z "$MONGO_URI" ] || [ "$MONGO_URI" = "mongodb://localhost:27017/coderoot_bot" ]; then
        echo -e "${YELLOW}⚠️  Using default MongoDB URI${NC}"
    fi
    echo -e "${GREEN}✅ MONGO_URI configured${NC}"
    
    if [ -z "$REDIS_URL" ] || [ "$REDIS_URL" = "redis://localhost:6379" ]; then
        echo -e "${YELLOW}⚠️  Using default Redis URL${NC}"
    fi
    echo -e "${GREEN}✅ REDIS_URL configured${NC}"
    
    echo ""
    echo -e "${BLUE}🚀 Starting application...${NC}"
    
    # Start the application in background
    nohup $APP_BINARY > $LOG_FILE 2>&1 &
    APP_PID=$!
    
    # Save PID
    echo $APP_PID > $PID_FILE
    
    # Wait a moment to check if it started successfully
    sleep 2
    
    if ps -p $APP_PID > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Application started successfully!${NC}"
        echo -e "${BLUE}📊 Application Info:${NC}"
        echo "  • PID: $APP_PID"
        echo "  • Log File: $LOG_FILE"
        echo "  • PID File: $PID_FILE"
        echo ""
        echo -e "${BLUE}📝 Useful Commands:${NC}"
        echo "  • View logs: tail -f $LOG_FILE"
        echo "  • Stop app: ./start.sh stop"
        echo "  • Restart app: ./start.sh restart"
        echo "  • Check status: ./start.sh status"
        echo ""
        echo -e "${GREEN}🎉 CodeRoot Bot is now running!${NC}"
    else
        echo -e "${RED}❌ Application failed to start${NC}"
        echo "Check the log file for details: $LOG_FILE"
        rm -f $PID_FILE
        exit 1
    fi
}

# Function to show status
show_status() {
    if is_running; then
        PID=$(cat $PID_FILE)
        echo -e "${GREEN}✅ Application is running${NC}"
        echo "  • PID: $PID"
        echo "  • Log File: $LOG_FILE"
        echo "  • Uptime: $(ps -o etime= -p $PID | tr -d ' ')"
    else
        echo -e "${RED}❌ Application is not running${NC}"
    fi
}

# Function to restart application
restart_app() {
    echo -e "${BLUE}🔄 Restarting application...${NC}"
    if is_running; then
        stop_app
        sleep 1
    fi
    start_app
}

# Main script logic
case "${1:-start}" in
    start)
        if is_running; then
            echo -e "${YELLOW}⚠️  Application is already running${NC}"
            show_status
        else
            start_app
        fi
        ;;
    stop)
        stop_app
        ;;
    restart)
        restart_app
        ;;
    status)
        show_status
        ;;
    logs)
        if [ -f "$LOG_FILE" ]; then
            tail -f $LOG_FILE
        else
            echo -e "${RED}❌ Log file not found: $LOG_FILE${NC}"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the application (default)"
        echo "  stop    - Stop the application"
        echo "  restart - Restart the application"
        echo "  status  - Show application status"
        echo "  logs    - Follow application logs"
        exit 1
        ;;
esac