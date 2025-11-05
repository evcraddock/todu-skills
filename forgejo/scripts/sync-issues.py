#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "requests>=2.31.0",
# ]
# requires-python = ">=3.9"
# ///

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone
import requests

# Import shared utilities
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from label_utils import get_forgejo_url as shared_get_forgejo_url, get_base_url_from_registry

# Add path to core scripts for sync_manager, id_registry, and recurring
core_scripts_path = Path(__file__).parent.parent.parent / "core" / "scripts"
sys.path.insert(0, str(core_scripts_path))
from sync_manager import update_sync_metadata
from id_registry import assign_id, lookup_id
from recurring import (
    is_recurring,
    create_completion_record,
    add_completion_to_history,
    calculate_next_due,
    update_recurring_task
)

CACHE_DIR = Path.home() / ".local" / "todu" / "forgejo"
ITEMS_DIR = Path.home() / ".local" / "todu" / "issues"

def get_forgejo_url(cwd=None):
    """Wrapper for shared get_forgejo_url that supports cwd parameter."""
    return shared_get_forgejo_url(repo_name=None, cwd=cwd)

def normalize_issue(issue, repo_name):
    """Convert Forgejo issue to normalized format."""
    # Extract status from status:* label, fallback to state
    labels = [label['name'] for label in issue.get('labels', [])]
    status = None
    for label in labels:
        if label.startswith('status:'):
            status = label.split(':', 1)[1]
            break

    # If no status label, derive from Forgejo state
    if not status:
        status = "open" if issue['state'] == "open" else "closed"

    # Add completedAt timestamp for completed issues (NOT canceled)
    completed_at = None
    if status in ["closed", "done"]:
        # Use closed_at if available, otherwise fall back to updated_at
        if issue.get('closed_at'):
            completed_at = issue['closed_at']
        else:
            completed_at = issue['updated_at']

    # Extract standardized priority from labels
    priority = None
    for label in labels:
        if label.startswith("priority:"):
            priority = label.split(":", 1)[1]
            break

    normalized = {
        "id": None,  # Will be assigned below
        "system": "forgejo",
        "type": "issue",
        "title": issue['title'],
        "description": issue['body'] or "",
        "state": issue['state'],  # System-level state: "open" or "closed"
        "status": status,  # Workflow-level status from labels
        "url": issue['html_url'],
        "createdAt": issue['created_at'],
        "updatedAt": issue['updated_at'],
        "labels": labels,
        "assignees": [assignee['login'] for assignee in (issue.get('assignees') or [])],
        "priority": priority,  # Standardized priority field
        "dueDate": None,  # Forgejo issues don't have due dates
        "systemData": {
            "repo": repo_name,
            "number": issue['number'],
            "state": issue['state'],
            "state_reason": issue.get('state_reason', None)
        }
    }

    # Only include completedAt if the issue is completed
    if completed_at:
        normalized["completedAt"] = completed_at

    # Check for recurring labels (e.g., "recurring:weekly", "recurring:daily")
    recurring_pattern = None
    for label in labels:
        if label.startswith("recurring:"):
            recurring_pattern = label.split(":", 1)[1]
            break

    # Add recurring metadata if labeled as recurring
    if recurring_pattern:
        # Parse interval from pattern
        interval = 1
        pattern = recurring_pattern

        # Simple pattern normalization
        if "daily" in pattern or "day" in pattern:
            pattern = "daily"
        elif "weekly" in pattern or "week" in pattern:
            pattern = "weekly"
        elif "monthly" in pattern or "month" in pattern:
            pattern = "monthly"
        elif "yearly" in pattern or "year" in pattern:
            pattern = "yearly"

        # Calculate next due date based on creation date
        created_at = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
        next_due = calculate_next_due(pattern, interval, created_at)

        normalized["recurring"] = {
            "pattern": pattern,
            "interval": interval,
            "nextDue": next_due,
            "completions": []
        }

        # Set dueDate to match nextDue
        normalized["dueDate"] = next_due

    return normalized

def sync_issues(repo_name, since=None, issue_number=None, base_url=None):
    """Sync Forgejo issues to local cache."""
    token = os.environ.get('FORGEJO_TOKEN')
    if not token:
        print(json.dumps({"error": "FORGEJO_TOKEN environment variable not set"}), file=sys.stderr)
        sys.exit(1)

    if not base_url:
        # Try to get from projects registry first
        base_url = get_base_url_from_registry(repo_name)

    if not base_url:
        # Fall back to git remote detection
        base_url = get_forgejo_url()

    try:
        headers = {
            'Authorization': f'token {token}',
            'Content-Type': 'application/json'
        }

        # Create cache directory
        ITEMS_DIR.mkdir(parents=True, exist_ok=True)

        # Use repo name prefix in filename to avoid conflicts
        # Replace '/' with '_' for valid filename
        repo_prefix = repo_name.replace('/', '_')

        # Fetch issues based on mode
        if issue_number:
            # Single issue mode
            api_url = f"{base_url}/api/v1/repos/{repo_name}/issues/{issue_number}"
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            issue = response.json()

            # Check if it's a pull request
            if issue.get('pull_request'):
                print(json.dumps({"error": f"Issue #{issue_number} is a pull request, not an issue"}), file=sys.stderr)
                return 1

            issues = [issue]
            sync_mode = "single"
        else:
            # Full or incremental sync mode
            api_url = f"{base_url}/api/v1/repos/{repo_name}/issues"
            params = {
                'state': 'all',
                'page': 1,
                'limit': 100
            }

            if since:
                params['since'] = since.isoformat()
                sync_mode = "incremental"
            else:
                sync_mode = "full"

            issues = []
            while True:
                response = requests.get(api_url, headers=headers, params=params)
                response.raise_for_status()
                page_issues = response.json()

                if not page_issues:
                    break

                # Filter out pull requests
                issues.extend([i for i in page_issues if not i.get('pull_request')])

                params['page'] += 1

        new_count = 0
        updated_count = 0

        for issue in issues:
            # Use system and repo prefix in filename to avoid conflicts
            filename = f"forgejo-{repo_prefix}-{issue['number']}.json"
            issue_file = ITEMS_DIR / filename
            is_new = not issue_file.exists()

            # Load existing issue if it exists
            existing_issue = None
            if not is_new:
                try:
                    with open(issue_file, 'r') as f:
                        existing_issue = json.load(f)
                except (json.JSONDecodeError, IOError):
                    pass

            # Save normalized issue
            normalized = normalize_issue(issue, repo_name)

            # Check if this is a recurring issue that was just completed
            if (existing_issue and
                is_recurring(existing_issue) and
                not existing_issue.get("completedAt") and
                normalized.get("completedAt")):
                # Recurring issue was completed! Create completion record
                completion = create_completion_record(
                    existing_issue,
                    normalized.get("completedAt")
                )

                # Add completion to history
                if "recurring" in existing_issue:
                    normalized["recurring"] = existing_issue["recurring"].copy()
                    add_completion_to_history(
                        normalized,
                        completion["id"],
                        normalized.get("completedAt")
                    )

                # Calculate next due date and reopen the task
                pattern = normalized["recurring"]["pattern"]
                interval = normalized["recurring"].get("interval", 1)
                # Use local system time, not UTC
                from_date = datetime.now()
                next_due = calculate_next_due(pattern, interval, from_date)

                # Update task for next occurrence
                normalized = update_recurring_task(normalized, next_due, pattern)

                # Reopen the issue in Forgejo
                try:
                    reopen_url = f'{base_url}/api/v1/repos/{repo_name}/issues/{issue["number"]}'
                    reopen_data = {'state': 'open'}
                    reopen_response = requests.patch(reopen_url, headers=headers, json=reopen_data)
                    if reopen_response.status_code == 201:
                        print(f"Reopened recurring issue #{issue['number']} for next occurrence", file=sys.stderr)
                    else:
                        print(f"Warning: Could not reopen issue #{issue['number']}: {reopen_response.status_code}", file=sys.stderr)
                except Exception as e:
                    print(f"Warning: Could not reopen issue #{issue['number']}: {e}", file=sys.stderr)

            # Assign or reuse todu ID
            if is_new:
                # New issue: assign new todu ID
                todu_id = assign_id(filename)
            else:
                # Existing issue: look up existing todu ID
                todu_id = lookup_id(filename)
                if todu_id is None:
                    # File exists but not in registry (shouldn't happen, but handle it)
                    todu_id = assign_id(filename)

            normalized["id"] = todu_id

            with open(issue_file, 'w') as f:
                json.dump(normalized, f, indent=2)

            if is_new:
                new_count += 1
            else:
                updated_count += 1

        # Update sync metadata in unified file
        update_sync_metadata(
            system="forgejo",
            mode=sync_mode,
            task_count=new_count + updated_count,
            repo=repo_name
        )

        result = {
            "synced": new_count + updated_count,
            "new": new_count,
            "updated": updated_count,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mode": sync_mode
        }

        # Add issue number for single issue sync
        if issue_number:
            result["issue"] = f"#{issue_number}"

        print(json.dumps(result, indent=2))
        return 0

    except requests.exceptions.RequestException as e:
        import traceback
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_msg = f"{error_msg}: {e.response.text}"
        error_info = {
            "error": error_msg,
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
        print(json.dumps(error_info), file=sys.stderr)
        return 1
    except Exception as e:
        import traceback
        error_info = {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
        print(json.dumps(error_info), file=sys.stderr)
        return 1

def main():
    parser = argparse.ArgumentParser(description='Sync Forgejo issues to local cache')
    parser.add_argument('--repo', required=True, help='Repository in owner/name format')
    parser.add_argument('--since', help='ISO timestamp to fetch issues since')
    parser.add_argument('--issue', type=int, help='Sync specific issue number')
    parser.add_argument('--base-url', help='Forgejo base URL (e.g., https://forgejo.example.com)')

    args = parser.parse_args()

    # Make --issue and --since mutually exclusive
    if args.issue and args.since:
        parser.error("Cannot specify both --issue and --since")

    since = datetime.fromisoformat(args.since.replace('Z', '+00:00')) if args.since else None

    return sync_issues(args.repo, since, args.issue, args.base_url)

if __name__ == '__main__':
    sys.exit(main())
