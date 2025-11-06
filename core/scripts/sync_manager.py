#!/usr/bin/env python3
"""
Shared sync metadata management for todu.

Manages sync metadata in the projects.json file, providing per-project
sync tracking instead of per-system tracking.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


# Projects file location
PROJECTS_FILE = Path.home() / ".local" / "todu" / "projects.json"


def read_projects() -> Dict[str, Any]:
    """
    Read the projects registry file.

    Returns:
        Dictionary with all registered projects.
        Returns empty dict if file doesn't exist.
    """
    if not PROJECTS_FILE.exists():
        return {}

    try:
        with open(PROJECTS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def write_projects(projects: Dict[str, Any]) -> None:
    """
    Write the projects registry file.

    Args:
        projects: Dictionary of all projects to write
    """
    # Ensure parent directory exists
    PROJECTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write to file
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=2)


def find_project_by_repo(system: str, repo: str) -> Optional[str]:
    """
    Find project nickname by system and repo identifier.

    Args:
        system: System name ('github', 'forgejo', or 'todoist')
        repo: Repository identifier (e.g., 'owner/repo' or project_id)

    Returns:
        Project nickname if found, None otherwise
    """
    projects = read_projects()

    for nickname, info in projects.items():
        if info.get('system') == system and info.get('repo') == repo:
            return nickname

    return None


def update_sync_metadata(
    system: str,
    mode: str,
    task_count: int,
    stats: Optional[Dict[str, int]] = None,
    project_id: Optional[str] = None,
    repo: Optional[str] = None
) -> None:
    """
    Update sync metadata for a specific project.

    Args:
        system: System name ('github', 'forgejo', or 'todoist')
        mode: Sync mode ('full', 'incremental', or 'single')
        task_count: Total number of tasks/issues synced
        stats: Optional detailed stats dict with 'new', 'updated', 'total' keys
        project_id: Optional Todoist project ID (deprecated, use repo)
        repo: Repository identifier to find the project
    """
    # For Todoist, project_id is the repo identifier
    if system == 'todoist' and project_id and not repo:
        repo = project_id

    # If no repo provided, we can't update per-project metadata
    if not repo:
        return

    # Find the project by repo
    nickname = find_project_by_repo(system, repo)
    if not nickname:
        # Project not registered, skip updating metadata
        return

    # Read existing projects
    projects = read_projects()

    # Update the project's sync metadata
    if nickname in projects:
        projects[nickname]["lastSync"] = datetime.now(timezone.utc).isoformat()
        projects[nickname]["lastSyncMode"] = mode
        projects[nickname]["taskCount"] = task_count

        # Add optional stats
        if stats:
            projects[nickname]["stats"] = stats

    # Write back to file
    write_projects(projects)


def get_project_sync_metadata(nickname: str) -> Optional[Dict[str, Any]]:
    """
    Get sync metadata for a specific project.

    Args:
        nickname: Project nickname

    Returns:
        Project's full info dict including sync metadata, or None if not found
    """
    projects = read_projects()
    return projects.get(nickname)


def get_all_projects_sync_metadata() -> Dict[str, Any]:
    """
    Get sync metadata for all projects.

    Returns:
        Dictionary of all projects with their sync metadata
    """
    return read_projects()
