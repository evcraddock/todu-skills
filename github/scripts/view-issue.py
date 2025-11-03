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
from datetime import datetime
from github import Github, Auth

# Add path to core scripts for id_registry
core_scripts_path = Path(__file__).parent.parent.parent / "core" / "scripts"
sys.path.insert(0, str(core_scripts_path))
from id_registry import lookup_filename

def format_issue_markdown(issue, comments, repo_name):
    """Format issue and comments as markdown."""
    lines = []

    # Title
    lines.append(f"# Issue #{issue.number}: {issue.title}")
    lines.append("")

    # Metadata
    lines.append(f"**System:** GitHub")
    lines.append(f"**Repository:** {repo_name}")
    lines.append(f"**Status:** {issue.state}")
    if issue.labels:
        labels = ", ".join([label.name for label in issue.labels])
        lines.append(f"**Labels:** {labels}")
    if issue.assignees:
        assignees = ", ".join([assignee.login for assignee in issue.assignees])
        lines.append(f"**Assignees:** {assignees}")
    lines.append(f"**Created:** {issue.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Updated:** {issue.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**URL:** {issue.html_url}")
    lines.append("")

    # Description
    lines.append("## Description")
    lines.append("")
    lines.append(issue.body or "*No description provided*")
    lines.append("")

    # Comments
    if comments:
        lines.append("## Comments")
        lines.append("")
        for comment in comments:
            lines.append(f"### {comment.user.login} commented on {comment.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append("")
            lines.append(comment.body)
            lines.append("")
    else:
        lines.append("## Comments")
        lines.append("")
        lines.append("*No comments*")
        lines.append("")

    return "\n".join(lines)

def view_issue(repo_name, issue_number):
    """Fetch and display issue with all comments."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print(json.dumps({"error": "GITHUB_TOKEN environment variable not set"}), file=sys.stderr)
        sys.exit(1)

    try:
        gh = Github(auth=Auth.Token(token))
        repo = gh.get_repo(repo_name)

        # Fetch issue
        issue = repo.get_issue(issue_number)

        # Check if it's a pull request
        if issue.pull_request:
            print(json.dumps({"error": f"Issue #{issue_number} is a pull request, not an issue"}), file=sys.stderr)
            return 1

        # Fetch all comments
        comments = list(issue.get_comments())

        # Format as markdown
        markdown = format_issue_markdown(issue, comments, repo_name)
        print(markdown)

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
    parser = argparse.ArgumentParser(description='View GitHub issue with all comments')
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
        # Expected format: github-owner_repo-number.json
        if not filename.startswith('github-'):
            print(json.dumps({"error": f"Todu ID {args.id} is not a GitHub issue"}), file=sys.stderr)
            return 1

        # Extract repo and issue number from filename
        parts = filename.replace('github-', '').replace('.json', '').rsplit('-', 1)
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
