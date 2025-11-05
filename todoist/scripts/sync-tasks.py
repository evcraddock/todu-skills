#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "todoist-api-python>=2.1.0",
# ]
# requires-python = ">=3.9"
# ///

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from todoist_api_python.api import TodoistAPI

# Add path to core scripts for sync_manager, id_registry, and recurring
core_scripts_path = Path(__file__).parent.parent.parent / "core" / "scripts"
sys.path.insert(0, str(core_scripts_path))
from sync_manager import update_sync_metadata
from id_registry import assign_id, lookup_id
from recurring import (
    is_recurring,
    create_completion_record,
    update_recurring_task,
    add_completion_to_history,
    get_recurring_task,
    calculate_next_due
)

CACHE_DIR = Path.home() / ".local" / "todu" / "todoist"
ITEMS_DIR = Path.home() / ".local" / "todu" / "issues"

# Priority mapping: Todoist 1-4 to our labels
PRIORITY_TO_LABEL = {
    4: "priority:high",    # Urgent
    3: "priority:medium",  # High
    2: "priority:low",     # Medium
    1: None                # Normal (no label)
}

def normalize_task(task):
    """Convert Todoist task to normalized format."""
    # Convert Todoist priority to label
    priority_label = PRIORITY_TO_LABEL.get(task.priority)
    task_labels = task.labels if task.labels else []
    if priority_label:
        task_labels.append(priority_label)

    # Convert datetime objects to ISO format strings
    created_at = task.created_at.isoformat() if task.created_at else None
    updated_at = task.updated_at.isoformat() if hasattr(task, 'updated_at') and task.updated_at else created_at

    # Convert due date if present
    due_date = None
    if task.due:
        if hasattr(task.due, 'date'):
            due_date = task.due.date.isoformat() if hasattr(task.due.date, 'isoformat') else str(task.due.date)
        else:
            due_date = str(task.due)

    # Determine normalized status from labels
    # Priority: status:canceled > status:done > status:waiting > status:in-progress > status:backlog > default
    status = "open"
    if task.is_completed:
        # Check for status labels to determine the actual status
        if "status:canceled" in task_labels:
            status = "canceled"
        elif "status:done" in task_labels:
            status = "done"
        else:
            # Completed but no status label, default to done
            status = "done"
    else:
        # Not completed, check for waiting, in-progress, or backlog
        if "status:waiting" in task_labels:
            status = "waiting"
        elif "status:in-progress" in task_labels:
            status = "in-progress"
        elif "status:backlog" in task_labels:
            status = "backlog"

    # Add completedAt timestamp for completed tasks
    completed_at = None
    if status in ["done", "canceled"]:
        # Use completed_at if available, otherwise fall back to updated_at
        if hasattr(task, 'completed_at') and task.completed_at:
            completed_at = task.completed_at.isoformat() if hasattr(task.completed_at, 'isoformat') else str(task.completed_at)
        else:
            completed_at = updated_at

    # Standardized priority field
    priority_value = None
    if task.priority == 4:
        priority_value = "high"
    elif task.priority == 3:
        priority_value = "medium"
    elif task.priority == 2:
        priority_value = "low"

    normalized = {
        "id": None,  # Will be assigned below
        "system": "todoist",
        "type": "task",
        "title": task.content,
        "description": task.description or "",
        "state": "closed" if task.is_completed else "open",  # System-level state
        "status": status,  # Workflow-level status from labels
        "url": task.url,
        "createdAt": created_at,
        "updatedAt": updated_at,
        "labels": task_labels,
        "assignees": [],  # Todoist tasks are personal
        "priority": priority_value,  # Standardized priority field
        "dueDate": due_date,  # Standardized due date field
        "systemData": {
            "task_id": task.id,  # Moved UUID here
            "project_id": task.project_id,
            "priority": task.priority,
            "due": due_date,
            "is_completed": task.is_completed
        }
    }

    # Only include completedAt if the task is completed
    if completed_at:
        normalized["completedAt"] = completed_at

    # Add recurring metadata if task is recurring
    if task.due and hasattr(task.due, 'is_recurring') and task.due.is_recurring:
        # Parse recurrence pattern
        pattern = "unknown"
        interval = 1

        # Extract pattern from due.string (e.g., "every week", "every 2 days")
        if hasattr(task.due, 'string') and task.due.string:
            recurrence_str = task.due.string.lower()
            if "every day" in recurrence_str or "daily" in recurrence_str:
                pattern = "daily"
            elif "every week" in recurrence_str or "weekly" in recurrence_str:
                pattern = "weekly"
            elif "every month" in recurrence_str or "monthly" in recurrence_str:
                pattern = "monthly"
            elif "every year" in recurrence_str or "yearly" in recurrence_str:
                pattern = "yearly"
            else:
                pattern = recurrence_str

        # Calculate next due if not already set or if task was just completed
        next_due = due_date
        if not next_due:
            # No due date from Todoist, calculate based on creation date
            created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            next_due = calculate_next_due(pattern, interval, created_dt)

        normalized["recurring"] = {
            "pattern": pattern,
            "interval": interval,
            "nextDue": next_due,
            "completions": []
        }

    return normalized

def sync_tasks(project_id=None, task_id=None):
    """Sync Todoist tasks to local cache."""
    token = os.environ.get('TODOIST_TOKEN')
    if not token:
        print(json.dumps({"error": "TODOIST_TOKEN environment variable not set"}), file=sys.stderr)
        sys.exit(1)

    try:
        api = TodoistAPI(token)

        # Create cache directories
        ITEMS_DIR.mkdir(parents=True, exist_ok=True)

        # Fetch tasks based on mode
        if task_id:
            # Single task mode
            try:
                task = api.get_task(task_id)
                tasks = [task]
                sync_mode = "single"
            except Exception as e:
                print(json.dumps({"error": f"Failed to fetch task {task_id}: {str(e)}"}), file=sys.stderr)
                return 1
        else:
            # Full sync mode (get all active tasks)
            # Note: Todoist API by default returns only active (non-completed) tasks
            # get_tasks() returns a ResultsPaginator that yields pages (lists) of tasks
            tasks_result = api.get_tasks(project_id=project_id) if project_id else api.get_tasks()
            # Flatten the pages into a single list of tasks
            tasks = []
            for page in tasks_result:
                tasks.extend(page)
            sync_mode = "full"

        new_count = 0
        updated_count = 0

        for task in tasks:
            filename = f"todoist-{task.id}.json"
            task_file = ITEMS_DIR / filename
            is_new = not task_file.exists()

            # Load existing task if it exists
            existing_task = None
            if not is_new:
                try:
                    with open(task_file, 'r') as f:
                        existing_task = json.load(f)
                except (json.JSONDecodeError, IOError):
                    pass

            # Save normalized task
            normalized = normalize_task(task)

            # Check if this is a recurring task that was just completed
            # For Todoist: detect completion by due date advancement (task stays open)
            if (existing_task and
                is_recurring(existing_task) and
                existing_task.get("dueDate") and
                normalized.get("dueDate") and
                existing_task["dueDate"] != normalized["dueDate"]):
                # Due date advanced! Task was completed
                # Use the old due date as the completion date
                completion_date = existing_task["dueDate"]

                completion = create_completion_record(
                    existing_task,
                    completion_date + "T23:59:59Z"  # End of the due date
                )

                # Add completion to history
                if "recurring" in existing_task:
                    normalized["recurring"] = existing_task["recurring"].copy()
                    add_completion_to_history(
                        normalized,
                        completion["id"],
                        completion_date + "T23:59:59Z"
                    )
            # Also check for non-recurring tasks that transitioned to completed
            elif (existing_task and
                  not is_recurring(existing_task) and
                  not existing_task.get("completedAt") and
                  normalized.get("completedAt")):
                # Non-recurring task was completed (keep existing logic)
                pass

            # Assign or reuse todu ID
            if is_new:
                # New task: assign new todu ID
                todu_id = assign_id(filename)
            else:
                # Existing task: look up existing todu ID
                todu_id = lookup_id(filename)
                if todu_id is None:
                    # File exists but not in registry (shouldn't happen, but handle it)
                    todu_id = assign_id(filename)

            normalized["id"] = todu_id

            with open(task_file, 'w') as f:
                json.dump(normalized, f, indent=2)

            if is_new:
                new_count += 1
            else:
                updated_count += 1

        # Update sync metadata in unified file
        update_sync_metadata(
            system="todoist",
            mode=sync_mode,
            task_count=new_count + updated_count,
            stats={
                "new": new_count,
                "updated": updated_count,
                "total": new_count + updated_count
            },
            project_id=project_id
        )

        # Return stats
        result = {
            "synced": new_count + updated_count,
            "new": new_count,
            "updated": updated_count,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        print(json.dumps(result, indent=2))
        return 0

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        return 1

def main():
    parser = argparse.ArgumentParser(description='Sync Todoist tasks to local cache')
    parser.add_argument('--project-id', help='Filter tasks by project ID')
    parser.add_argument('--task-id', help='Sync a single task by ID')

    args = parser.parse_args()

    return sync_tasks(project_id=args.project_id, task_id=args.task_id)

if __name__ == '__main__':
    sys.exit(main())
