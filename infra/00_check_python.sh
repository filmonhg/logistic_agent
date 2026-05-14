#!/usr/bin/env bash
set -euo pipefail

REQUIRED_MAJOR=3
REQUIRED_MINOR=10

if ! command -v python >/dev/null 2>&1; then
  echo "❌ No 'python' on PATH. Did you activate the venv? Try:"
  echo "   source logistics-venv/bin/activate"
  exit 1
fi

PY_VERSION=$(python --version 2>&1 | awk '{print $2}')
MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
MINOR=$(echo "$PY_VERSION" | cut -d. -f2)

if [ "$MAJOR" -lt "$REQUIRED_MAJOR" ] || \
   { [ "$MAJOR" -eq "$REQUIRED_MAJOR" ] && [ "$MINOR" -lt "$REQUIRED_MINOR" ]; }; then
  echo "❌ Python ${REQUIRED_MAJOR}.${REQUIRED_MINOR}+ required, found ${PY_VERSION}"
  echo ""
  echo "Fix on macOS:"
  echo "   brew install python@3.12"
  echo "   cd ~/logistics-agent"
  echo "   deactivate; rm -rf logistics-venv"
  echo "   python3.12 -m venv logistics-venv"
  echo "   source logistics-venv/bin/activate"
  echo "   pip install --upgrade pip"
  echo "   pip install -r requirements.txt"
  exit 1
fi

# Confirm key packages are importable
python -c "from strands import Agent" 2>/dev/null || {
  echo "❌ Cannot import 'strands'. Run: pip install -r requirements.txt"; exit 1; }
python -c "from mcp.server.fastmcp import FastMCP" 2>/dev/null || {
  echo "❌ Cannot import 'mcp'. Run: pip install -r requirements.txt"; exit 1; }
python -c "import boto3" 2>/dev/null || {
  echo "❌ Cannot import 'boto3'. Run: pip install -r requirements.txt"; exit 1; }

echo "✓ Python ${PY_VERSION} OK, all required packages importable."
