"""
Recurring task utilities for todu.

Handles detection, creation, and querying of recurring tasks and their
completion history.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta

from id_registry import assign_id, lookup_id

ISSUES_DIR = Path.home() / ".local" / "todu" / "issues"


def is_recurring(task_data: Dict) -> bool:
    """
    Check if a task has recurring metadata.

    Args:
        task_data: The normalized task data dict

    Returns:
        True if task has 'recurring' object, False otherwise
    """
    return "recurring" in task_data and task_data["recurring"] is not None


def calculate_next_due(pattern: str, interval: int = 1, from_date: Optional[datetime] = None) -> str:
    """
    Calculate the next due date for a recurring task.

    Args:
        pattern: Recurrence pattern ('daily', 'weekly', 'monthly', 'yearly')
        interval: Number of pattern units between occurrences (default: 1)
        from_date: Starting date (defaults to now if not provided)

    Returns:
        ISO format date string for the next occurrence

    Raises:
        ValueError: If pattern is not recognized
    """
    if from_date is None:
        from_date = datetime.now(timezone.utc)

    # Ensure from_date is timezone-aware
    if from_date.tzinfo is None:
        from_date = from_date.replace(tzinfo=timezone.utc)

    # Calculate next due based on pattern
    if pattern == "daily":
        next_due = from_date + timedelta(days=interval)
    elif pattern == "weekly":
        next_due = from_date + timedelta(weeks=interval)
    elif pattern == "monthly":
        next_due = from_date + relativedelta(months=interval)
    elif pattern == "yearly":
        next_due = from_date + relativedelta(years=interval)
    else:
        raise ValueError(f"Unknown recurrence pattern: {pattern}")

    return next_due.isoformat()


def create_completion_record(task_data: Dict, completed_at: Optional[str] = None) -> Dict:
    """
    Create a completion record for a recurring task.

    This creates a NEW task record with:
    - New todu ID
    - Same systemData (links to original)
    - Status: 'done'
    - CompletedAt timestamp
    - Snapshot of task at completion time

    Args:
        task_data: The original recurring task data
        completed_at: ISO format timestamp, defaults to now

    Returns:
        The completion record dict with assigned todu ID

    Raises:
        ValueError: If task is not recurring
    """
    if not is_recurring(task_data):
        raise ValueError("Task is not recurring")

    # Use provided timestamp or current time
    if completed_at is None:
        completed_at = datetime.now(timezone.utc).isoformat()

    # Create completion record as a snapshot of the task
    completion = {
        "id": None,  # Will be assigned below
        "system": task_data["system"],
        "type": task_data["type"],
        "title": task_data["title"],
        "description": task_data.get("description", ""),
        "state": "closed",
        "status": "done",
        "url": task_data.get("url", ""),
        "createdAt": task_data.get("createdAt"),
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "completedAt": completed_at,
        "labels": task_data.get("labels", []),
        "assignees": task_data.get("assignees", []),
        "priority": task_data.get("priority"),
        "dueDate": task_data.get("dueDate"),
        "systemData": task_data["systemData"].copy(),  # Same systemData links records
    }

    # Save completion record to cache
    filename = _generate_completion_filename(task_data, completed_at)
    todu_id = assign_id(filename)
    completion["id"] = todu_id

    cache_file = ISSUES_DIR / filename
    ISSUES_DIR.mkdir(parents=True, exist_ok=True)

    with open(cache_file, 'w') as f:
        json.dump(completion, f, indent=2)

    return completion


def update_recurring_task(task_data: Dict, next_due: str, pattern: Optional[str] = None) -> Dict:
    """
    Update a recurring task with next occurrence information.

    Args:
        task_data: The original recurring task data
        next_due: ISO format date for next occurrence
        pattern: Optional recurrence pattern (if changed)

    Returns:
        Updated task data

    Raises:
        ValueError: If task is not recurring
    """
    if not is_recurring(task_data):
        raise ValueError("Task is not recurring")

    # Update due date
    task_data["dueDate"] = next_due

    # Update recurring object
    if "recurring" not in task_data:
        task_data["recurring"] = {}

    task_data["recurring"]["nextDue"] = next_due

    if pattern:
        task_data["recurring"]["pattern"] = pattern

    # Keep task open/pending
    task_data["state"] = "open"
    task_data["status"] = "open"

    # Remove completedAt if present
    if "completedAt" in task_data:
        del task_data["completedAt"]

    task_data["updatedAt"] = datetime.now(timezone.utc).isoformat()

    return task_data


def add_completion_to_history(task_data: Dict, completion_id: int, completed_at: str) -> Dict:
    """
    Add a completion entry to task's recurring.completions array.

    Args:
        task_data: The original recurring task data
        completion_id: The todu ID of the completion record
        completed_at: ISO format timestamp

    Returns:
        Updated task data with completion added to history
    """
    if "recurring" not in task_data:
        task_data["recurring"] = {}

    if "completions" not in task_data["recurring"]:
        task_data["recurring"]["completions"] = []

    # Add new completion to history
    task_data["recurring"]["completions"].append({
        "completedAt": completed_at,
        "completionId": completion_id
    })

    # Sort by completion date (most recent first)
    task_data["recurring"]["completions"].sort(
        key=lambda x: x["completedAt"],
        reverse=True
    )

    return task_data


def get_completion_history(system: str, system_data: Dict) -> List[Dict]:
    """
    Get all completion records for a recurring task.

    Searches for all tasks with matching system and systemData.

    Args:
        system: The system name (github, forgejo, todoist)
        system_data: The systemData dict to match

    Returns:
        List of completion records, sorted by completedAt (most recent first)
    """
    if not ISSUES_DIR.exists():
        return []

    completions = []

    for cache_file in ISSUES_DIR.glob(f'{system}-*.json'):
        try:
            with open(cache_file) as f:
                task = json.load(f)

            # Check if systemData matches and status is done
            if (task.get("system") == system and
                task.get("status") == "done" and
                _system_data_matches(task.get("systemData", {}), system_data)):
                completions.append(task)
        except (json.JSONDecodeError, IOError):
            continue

    # Sort by completion date (most recent first)
    completions.sort(
        key=lambda x: x.get("completedAt", ""),
        reverse=True
    )

    return completions


def get_recurring_task(system: str, system_data: Dict) -> Optional[Dict]:
    """
    Get the original recurring task (not a completion record).

    Args:
        system: The system name
        system_data: The systemData dict to match

    Returns:
        The recurring task dict, or None if not found
    """
    if not ISSUES_DIR.exists():
        return None

    for cache_file in ISSUES_DIR.glob(f'{system}-*.json'):
        try:
            with open(cache_file) as f:
                task = json.load(f)

            # Find task with matching systemData that is recurring and not completed
            if (task.get("system") == system and
                is_recurring(task) and
                task.get("status") != "done" and
                _system_data_matches(task.get("systemData", {}), system_data)):
                return task
        except (json.JSONDecodeError, IOError):
            continue

    return None


def _system_data_matches(data1: Dict, data2: Dict) -> bool:
    """
    Check if two systemData dicts represent the same task.

    For GitHub/Forgejo: Compare repo + number
    For Todoist: Compare task_id

    Args:
        data1: First systemData dict
        data2: Second systemData dict

    Returns:
        True if they match, False otherwise
    """
    # GitHub/Forgejo: match on repo + number
    if "repo" in data1 and "repo" in data2:
        return (data1.get("repo") == data2.get("repo") and
                data1.get("number") == data2.get("number"))

    # Todoist: match on task_id
    if "task_id" in data1 and "task_id" in data2:
        return data1.get("task_id") == data2.get("task_id")

    return False


def _generate_completion_filename(task_data: Dict, completed_at: str) -> str:
    """
    Generate a unique filename for a completion record.

    Format: {system}-{encoded_id}-completion-{timestamp}.json

    Args:
        task_data: The task data
        completed_at: ISO format timestamp

    Returns:
        Filename string
    """
    system = task_data["system"]
    system_data = task_data["systemData"]

    # Parse timestamp to get a short identifier
    try:
        dt = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
        timestamp = dt.strftime("%Y%m%d%H%M%S")
    except ValueError:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

    # Create encoded identifier based on system
    if system in ["github", "forgejo"]:
        repo = system_data.get("repo", "").replace("/", "_")
        number = system_data.get("number", "")
        encoded_id = f"{repo}-{number}"
    elif system == "todoist":
        task_id = system_data.get("task_id", "")
        encoded_id = task_id
    else:
        encoded_id = "unknown"

    return f"{system}-{encoded_id}-completion-{timestamp}.json"
