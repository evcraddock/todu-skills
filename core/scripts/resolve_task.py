"""
Task resolution for todu.

Resolves task identifiers (unified ID, system-specific ID, or description)
to the system, repo, and issue number.
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from id_registry import lookup_filename

CACHE_DIR = Path.home() / ".local" / "todu"
ISSUES_DIR = CACHE_DIR / "issues"


class AmbiguousTaskError(Exception):
    """Raised when multiple tasks match the query."""

    def __init__(self, matches: List[Dict]):
        self.matches = matches
        super().__init__(f"Multiple tasks match ({len(matches)})")


def load_task_from_cache(filename: str) -> Optional[Dict]:
    """Load task data from cache file.

    Args:
        filename: The cache filename (e.g., "github-evcraddock_todu-11.json")

    Returns:
        Task data dict or None if not found
    """
    cache_file = ISSUES_DIR / filename

    if not cache_file.exists():
        return None

    try:
        with open(cache_file) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def parse_filename(filename: str) -> Optional[Dict]:
    """Parse a cache filename into components.

    Args:
        filename: Cache filename like "github-evcraddock_todu-11.json"

    Returns:
        Dict with system, repo, number or None if invalid format
    """
    # Remove .json extension
    name = filename.replace('.json', '')

    # Split on last hyphen to get number
    parts = name.rsplit('-', 1)
    if len(parts) != 2:
        return None

    prefix, number_str = parts

    # Split on first hyphen to get system
    system_repo = prefix.split('-', 1)
    if len(system_repo) != 2:
        return None

    system, repo_encoded = system_repo

    # Decode repo (underscores are slashes)
    repo = repo_encoded.replace('_', '/')

    try:
        number = int(number_str)
    except ValueError:
        return None

    return {
        'system': system,
        'repo': repo,
        'number': number
    }


def search_tasks_by_description(query: str) -> List[Dict]:
    """Search for tasks by description/title.

    Args:
        query: Search query string

    Returns:
        List of matching task dicts
    """
    if not ISSUES_DIR.exists():
        return []

    query_lower = query.lower()
    matches = []

    for cache_file in ISSUES_DIR.glob('*.json'):
        try:
            with open(cache_file) as f:
                task = json.load(f)

            # Search in title and description
            title = task.get('title', '').lower()
            description = task.get('description', '').lower()

            if query_lower in title or query_lower in description:
                # Parse filename to get system/repo/number
                parsed = parse_filename(cache_file.name)
                if parsed:
                    matches.append({
                        'id': task.get('id'),
                        'system': parsed['system'],
                        'repo': parsed['repo'],
                        'number': parsed['number'],
                        'title': task.get('title'),
                        'state': task.get('state'),
                        'url': task.get('url')
                    })
        except (json.JSONDecodeError, IOError):
            continue

    return matches


def resolve_task(identifier: str) -> Dict:
    """Resolve task identifier to system + repo + issue.

    Args:
        identifier:
            - "20" (unified ID)
            - "github #15" (system-specific)
            - "auth bug" (description search)

    Returns:
        {
            "unified_id": 20,
            "system": "github|forgejo|todoist",
            "repo": "owner/repo",
            "number": 15,
            "title": "...",
            "url": "...",
            "filename": "github-evcraddock_todu-11.json"
        }

    Raises:
        ValueError: If task not found
        AmbiguousTaskError: If multiple tasks match
    """
    # Try as unified ID
    if identifier.isdigit():
        unified_id = int(identifier)
        filename = lookup_filename(unified_id)

        if filename:
            # Load from cache to get details
            task = load_task_from_cache(filename)
            if task:
                parsed = parse_filename(filename)
                if parsed:
                    return {
                        'unified_id': unified_id,
                        'system': parsed['system'],
                        'repo': parsed['repo'],
                        'number': parsed['number'],
                        'title': task.get('title'),
                        'state': task.get('state'),
                        'url': task.get('url'),
                        'filename': filename
                    }

    # Try as system-specific: "github #15"
    if ' ' in identifier:
        parts = identifier.split(' ', 1)
        if len(parts) == 2:
            system, num_part = parts
            num_str = num_part.lstrip('#')

            if num_str.isdigit():
                number = int(num_str)

                # Search through cache for matching system + number
                for cache_file in ISSUES_DIR.glob(f'{system}-*.json'):
                    parsed = parse_filename(cache_file.name)
                    if parsed and parsed['number'] == number:
                        task = load_task_from_cache(cache_file.name)
                        if task:
                            return {
                                'unified_id': task.get('id'),
                                'system': parsed['system'],
                                'repo': parsed['repo'],
                                'number': parsed['number'],
                                'title': task.get('title'),
                                'state': task.get('state'),
                                'url': task.get('url'),
                                'filename': cache_file.name
                            }

    # Try as description search
    matches = search_tasks_by_description(identifier)

    if len(matches) == 0:
        raise ValueError(f"Task not found: '{identifier}'")

    if len(matches) == 1:
        return matches[0]

    # Multiple matches - raise error with options
    raise AmbiguousTaskError(matches)


def get_task_details(unified_id: int) -> Optional[Dict]:
    """Get full task details from unified ID.

    Args:
        unified_id: The todu unified ID

    Returns:
        Full task data or None if not found
    """
    filename = lookup_filename(unified_id)
    if not filename:
        return None

    return load_task_from_cache(filename)
