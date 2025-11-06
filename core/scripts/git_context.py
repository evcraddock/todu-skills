"""
Git context extraction for todu.

Extracts git repository information from the current directory.
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


def run_git_command(args: List[str], cwd: Optional[Path] = None) -> Optional[str]:
    """Run a git command and return output.

    Args:
        args: Git command arguments
        cwd: Working directory (default: current)

    Returns:
        Command output or None if command fails
    """
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def parse_repo_from_remote(remote_url: str) -> Optional[str]:
    """Parse owner/repo from git remote URL.

    Args:
        remote_url: Git remote URL (SSH or HTTPS)

    Returns:
        "owner/repo" string or None if parsing fails

    Examples:
        git@github.com:evcraddock/todu.git -> evcraddock/todu
        https://github.com/evcraddock/todu.git -> evcraddock/todu
        git@forgejo.caradoc.com:erik/Vault.git -> erik/Vault
    """
    # Remove .git suffix if present
    url = remote_url
    if url.endswith('.git'):
        url = url[:-4]

    # SSH format: git@host:owner/repo
    ssh_match = re.match(r'git@[^:]+:(.+)', url)
    if ssh_match:
        return ssh_match.group(1)

    # HTTPS format: https://host/owner/repo
    https_match = re.match(r'https?://[^/]+/(.+)', url)
    if https_match:
        return https_match.group(1)

    return None


def detect_system_from_remote(remote_url: str) -> Optional[str]:
    """Detect task management system from remote URL.

    Args:
        remote_url: Git remote URL

    Returns:
        System name (github, forgejo) or None
    """
    if 'github.com' in remote_url:
        return 'github'
    elif 'forgejo' in remote_url or 'gitea' in remote_url or 'codeberg' in remote_url:
        return 'forgejo'
    return None


def get_base_url_from_remote(remote_url: str) -> Optional[str]:
    """Extract base URL from remote for Forgejo instances.

    Args:
        remote_url: Git remote URL

    Returns:
        Base URL or None
    """
    # Extract host from SSH or HTTPS URL
    ssh_match = re.match(r'git@([^:]+):', remote_url)
    if ssh_match:
        host = ssh_match.group(1)
        return f'https://{host}'

    https_match = re.match(r'(https?://[^/]+)', remote_url)
    if https_match:
        return https_match.group(1)

    return None


def get_git_context(cwd: Optional[Path] = None) -> Optional[Dict]:
    """Extract git context from current directory.

    Args:
        cwd: Working directory (default: current)

    Returns:
        {
            "repo": "owner/repo",
            "system": "github|forgejo",
            "base_url": "https://...",  # for forgejo
            "remote_url": "git@...",
            "branch": "main",
            "commits": [...],  # last 5 commits
            "modified_files": [...],
            "is_git_repo": True
        }
        or None if not a git repository
    """
    # Check if we're in a git repository
    git_dir = run_git_command(['rev-parse', '--git-dir'], cwd)
    if not git_dir:
        return None

    # Get remote URL
    remote_url = run_git_command(['remote', 'get-url', 'origin'], cwd)
    if not remote_url:
        # No origin remote, but still a git repo
        return {
            'is_git_repo': True,
            'repo': None,
            'system': None,
            'base_url': None,
            'remote_url': None,
            'branch': run_git_command(['branch', '--show-current'], cwd),
            'commits': [],
            'modified_files': []
        }

    # Parse repo info
    repo = parse_repo_from_remote(remote_url)
    system = detect_system_from_remote(remote_url)
    base_url = get_base_url_from_remote(remote_url) if system == 'forgejo' else None

    # Get current branch
    branch = run_git_command(['branch', '--show-current'], cwd)

    # Get recent commits
    commits_output = run_git_command(['log', '--oneline', '-5'], cwd)
    commits = commits_output.split('\n') if commits_output else []

    # Get modified files
    status_output = run_git_command(['status', '--short'], cwd)
    modified_files = status_output.split('\n') if status_output else []
    # Filter out empty lines
    modified_files = [f for f in modified_files if f]

    return {
        'is_git_repo': True,
        'repo': repo,
        'system': system,
        'base_url': base_url,
        'remote_url': remote_url,
        'branch': branch,
        'commits': commits,
        'modified_files': modified_files
    }


def is_git_repository(cwd: Optional[Path] = None) -> bool:
    """Check if current directory is a git repository.

    Args:
        cwd: Working directory (default: current)

    Returns:
        True if in a git repository
    """
    return run_git_command(['rev-parse', '--git-dir'], cwd) is not None


def get_repo_identifier(cwd: Optional[Path] = None) -> Optional[str]:
    """Get repo identifier (owner/repo) from current git directory.

    Args:
        cwd: Working directory (default: current)

    Returns:
        "owner/repo" string or None
    """
    context = get_git_context(cwd)
    return context['repo'] if context else None
