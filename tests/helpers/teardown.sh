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

# Safety check: Ensure we're running against localhost
API_URL=$(todu config show | grep -i "url" | awk '{print $NF}')
if [[ ! "$API_URL" =~ ^http://localhost ]]; then
    echo "Error: API URL is not localhost"
    echo "Found: $API_URL"
    echo "Teardown can only be run against localhost for safety"
    exit 1
fi

cd "$TEST_DIR"

# Get all project IDs and remove them
echo "Removing all test projects..."
PROJECT_IDS=$(todu project list --format json | grep '"id"' | awk '{print $2}' | tr -d ',')

if [ -z "$PROJECT_IDS" ]; then
    echo "No projects to clean up."
    exit 0
fi

for PROJECT_ID in $PROJECT_IDS; do
    PROJECT_NAME=$(todu project list --format json | grep -A 10 "\"id\": $PROJECT_ID" | grep '"name"' | head -1 | awk -F'"' '{print $4}')
    echo "Removing project '$PROJECT_NAME' (ID: $PROJECT_ID)..."
    todu project remove "$PROJECT_ID" --cascade --force
done

# Remove test systems
echo "Removing test systems..."
if todu system list --format json | grep -q '"identifier": "github"'; then
    GITHUB_SYSTEM_ID=$(todu system list --format json | grep -B 1 '"identifier": "github"' | grep '"id"' | awk '{print $2}' | tr -d ',')
    echo "Removing GitHub test system (ID: $GITHUB_SYSTEM_ID)..."
    todu system remove "$GITHUB_SYSTEM_ID" --force
fi

if todu system list --format json | grep -q '"identifier": "forgejo"'; then
    FORGEJO_SYSTEM_ID=$(todu system list --format json | grep -B 1 '"identifier": "forgejo"' | grep '"id"' | awk '{print $2}' | tr -d ',')
    echo "Removing Forgejo test system (ID: $FORGEJO_SYSTEM_ID)..."
    todu system remove "$FORGEJO_SYSTEM_ID" --force
fi

echo "Test environment teardown complete!"
