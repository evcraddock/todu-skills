#!/usr/bin/env python3
"""Shared utilities for managing Forgejo labels and base URL resolution."""

import json
import os
import subprocess
from pathlib import Path
import requests

# Valid status and priority values
VALID_STATUSES = ["backlog", "in-progress", "waiting", "done", "canceled"]
VALID_PRIORITIES = ["low", "medium", "high"]

# Label color scheme
LABEL_COLORS = {
    "status:backlog": "#d4c5f9",
    "status:in-progress": "#fbca04",
    "status:waiting": "#fef2c0",
    "status:done": "#0e8a16",
    "status:canceled": "#d93f0b",
    "priority:low": "#0075ca",
    "priority:medium": "#a2eeef",
    "priority:high": "#d73a4a"
}


def load_projects():
    """Load projects from projects.json."""
    projects_file = Path.home() / ".local" / "todu" / "projects.json"
    if not projects_file.exists():
        return {}
    try:
        with open(projects_file) as f:
            return json.load(f)
    except Exception:
        return {}


def get_base_url_from_registry(repo_name):
    """Get base URL for a Forgejo repo from projects registry."""
    projects = load_projects()
    for nickname, info in projects.items():
        if info.get('system') == 'forgejo' and info.get('repo') == repo_name:
            return info.get('baseUrl')
    return None


def get_forgejo_url(repo_name=None, cwd=None):
    """Get Forgejo base URL from projects registry, environment, or git remote.

    Args:
        repo_name: Repository in owner/repo format (optional)
        cwd: Working directory for git commands (optional)

    Returns:
        str: Base URL for Forgejo instance
    """
    # First try projects registry if repo_name provided
    if repo_name:
        base_url = get_base_url_from_registry(repo_name)
        if base_url:
            return base_url.rstrip('/')

    # Then check environment variable
    if os.environ.get('FORGEJO_URL'):
        return os.environ['FORGEJO_URL'].rstrip('/')

    # Try to extract from git remote
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd
        )
        remote_url = result.stdout.strip()

        # Parse URL to extract base domain
        # Handle both SSH and HTTPS URLs
        if remote_url.startswith('ssh://git@'):
            # SSH format: ssh://git@forgejo.example.com/owner/repo.git
            host = remote_url.replace('ssh://git@', '').split('/')[0]
            base_url = f"https://{host}"
        elif remote_url.startswith('git@'):
            # SSH format: git@forgejo.example.com:owner/repo.git
            host = remote_url.split('@')[1].split(':')[0]
            base_url = f"https://{host}"
        elif remote_url.startswith('http'):
            # HTTPS format: https://forgejo.example.com/owner/repo.git
            from urllib.parse import urlparse
            parsed = urlparse(remote_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
        else:
            base_url = None

        # Reject github.com
        if base_url and 'github.com' in base_url:
            print(json.dumps({
                "error": "This appears to be a GitHub repository, not Forgejo",
                "help": "Use the github plugin for GitHub repositories"
            }), file=sys.stderr)
            import sys
            sys.exit(1)

        if base_url:
            return base_url
    except Exception:
        pass

    print(json.dumps({
        "error": "Could not detect Forgejo URL from git remote",
        "help": "Make sure you are in a git repository with a Forgejo remote"
    }), file=sys.stderr)
    import sys
    sys.exit(1)


def ensure_labels_exist(base_url, headers, repo_name, required_labels):
    """Ensure required labels exist in the repository, creating them if necessary.

    Args:
        base_url: Forgejo base URL (e.g., "https://forgejo.example.com")
        headers: Request headers with authorization
        repo_name: Repository in "owner/repo" format
        required_labels: List of label names to ensure exist

    Returns:
        dict: Mapping of label names to their IDs
    """
    label_map = {}

    try:
        # Get existing labels
        api_url = f"{base_url}/api/v1/repos/{repo_name}/labels"
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        existing_labels = response.json()

        # Build name -> ID mapping for existing labels
        for label in existing_labels:
            label_map[label['name']] = label['id']

        # Create missing labels
        for label_name in required_labels:
            if label_name not in label_map:
                color = LABEL_COLORS.get(label_name, "#ededed")
                description = f"Auto-created label for {label_name}"

                create_payload = {
                    "name": label_name,
                    "color": color.lstrip('#'),
                    "description": description
                }

                create_response = requests.post(api_url, headers=headers, json=create_payload)
                create_response.raise_for_status()
                new_label = create_response.json()
                label_map[label_name] = new_label['id']
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_msg = f"{error_msg}: {e.response.text}"
        # Don't fail if label creation fails - return what we have
        pass
    except Exception:
        # Don't fail if label creation fails - return what we have
        pass

    return label_map


def get_label_ids(base_url, headers, repo_name, label_names):
    """Get label IDs from label names.

    Args:
        base_url: Forgejo base URL (e.g., "https://forgejo.example.com")
        headers: Request headers with authorization
        repo_name: Repository in "owner/repo" format
        label_names: List of label names to get IDs for

    Returns:
        list: List of label IDs
    """
    if not label_names:
        return []

    try:
        api_url = f"{base_url}/api/v1/repos/{repo_name}/labels"
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        all_labels = response.json()

        # Build name -> ID mapping
        label_map = {label['name']: label['id'] for label in all_labels}

        # Convert names to IDs
        label_ids = []
        for name in label_names:
            if name in label_map:
                label_ids.append(label_map[name])

        return label_ids
    except Exception:
        return []
