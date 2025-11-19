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

# Setup test systems (github and forgejo)
echo "Setting up test systems..."
if ! todu system list --format json | grep -q '"identifier": "github"'; then
    echo "Creating GitHub test system..."
    todu system add --identifier github --name github --url https://githubtest.local
fi

if ! todu system list --format json | grep -q '"identifier": "forgejo"'; then
    echo "Creating Forgejo test system..."
    todu system add --identifier forgejo --name forgejo --url https://forgejotest.local
fi

# Check if todu-tests project already exists
if todu project list --format json | grep -q '"name": "todu-tests"'; then
    echo "Test project 'todu-tests' already exists. Skipping creation."
    exit 0
fi

# Create test projects for each system
echo "Creating test projects..."

# Local test project
echo "Creating local test project 'todu-tests'..."
todu project add \
    --name todu-tests \
    --system local \
    --description "Test project for todu-skills development and testing"

# GitHub test project
echo "Creating GitHub test project 'test-github-repo'..."
todu project add \
    --name test-github-repo \
    --system github \
    --external-id "testuser/test-repo" \
    --description "Test GitHub repository"

# Forgejo test project
echo "Creating Forgejo test project 'test-forgejo-repo'..."
todu project add \
    --name test-forgejo-repo \
    --system forgejo \
    --external-id "testuser/forgejo-repo" \
    --description "Test Forgejo repository"

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
