#!/bin/bash
# ==============================================
# OPOSICIONES-SYSTEM Setup Verification Script
# ==============================================
# Run this script to verify your environment is ready

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0
WARN=0

echo "========================================"
echo "  OPOSICIONES-SYSTEM Setup Test"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# ---------------------------------------------
# Helper Functions
# ---------------------------------------------

check_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((FAIL++))
}

check_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    ((WARN++))
}

# ---------------------------------------------
# 1. Environment Variables
# ---------------------------------------------
echo "--- Environment Variables ---"

if [ -f ".env" ]; then
    check_pass ".env file exists"

    # Source the .env file
    export $(grep -v '^#' .env | xargs)

    # Check required vars
    for var in MINIMAX_API_KEY MISTRAL_API_KEY TELEGRAM_BOT_TOKEN; do
        if [ -n "${!var}" ] && [ "${!var}" != "your_${var,,}_here" ]; then
            check_pass "$var is configured"
        else
            check_fail "$var is not configured"
        fi
    done
else
    check_fail ".env file not found - copy .env.example to .env"
fi

echo ""

# ---------------------------------------------
# 2. Python Version
# ---------------------------------------------
echo "--- Python Environment ---"

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
    check_pass "Python $PYTHON_VERSION (>= 3.10 required)"
else
    check_fail "Python $PYTHON_VERSION - need 3.10+ (current: $PYTHON_MAJOR.$PYTHON_MINOR)"
fi

# Check pip
if command -v pip3 &> /dev/null; then
    check_pass "pip3 available"
else
    check_fail "pip3 not found"
fi

echo ""

# ---------------------------------------------
# 3. Docker
# ---------------------------------------------
echo "--- Docker Environment ---"

if command -v docker &> /dev/null; then
    check_pass "Docker installed"

    if docker info &> /dev/null; then
        check_pass "Docker daemon running"
    else
        check_fail "Docker daemon not running - start Docker Desktop"
    fi
else
    check_fail "Docker not installed"
fi

echo ""

# ---------------------------------------------
# 4. Redis
# ---------------------------------------------
echo "--- Redis ---"

if docker ps 2>/dev/null | grep -q redis; then
    check_pass "Redis container running"
elif command -v redis-cli &> /dev/null; then
    if redis-cli ping 2>/dev/null | grep -q PONG; then
        check_pass "Redis server responding"
    else
        check_warn "Redis installed but not responding"
    fi
else
    check_warn "Redis not configured (optional for caching)"
fi

echo ""

# ---------------------------------------------
# 5. Ollama
# ---------------------------------------------
echo "--- Ollama (Local LLM Fallback) ---"

if command -v ollama &> /dev/null; then
    check_pass "Ollama installed"

    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        check_pass "Ollama server running"

        # Check for model
        if ollama list 2>/dev/null | grep -q "llama3"; then
            check_pass "llama3 model available"
        else
            check_warn "No llama3 model - run: ollama pull llama3.2:3b"
        fi
    else
        check_warn "Ollama not running - start with: ollama serve"
    fi
else
    check_warn "Ollama not installed - visit: https://ollama.ai"
fi

echo ""

# ---------------------------------------------
# 6. API Connectivity Tests
# ---------------------------------------------
echo "--- API Connectivity ---"

# MiniMax API Test
if [ -n "$MINIMAX_API_KEY" ] && [ -n "$MINIMAX_GROUP_ID" ]; then
    echo "Testing MiniMax API..."
    RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/minimax_test.json \
        "https://api.minimax.chat/v1/text/chatcompletion_v2" \
        -H "Authorization: Bearer $MINIMAX_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"model":"abab6.5s-chat","messages":[{"role":"user","content":"hi"}],"max_tokens":10}' \
        2>/dev/null || echo "000")

    HTTP_CODE=${RESPONSE: -3}
    if [ "$HTTP_CODE" = "200" ]; then
        check_pass "MiniMax API responding"
    else
        check_fail "MiniMax API error (HTTP $HTTP_CODE)"
    fi
    rm -f /tmp/minimax_test.json
else
    check_warn "Skipping MiniMax test - credentials not set"
fi

# Mistral API Test
if [ -n "$MISTRAL_API_KEY" ]; then
    echo "Testing Mistral API..."
    RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/mistral_test.json \
        "https://api.mistral.ai/v1/embeddings" \
        -H "Authorization: Bearer $MISTRAL_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"model":"mistral-embed","input":"test"}' \
        2>/dev/null || echo "000")

    HTTP_CODE=${RESPONSE: -3}
    if [ "$HTTP_CODE" = "200" ]; then
        check_pass "Mistral API responding"
    else
        check_fail "Mistral API error (HTTP $HTTP_CODE)"
    fi
    rm -f /tmp/mistral_test.json
else
    check_warn "Skipping Mistral test - credentials not set"
fi

echo ""

# ---------------------------------------------
# 7. Telegram Bot Test
# ---------------------------------------------
echo "--- Telegram Bot ---"

if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    echo "Testing Telegram Bot API..."
    RESPONSE=$(curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe" 2>/dev/null)

    if echo "$RESPONSE" | grep -q '"ok":true'; then
        BOT_USERNAME=$(echo "$RESPONSE" | grep -o '"username":"[^"]*"' | cut -d'"' -f4)
        check_pass "Telegram bot responding (@$BOT_USERNAME)"
    else
        check_fail "Telegram bot not responding - check token"
    fi
else
    check_warn "Skipping Telegram test - token not set"
fi

echo ""

# ---------------------------------------------
# 8. SQLite Test
# ---------------------------------------------
echo "--- SQLite ---"

if python3 -c "import sqlite3; conn = sqlite3.connect(':memory:'); conn.close()" 2>/dev/null; then
    check_pass "SQLite working"
else
    check_fail "SQLite not working"
fi

echo ""

# ---------------------------------------------
# 9. Data Directories
# ---------------------------------------------
echo "--- Data Directories ---"

DATA_DIR="${DATA_DIR:-$HOME/.oposiciones-system/data}"

for dir in "$DATA_DIR" "$(dirname ${VECTOR_DB_PATH:-$HOME/.oposiciones-system/vectors.db})" "$(dirname ${MEMORY_DB_PATH:-$HOME/.oposiciones-system/memory.db})"; do
    if [ -d "$dir" ]; then
        check_pass "Directory exists: $dir"
    else
        check_warn "Directory missing: $dir (will be created on first run)"
    fi
done

echo ""

# ---------------------------------------------
# Summary
# ---------------------------------------------
echo "========================================"
echo "  SUMMARY"
echo "========================================"
echo -e "${GREEN}Passed:${NC} $PASS"
echo -e "${YELLOW}Warnings:${NC} $WARN"
echo -e "${RED}Failed:${NC} $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}Environment ready for development!${NC}"
    exit 0
else
    echo -e "${RED}Please fix the failed checks before proceeding.${NC}"
    exit 1
fi
