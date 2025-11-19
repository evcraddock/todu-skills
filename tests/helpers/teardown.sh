#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$(dirname "$SCRIPT_DIR")"

echo "Tearing down todu test environment..."

# Check if todu CLI is installed
if ! command -v todu &> /dev/null; then
    echo "Error: todu CLI is not installed"
    exit 1
fi

cd "$TEST_DIR"

# Check if todu-tests project exists
if ! todu project list --format json | grep -q '"name": "todu-tests"'; then
    echo "Test project 'todu-tests' does not exist. Nothing to clean up."
    exit 0
fi

# Get the project ID
PROJECT_ID=$(todu project list --format json | grep -A 5 '"name": "todu-tests"' | grep '"id"' | head -1 | awk '{print $2}' | tr -d ',')

if [ -z "$PROJECT_ID" ]; then
    echo "Error: Could not find project ID for 'todu-tests'"
    exit 1
fi

# Remove the test project
echo "Removing test project 'todu-tests' (ID: $PROJECT_ID)..."
todu project remove "$PROJECT_ID" --force

echo "Test environment teardown complete!"
