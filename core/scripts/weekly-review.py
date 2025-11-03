#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# requires-python = ">=3.9"
# ///

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

# Import cache loading functions from list-items.py
_list_items_path = Path(__file__).parent / "list-items.py"
_spec = importlib.util.spec_from_file_location("list_items", _list_items_path)
_list_items = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_list_items)

load_items_from_consolidated = _list_items.load_items_from_consolidated
load_items_from_legacy = _list_items.load_items_from_legacy


def load_all_tasks() -> List[Dict[str, Any]]:
    """Load all tasks/issues from consolidated cache with legacy fallback."""
    # Try consolidated structure first, fall back to legacy
    tasks = load_items_from_consolidated()
    if not tasks:
        tasks = load_items_from_legacy()
    return tasks


def load_project_registry() -> Dict[str, str]:
    """Load project registry and create a mapping from project ID to nickname."""
    projects_file = Path.home() / ".local" / "todu" / "projects.json"
    if not projects_file.exists():
        return {}

    try:
        with open(projects_file) as f:
            projects = json.load(f)

        # Create mapping: repo/project_id -> nickname
        project_map = {}
        for nickname, info in projects.items():
            repo = info.get("repo", "")
            if repo:
                project_map[repo] = nickname

        return project_map
    except:
        return {}


def get_project_name(task: Dict[str, Any], project_map: Dict[str, str]) -> str | None:
    """Get human-readable project name for a task."""
    system = task.get("system", "")
    system_data = task.get("systemData", {})

    if system == "github":
        repo = system_data.get("repo", "")
        return project_map.get(repo)
    elif system == "forgejo":
        repo = system_data.get("repo", "")
        return project_map.get(repo)
    elif system == "todoist":
        project_id = system_data.get("project_id", "")
        return project_map.get(project_id)

    return None


def get_system_identifier(task: Dict[str, Any]) -> str:
    """Extract system-specific identifier from task."""
    system = task.get("system", "")
    system_data = task.get("systemData", {})

    if system in ["github", "forgejo"]:
        # GitHub and Forgejo use issue numbers
        number = system_data.get("number")
        if number:
            return f"#{number}"
    elif system == "todoist":
        # Todoist uses task_id (UUID)
        task_id = system_data.get("task_id", "")
        if task_id:
            return task_id[:8]  # Show first 8 chars of UUID

    return ""


def parse_priority(task: Dict[str, Any]) -> str:
    """Extract priority level from task."""
    # Use standardized priority field (set by plugin during sync)
    priority = task.get("priority")
    if priority in ["high", "medium", "low"]:
        return priority

    # Fallback: check labels for priority:high/medium/low
    labels = task.get("labels", [])
    for label in labels:
        if label.startswith("priority:"):
            return label.split(":", 1)[1]

    return "none"


def has_status_label(task: Dict[str, Any], status: str) -> bool:
    """Check if task has a specific status label."""
    labels = task.get("labels", [])
    return f"status:{status}" in labels


def parse_due_date(task: Dict[str, Any]) -> datetime | None:
    """Extract due date from task."""
    # Use standardized dueDate field (set by plugin during sync)
    due_date_str = task.get("dueDate")
    if not due_date_str:
        return None

    try:
        # Parse ISO date string
        return datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
    except:
        return None


def to_local_date(dt: datetime, user_tz) -> datetime:
    """Convert datetime to user's local timezone."""
    if dt.tzinfo is None:
        # Assume UTC if no timezone info
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(user_tz)


def format_date(dt: datetime | None) -> str:
    """Format date for display."""
    if dt is None:
        return "-"
    return dt.strftime("%Y-%m-%d")


def get_week_range(date: datetime) -> tuple[datetime, datetime]:
    """Get Monday-Sunday range for the week containing date."""
    # Get Monday of the week
    monday = date - timedelta(days=date.weekday())
    monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)

    # Get Sunday of the week
    sunday = monday + timedelta(days=6, hours=23, minutes=59, seconds=59)

    return monday, sunday


def generate_weekly_review(tasks: List[Dict[str, Any]], user_tz, project_map: Dict[str, str], week_date: datetime | None = None) -> str:
    """Generate weekly task review organized by status and priority."""
    if week_date is None:
        week_date = datetime.now(user_tz)

    monday, sunday = get_week_range(week_date)

    # Filter tasks by categories
    waiting = []
    next_tasks = []
    active = []
    backlog = []
    completed = []
    canceled = []

    for task in tasks:
        status = task.get("status", "")
        priority = parse_priority(task)

        # Waiting: status:waiting label
        if has_status_label(task, "waiting") and status not in ["done", "closed", "canceled"]:
            waiting.append(task)

        # Next: priority:high
        if priority == "high" and status not in ["done", "closed", "canceled"]:
            next_tasks.append(task)

        # Active: priority:medium
        if priority == "medium" and status not in ["done", "closed", "canceled"]:
            active.append(task)

        # Backlog: priority:low OR no priority (none)
        if (priority == "low" or priority == "none") and status not in ["done", "closed", "canceled"]:
            backlog.append(task)

        # Completed this week
        if status in ["done", "closed"]:
            completed_at_str = task.get("completedAt")
            if completed_at_str:
                try:
                    completed_at = datetime.fromisoformat(completed_at_str.replace('Z', '+00:00'))
                    completed_at_local = to_local_date(completed_at, user_tz)
                    if monday <= completed_at_local <= sunday:
                        completed.append((task, completed_at_local))
                except:
                    pass

        # Canceled this week
        if status == "canceled":
            updated_at_str = task.get("updatedAt")
            if updated_at_str:
                try:
                    updated_at = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
                    updated_at_local = to_local_date(updated_at, user_tz)
                    if monday <= updated_at_local <= sunday:
                        canceled.append((task, updated_at_local))
                except:
                    pass

    # Generate markdown report
    lines = [
        f"# Weekly Review: {monday.strftime('%m-%d-%Y')} to {sunday.strftime('%m-%d-%Y')}",
        "",
        "*This is a read-only report. Checkboxes are for visual reference only and are not interactive.*",
        "",
        "## Summary",
        f"- **Waiting**: {len(waiting)} tasks",
        f"- **Next**: {len(next_tasks)} tasks",
        f"- **Active**: {len(active)} tasks",
        f"- **Backlog**: {len(backlog)} tasks",
        f"- **Completed**: {len(completed)} tasks",
        f"- **Cancelled**: {len(canceled)} tasks",
        ""
    ]

    # Helper function to format a task item
    def format_task(task: Dict[str, Any], show_due: bool = True, show_priority: bool = False) -> List[str]:
        system = task.get("system", "")
        todu_id = task.get("id", "")
        system_id = get_system_identifier(task)
        title = task.get("title", "")
        priority = parse_priority(task)
        assignees = ", ".join(task.get("assignees", []))
        due = format_date(parse_due_date(task))
        url = task.get("url", "")
        project = get_project_name(task, project_map)

        result = [f"- [ ] **#{todu_id} - {title}**"]

        meta = [f"System: {system}"]
        if project:
            meta.append(f"Project: {project}")
        if system_id:
            meta.append(f"System ID: {system_id}")
        if show_priority and priority != "none":
            meta.append(f"Priority: {priority}")
        if assignees:
            meta.append(f"Assignee: {assignees}")
        if show_due and due != "-":
            meta.append(f"Due: {due}")

        result.append(f"  {' • '.join(meta)}")
        result.append(f"  {url}")
        result.append("")

        return result

    # Waiting section
    if waiting:
        lines.append("## 🔒 Waiting ({})".format(len(waiting)))
        lines.append("")
        # Sort by project name
        waiting.sort(key=lambda t: get_project_name(t, project_map) or "")
        for task in waiting:
            lines.extend(format_task(task, show_priority=True))

    # Next section
    if next_tasks:
        lines.append("## 🔥 Next ({})".format(len(next_tasks)))
        lines.append("")
        # Sort by project name
        next_tasks.sort(key=lambda t: get_project_name(t, project_map) or "")
        for task in next_tasks:
            lines.extend(format_task(task))

    # Active section
    if active:
        lines.append("## 🚧 Active ({})".format(len(active)))
        lines.append("")
        # Sort by project name
        active.sort(key=lambda t: get_project_name(t, project_map) or "")
        for task in active:
            lines.extend(format_task(task))

    # Backlog section
    if backlog:
        lines.append("## 📋 Backlog ({})".format(len(backlog)))
        lines.append("")
        # Sort by project name
        backlog.sort(key=lambda t: get_project_name(t, project_map) or "")
        for task in backlog:
            lines.extend(format_task(task, show_due=False))

    # Completed section
    if completed:
        lines.append("## ✅ Completed This Week ({})".format(len(completed)))
        lines.append("")
        # Sort by project name, then completion date
        completed.sort(key=lambda x: (get_project_name(x[0], project_map) or "", x[1]))
        for task, completed_at in completed:
            system = task.get("system", "")
            todu_id = task.get("id", "")
            system_id = get_system_identifier(task)
            title = task.get("title", "")
            completed_date = completed_at.strftime("%Y-%m-%d")
            assignees = ", ".join(task.get("assignees", []))
            labels = [l for l in task.get("labels", []) if not l.startswith("status:") and not l.startswith("priority:")]
            url = task.get("url", "")
            project = get_project_name(task, project_map)

            lines.append(f"- [x] **#{todu_id} - {title}**")
            meta = [f"System: {system}"]
            if project:
                meta.append(f"Project: {project}")
            if system_id:
                meta.append(f"System ID: {system_id}")
            meta.append(f"Completed: {completed_date}")
            if assignees:
                meta.append(f"Assignee: {assignees}")
            if labels:
                meta.append(f"Labels: {', '.join(labels)}")
            lines.append(f"  {' • '.join(meta)}")
            lines.append(f"  {url}")
            lines.append("")

    # Canceled section
    if canceled:
        lines.append("## ❌ Cancelled This Week ({})".format(len(canceled)))
        lines.append("")
        # Sort by project name, then cancellation date
        canceled.sort(key=lambda x: (get_project_name(x[0], project_map) or "", x[1]))
        for task, canceled_at in canceled:
            system = task.get("system", "")
            todu_id = task.get("id", "")
            system_id = get_system_identifier(task)
            title = task.get("title", "")
            canceled_date = canceled_at.strftime("%Y-%m-%d")
            assignees = ", ".join(task.get("assignees", []))
            labels = [l for l in task.get("labels", []) if not l.startswith("status:") and not l.startswith("priority:")]
            url = task.get("url", "")
            project = get_project_name(task, project_map)

            lines.append(f"**#{todu_id} - {title}**")
            meta = [f"System: {system}"]
            if project:
                meta.append(f"Project: {project}")
            if system_id:
                meta.append(f"System ID: {system_id}")
            meta.append(f"Cancelled: {canceled_date}")
            if assignees:
                meta.append(f"Assignee: {assignees}")
            if labels:
                meta.append(f"Labels: {', '.join(labels)}")
            lines.append(f"  {' • '.join(meta)}")
            lines.append(f"  {url}")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate weekly review from cached tasks')
    parser.add_argument('--output', help='Output file path (default: stdout)')
    parser.add_argument('--week', help='Week date (YYYY-MM-DD) for weekly review (default: current week)')

    args = parser.parse_args()

    # Get user's local timezone
    user_tz = datetime.now().astimezone().tzinfo

    # Load all tasks
    tasks = load_all_tasks()

    if not tasks:
        print("Warning: No tasks found in cache. Run sync commands first.", file=sys.stderr)
        return 1

    # Load project registry
    project_map = load_project_registry()

    # Generate report
    week_date = None
    if args.week:
        try:
            week_date = datetime.fromisoformat(args.week).replace(tzinfo=user_tz)
        except:
            print(f"Error: Invalid week date format: {args.week}", file=sys.stderr)
            return 1

    report = generate_weekly_review(tasks, user_tz, project_map, week_date)

    # Output report
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"Report saved to: {output_path}")
    else:
        print(report)

    return 0


if __name__ == '__main__':
    sys.exit(main())
