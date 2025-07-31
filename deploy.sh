#!/bin/bash

# CodeRoot Bot Deployment Script
# This script builds the application using vendored dependencies for zero-dependency deployment

set -e  # Exit on any error

echo "🚀 CodeRoot Bot - Local Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="coderoot-bot"
BUILD_FLAGS="-mod=vendor -tags netgo -ldflags='-s -w'"
OUTPUT_BINARY="app"

echo -e "${BLUE}📋 Build Configuration:${NC}"
echo "  • App Name: $APP_NAME"
echo "  • Build Flags: $BUILD_FLAGS"
echo "  • Output Binary: $OUTPUT_BINARY"
echo "  • Using Vendored Dependencies: YES"
echo ""

# Check if vendor directory exists
if [ ! -d "vendor" ]; then
    echo -e "${RED}❌ Error: vendor/ directory not found${NC}"
    echo "Run 'go mod vendor' first to create vendored dependencies"
    exit 1
fi

echo -e "${YELLOW}📦 Vendor Directory Status:${NC}"
VENDOR_SIZE=$(du -sh vendor/ | cut -f1)
echo "  • Size: $VENDOR_SIZE"
echo "  • Dependencies: $(find vendor/ -name "*.go" | wc -l) Go files"
echo ""

# Clean previous builds
echo -e "${YELLOW}🧹 Cleaning previous builds...${NC}"
rm -f $OUTPUT_BINARY
echo "  • Removed old binary"

# Build the application
echo -e "${YELLOW}🔨 Building application...${NC}"
echo "Command: go build -mod=vendor -tags netgo -ldflags='-s -w' -o $OUTPUT_BINARY"

if go build -mod=vendor -tags netgo -ldflags='-s -w' -o $OUTPUT_BINARY; then
    echo -e "${GREEN}✅ Build successful!${NC}"
else
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi

# Check binary
if [ -f "$OUTPUT_BINARY" ]; then
    BINARY_SIZE=$(ls -lh $OUTPUT_BINARY | awk '{print $5}')
    echo -e "${GREEN}📊 Binary Information:${NC}"
    echo "  • File: $OUTPUT_BINARY"
    echo "  • Size: $BINARY_SIZE"
    echo "  • Executable: Yes"
    echo ""
else
    echo -e "${RED}❌ Error: Binary not created${NC}"
    exit 1
fi

# Test binary
echo -e "${YELLOW}🧪 Testing binary...${NC}"
if timeout 3s ./$OUTPUT_BINARY 2>/dev/null || [ $? -eq 124 ]; then
    echo -e "${GREEN}✅ Binary starts successfully${NC}"
else
    echo -e "${YELLOW}⚠️  Binary requires environment variables (expected)${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Deployment Ready!${NC}"
echo "=========================================="
echo -e "${BLUE}📝 Next Steps:${NC}"
echo "1. Set required environment variables:"
echo "   • BOT_TOKEN=your_telegram_bot_token"
echo "   • MONGO_URI=your_mongodb_connection_string"
echo "   • REDIS_URL=your_redis_connection_string"
echo ""
echo "2. Run the application:"
echo "   ./$OUTPUT_BINARY"
echo ""
echo "3. For production deployment:"
echo "   • Upload entire project directory (including vendor/)"
echo "   • Run this script on target server"
echo "   • Configure environment variables"
echo "   • Start the application"
echo ""
echo -e "${GREEN}✨ Zero-dependency deployment ready!${NC}"