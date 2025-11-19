#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$(dirname "$SCRIPT_DIR")"

echo "Setting up todu test environment..."

# Check if todu CLI is installed
if ! command -v todu &> /dev/null; then
    echo "Error: todu CLI is not installed"
    exit 1
fi

# Check if test API is accessible
cd "$TEST_DIR"
API_URL=$(grep "api_url:" config.yaml | awk '{print $2}' | tr -d '"')
echo "Checking test API at $API_URL..."

if ! curl -s -f "$API_URL/health" > /dev/null 2>&1; then
    echo "Warning: Test API at $API_URL may not be accessible"
    echo "Continuing anyway..."
fi

# Check if todu-tests project already exists
if todu project list --format json | grep -q '"name": "todu-tests"'; then
    echo "Test project 'todu-tests' already exists. Skipping creation."
    exit 0
fi

# Create local test project
echo "Creating test project 'todu-tests'..."
todu project add \
    --name todu-tests \
    --system local \
    --description "Test project for todu-skills development and testing"

# Get the project ID
PROJECT_ID=$(todu project list --format json | grep -A 5 '"name": "todu-tests"' | grep '"id"' | head -1 | awk '{print $2}' | tr -d ',')

echo "Created test project with ID: $PROJECT_ID"

# Create sample tasks for fixture generation
echo "Creating sample tasks..."

todu task create \
    --project todu-tests \
    --title "Sample task for testing" \
    --description "This is a sample task created for testing and fixture generation" \
    --priority high \
    --label testing \
    --label sample

todu task create \
    --project todu-tests \
    --title "Another test task" \
    --description "Second sample task for testing list operations" \
    --priority medium \
    --label testing

todu task create \
    --project todu-tests \
    --title "Completed test task" \
    --description "A task that will be marked as done" \
    --status done

echo "Test environment setup complete!"
echo "Project: todu-tests"
echo "Run teardown.sh to clean up when done."
