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
from datetime import datetime
import requests

# Import shared utilities
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from label_utils import get_forgejo_url

# Add path to core scripts for id_registry
core_scripts_path = Path(__file__).parent.parent.parent / "core" / "scripts"
sys.path.insert(0, str(core_scripts_path))
from id_registry import lookup_filename

def format_issue_markdown(issue, comments, repo_name):
    """Format issue and comments as markdown."""
    lines = []

    # Title
    lines.append(f"# Issue #{issue['number']}: {issue['title']}")
    lines.append("")

    # Metadata
    lines.append(f"**System:** Forgejo")
    lines.append(f"**Repository:** {repo_name}")
    lines.append(f"**Status:** {issue['state']}")
    if issue.get('labels'):
        labels = ", ".join([label['name'] for label in issue['labels']])
        lines.append(f"**Labels:** {labels}")
    if issue.get('assignees'):
        assignees = ", ".join([assignee['login'] for assignee in issue['assignees']])
        lines.append(f"**Assignees:** {assignees}")

    created_at = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
    updated_at = datetime.fromisoformat(issue['updated_at'].replace('Z', '+00:00'))
    lines.append(f"**Created:** {created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Updated:** {updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**URL:** {issue['html_url']}")
    lines.append("")

    # Description
    lines.append("## Description")
    lines.append("")
    lines.append(issue.get('body') or "*No description provided*")
    lines.append("")

    # Comments
    if comments:
        lines.append("## Comments")
        lines.append("")
        for comment in comments:
            comment_date = datetime.fromisoformat(comment['created_at'].replace('Z', '+00:00'))
            lines.append(f"### {comment['user']['login']} commented on {comment_date.strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append("")
            lines.append(comment['body'])
            lines.append("")
    else:
        lines.append("## Comments")
        lines.append("")
        lines.append("*No comments*")
        lines.append("")

    return "\n".join(lines)

def view_issue(repo_name, issue_number):
    """Fetch and display issue with all comments."""
    token = os.environ.get('FORGEJO_TOKEN')
    if not token:
        print(json.dumps({"error": "FORGEJO_TOKEN environment variable not set"}), file=sys.stderr)
        sys.exit(1)

    base_url = get_forgejo_url(repo_name)

    try:
        headers = {
            'Authorization': f'token {token}',
            'Content-Type': 'application/json'
        }

        # Fetch issue
        issue_url = f"{base_url}/api/v1/repos/{repo_name}/issues/{issue_number}"
        response = requests.get(issue_url, headers=headers)
        response.raise_for_status()
        issue = response.json()

        # Check if it's a pull request
        if issue.get('pull_request'):
            print(json.dumps({"error": f"Issue #{issue_number} is a pull request, not an issue"}), file=sys.stderr)
            return 1

        # Fetch all comments
        comments_url = f"{base_url}/api/v1/repos/{repo_name}/issues/{issue_number}/comments"
        response = requests.get(comments_url, headers=headers)
        response.raise_for_status()
        comments = response.json()

        # Format as markdown
        markdown = format_issue_markdown(issue, comments, repo_name)
        print(markdown)

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
    parser = argparse.ArgumentParser(description='View Forgejo issue with all comments')
    parser.add_argument('--repo', help='Repository in owner/name format')
    parser.add_argument('--issue', type=int, help='Issue number')
    parser.add_argument('--id', type=int, help='Todu ID to look up')

    args = parser.parse_args()

    # Handle todu ID lookup
    if args.id:
        # Look up filename from todu ID
        filename = lookup_filename(args.id)
        if not filename:
            print(json.dumps({"error": f"Todu ID {args.id} not found in registry"}), file=sys.stderr)
            return 1

        # Parse filename to extract repo and issue number
        # Expected format: forgejo-owner_repo-number.json
        if not filename.startswith('forgejo-'):
            print(json.dumps({"error": f"Todu ID {args.id} is not a Forgejo issue"}), file=sys.stderr)
            return 1

        # Extract repo and issue number from filename
        parts = filename.replace('forgejo-', '').replace('.json', '').rsplit('-', 1)
        if len(parts) != 2:
            print(json.dumps({"error": f"Invalid filename format: {filename}"}), file=sys.stderr)
            return 1

        repo_name = parts[0].replace('_', '/')
        issue_number = int(parts[1])

        return view_issue(repo_name, issue_number)

    # Traditional repo + issue lookup
    if not args.repo or not args.issue:
        parser.error("Either --id or both --repo and --issue must be specified")

    return view_issue(args.repo, args.issue)

if __name__ == '__main__':
    sys.exit(main())
