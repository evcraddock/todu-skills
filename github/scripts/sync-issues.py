#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "PyGithub>=2.1.1",
# ]
# requires-python = ">=3.9"
# ///

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from github import Github, Auth

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

CACHE_DIR = Path.home() / ".local" / "todu" / "github"
ITEMS_DIR = Path.home() / ".local" / "todu" / "issues"

def normalize_issue(issue, repo_name):
    """Convert GitHub issue to normalized format."""
    # Extract label names first
    label_names = [label.name for label in issue.labels]

    # Extract standardized status from labels
    status = None
    for label in label_names:
        if label.startswith("status:"):
            status = label.split(":", 1)[1]
            break

    # Fall back to GitHub state if no status label
    if not status:
        status = "open" if issue.state == "open" else "closed"

    # Add completedAt timestamp for completed issues (NOT canceled)
    completed_at = None
    if issue.state == "closed" and status not in ["canceled"]:
        # Use closed_at if available, otherwise fall back to updated_at
        if hasattr(issue, 'closed_at') and issue.closed_at:
            completed_at = issue.closed_at.isoformat()
        else:
            completed_at = issue.updated_at.isoformat()

    # Extract standardized priority from labels
    priority = None
    for label in label_names:
        if label.startswith("priority:"):
            priority = label.split(":", 1)[1]
            break

    normalized = {
        "id": None,  # Will be assigned below
        "system": "github",
        "type": "issue",
        "title": issue.title,
        "description": issue.body or "",
        "state": issue.state,  # System-level state: "open" or "closed"
        "status": status,  # Workflow-level status from labels
        "url": issue.html_url,
        "createdAt": issue.created_at.isoformat(),
        "updatedAt": issue.updated_at.isoformat(),
        "labels": label_names,
        "assignees": [assignee.login for assignee in issue.assignees],
        "priority": priority,  # Standardized priority field
        "dueDate": None,  # GitHub issues don't have due dates
        "systemData": {
            "repo": repo_name,
            "number": issue.number,
            "state": issue.state,
            "state_reason": getattr(issue, 'state_reason', None)
        }
    }

    # Only include completedAt if the issue is closed
    if completed_at:
        normalized["completedAt"] = completed_at

    # Check for recurring labels (e.g., "recurring:weekly", "recurring:daily")
    recurring_pattern = None
    for label in label_names:
        if label.startswith("recurring:"):
            recurring_pattern = label.split(":", 1)[1]
            break

    # Add recurring metadata if labeled as recurring
    if recurring_pattern:
        # Parse interval from pattern (e.g., "every-2-weeks" -> interval=2, pattern="weekly")
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
        next_due = calculate_next_due(pattern, interval, issue.created_at)

        normalized["recurring"] = {
            "pattern": pattern,
            "interval": interval,
            "nextDue": next_due,
            "completions": []
        }

        # Set dueDate to match nextDue
        normalized["dueDate"] = next_due

    return normalized

def sync_issues(repo_name, since=None, issue_number=None):
    """Sync GitHub issues to local cache."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print(json.dumps({"error": "GITHUB_TOKEN environment variable not set"}), file=sys.stderr)
        sys.exit(1)

    try:
        gh = Github(auth=Auth.Token(token))
        repo = gh.get_repo(repo_name)

        # Create cache directories
        ITEMS_DIR.mkdir(parents=True, exist_ok=True)

        # Use repo name prefix in filename to avoid conflicts
        # Replace '/' with '_' for valid filename
        repo_prefix = repo_name.replace('/', '_')

        # Fetch issues based on mode
        if issue_number:
            # Single issue mode
            issue = repo.get_issue(issue_number)
            if issue.pull_request:
                print(json.dumps({"error": f"Issue #{issue_number} is a pull request, not an issue"}), file=sys.stderr)
                return 1
            issues = [issue]
            sync_mode = "single"
        elif since:
            # Incremental sync mode
            issues = repo.get_issues(state='all', since=since)
            sync_mode = "incremental"
        else:
            # Full sync mode
            issues = repo.get_issues(state='all')
            sync_mode = "full"

        new_count = 0
        updated_count = 0

        for issue in issues:
            # Skip pull requests
            if issue.pull_request:
                continue

            # Use system and repo prefix in filename to avoid conflicts
            filename = f"github-{repo_prefix}-{issue.number}.json"
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

                # Reopen the issue in GitHub
                try:
                    repo.get_issue(issue.number).edit(state="open")
                    print(f"Reopened recurring issue #{issue.number} for next occurrence", file=sys.stderr)
                except Exception as e:
                    print(f"Warning: Could not reopen issue #{issue.number}: {e}", file=sys.stderr)

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
            system="github",
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
    parser = argparse.ArgumentParser(description='Sync GitHub issues to local cache')
    parser.add_argument('--repo', required=True, help='Repository in owner/name format')
    parser.add_argument('--since', help='ISO timestamp to fetch issues since')
    parser.add_argument('--issue', type=int, help='Sync specific issue number')

    args = parser.parse_args()

    # Make --issue and --since mutually exclusive
    if args.issue and args.since:
        parser.error("Cannot specify both --issue and --since")

    since = datetime.fromisoformat(args.since.replace('Z', '+00:00')) if args.since else None

    return sync_issues(args.repo, since, args.issue)

if __name__ == '__main__':
    sys.exit(main())
