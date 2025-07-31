#!/bin/bash

# CodeRoot Bot - Comprehensive Deployment Testing Script
set -e

echo "🧪 CodeRoot Bot - Comprehensive Deployment Testing"
echo "=================================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

FAILED_TESTS=0
TOTAL_TESTS=0

run_test() {
    local test_name="$1"
    local test_command="$2"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -e "${BLUE}🔍 Test $TOTAL_TESTS: $test_name${NC}"
    
    if eval "$test_command"; then
        echo -e "${GREEN}✅ PASSED: $test_name${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED: $test_name${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

echo -e "${YELLOW}🔧 Phase 1: Environment & Dependencies${NC}"

run_test "Go Version Check" "go version | grep -q 'go1.2'"
run_test "Vendor Directory Check" "[ -d vendor ] && [ -f vendor/modules.txt ]"
run_test "Go Module Files Check" "[ -f go.mod ] && [ -f go.sum ]"
run_test "Source Files Check" "[ -f main.go ] && [ -d internal ]"

echo -e "${YELLOW}🏗️  Phase 2: Build Testing${NC}"

run_test "Go Vet Check" "go vet ./..."
run_test "Compilation Test" "go build -mod=vendor -o test-binary ."
run_test "Binary Executable Check" "[ -x test-binary ]"

rm -f test-binary

echo -e "${YELLOW}🚀 Phase 3: Deployment Scripts${NC}"

run_test "Deploy Script Check" "[ -x deploy.sh ]"
run_test "Start Script Check" "[ -x start.sh ]"
run_test "Environment Template Check" "[ -f .env.example ]"
run_test "Dockerfile Check" "[ -f Dockerfile ]"

echo -e "${YELLOW}🔧 Phase 4: Code Quality${NC}"

run_test "Error Handling Check" "grep -r 'if err != nil' internal/ | wc -l | awk '{exit (\$1 < 10)}'"
run_test "Repository Methods Check" "grep -q 'GetByUserID' internal/database/repositories.go"

echo ""
echo "=============================================="
echo -e "${BLUE}📊 TEST RESULTS SUMMARY${NC}"
echo "=============================================="

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED! ($TOTAL_TESTS/$TOTAL_TESTS)${NC}"
    echo -e "${GREEN}✅ Your CodeRoot Bot is ready for deployment!${NC}"
    exit 0
else
    echo -e "${RED}❌ TESTS FAILED: $FAILED_TESTS/$TOTAL_TESTS${NC}"
    echo -e "${RED}🚨 Deployment NOT recommended until issues are fixed!${NC}"
    exit 1
fi
