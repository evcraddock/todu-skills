#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "rumps>=0.4.0",
#   "watchdog>=3.0.0"
# ]
# requires-python = ">=3.9"
# ///

"""
macOS Menu Bar App for Todu Task Visibility

Displays task counts and provides quick access to task management functions.
"""

import sys
import subprocess
import tempfile
import threading
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional

import rumps
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add core scripts to path
CORE_SCRIPTS = Path(__file__).parent.parent / "core" / "scripts"
sys.path.insert(0, str(CORE_SCRIPTS))

# Import from existing scripts
from report import (
    load_all_tasks,
    load_project_registry,
    parse_priority,
    parse_due_date,
    to_local_date,
    get_project_name,
    generate_daily_report,
    generate_weekly_report
)

CACHE_DIR = Path.home() / ".local" / "todu"
ISSUES_DIR = CACHE_DIR / "issues"


class TaskData:
    """Holds task count statistics."""

    def __init__(self):
        self.in_progress = 0
        self.waiting = 0
        self.high_priority = 0
        self.due_today = 0
        self.overdue = 0
        self.projects: Dict[str, int] = {}
        self.total_open = 0


class CacheFileHandler(FileSystemEventHandler):
    """Watches for changes in the todu cache directory."""

    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            self.callback()

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            self.callback()

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            self.callback()


class ToduMenuBar(rumps.App):
    """macOS Menu Bar Application for Todu."""

    def __init__(self):
        super(ToduMenuBar, self).__init__("Todu", "☑️")
        self.menu = [
            "In Progress: ...",
            "Next: ...",
            rumps.separator,
            "Due Today: ...",
            rumps.separator,
            rumps.MenuItem("Projects", callback=None),
            rumps.separator,
            "⟳ Sync Now",
            "📊 Daily Review",
            "📅 Weekly Review",
            rumps.separator,
        ]

        self.task_data = TaskData()
        self.user_tz = datetime.now().astimezone().tzinfo
        self.observer = None

        # Initial load
        self.update_task_data()

        # Set up file watching
        self.setup_file_watching()

        # Set up timer fallback (refresh every 60 seconds)
        self.timer = rumps.Timer(self.timer_callback, 60)
        self.timer.start()

    def setup_file_watching(self):
        """Set up file system watching for cache directory."""
        if not ISSUES_DIR.exists():
            ISSUES_DIR.mkdir(parents=True, exist_ok=True)

        event_handler = CacheFileHandler(self.update_task_data)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(ISSUES_DIR), recursive=False)
        self.observer.start()

    def timer_callback(self, _):
        """Fallback timer to refresh data every 60 seconds."""
        self.update_task_data()

    def update_task_data(self):
        """Load and categorize tasks from cache."""
        try:
            tasks = load_all_tasks()
            project_map = load_project_registry()

            if not tasks:
                self.title = "📋 0"
                self.update_menu_items(TaskData())
                return

            data = TaskData()
            now = datetime.now(self.user_tz)
            today = now.date()

            # Count tasks by category
            for task in tasks:
                status = task.get("status", "")
                priority = parse_priority(task)

                # Skip closed/canceled tasks for most counts
                if status in ["done", "closed", "canceled"]:
                    continue

                data.total_open += 1

                # In Progress (status:in-progress, but not waiting)
                if status == "in-progress":
                    data.in_progress += 1

                # Waiting (status:waiting)
                if status == "waiting":
                    data.waiting += 1

                # High Priority (priority = high)
                if priority == "high":
                    data.high_priority += 1

                # Due today / Overdue
                due_date = parse_due_date(task)
                if due_date:
                    due_local = to_local_date(due_date, self.user_tz).date()
                    if due_local == today:
                        data.due_today += 1
                    elif due_local < today:
                        data.overdue += 1

                # Projects
                project = get_project_name(task, project_map)
                if project:
                    data.projects[project] = data.projects.get(project, 0) + 1

            self.task_data = data

            # Update title with in-progress count
            self.title = f"☑️ {data.in_progress}"

            # Update menu
            self.update_menu_items(data)

        except Exception as e:
            print(f"Error updating task data: {e}", file=sys.stderr)
            self.title = "☑️ !"

    def update_menu_items(self, data: TaskData):
        """Update menu items with current counts."""
        # Update counts
        self.menu["In Progress: ..."].title = f"In Progress: {data.in_progress} tasks"
        self.menu["Next: ..."].title = f"Next: {data.high_priority} tasks"
        self.menu["Due Today: ..."].title = f"Due Today: {data.due_today}"

        # Update or create overdue if needed
        # First, remove any existing "Overdue:" items (handles duplicates from bug)
        keys_to_remove = [k for k in self.menu.keys() if k.startswith("Overdue:")]
        for key in keys_to_remove:
            del self.menu[key]

        if data.overdue > 0:
            # Insert new overdue item before Projects
            self.menu.insert_before("Projects", rumps.MenuItem(f"Overdue: {data.overdue}", callback=None))

        # Update projects submenu - rebuild it each time
        # Remove old Projects menu
        if "Projects" in self.menu:
            del self.menu["Projects"]

        # Create new Projects submenu
        projects_menu = rumps.MenuItem("Projects")

        if data.projects:
            sorted_projects = sorted(data.projects.items(), key=lambda x: x[1], reverse=True)
            for project, count in sorted_projects:
                projects_menu.add(rumps.MenuItem(f"• {project} ({count} open)", callback=None))
        else:
            projects_menu.add(rumps.MenuItem("No projects", callback=None))

        # Insert Projects menu before the separator
        self.menu.insert_before("⟳ Sync Now", projects_menu)

    def _run_sync_background(self):
        """Run sync in a background thread to avoid blocking UI."""
        try:
            sync_script = CORE_SCRIPTS / "sync_manager.py"
            if not sync_script.exists():
                print("Error: Sync script not found", file=sys.stderr)
                return

            # Run sync and wait for completion
            result = subprocess.run(
                ["python3", str(sync_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                rumps.notification(
                    title="Todu Sync",
                    subtitle="Sync completed",
                    message="Tasks updated successfully"
                )
            else:
                print(f"Sync failed: {result.stderr}", file=sys.stderr)
                rumps.notification(
                    title="Todu Sync",
                    subtitle="Sync failed",
                    message="Check console for details"
                )

        except Exception as e:
            print(f"Sync error: {e}", file=sys.stderr)

    @rumps.clicked("⟳ Sync Now")
    def sync_now(self, _):
        """Trigger manual sync of all systems."""
        # Start sync in background thread to avoid blocking UI
        thread = threading.Thread(target=self._run_sync_background, daemon=True)
        thread.start()

        rumps.notification(
            title="Todu Sync",
            subtitle="Sync started",
            message="Syncing tasks from all systems..."
        )

    def _generate_daily_review_background(self):
        """Generate daily review and save to ~/Vault/Daily-Review.md."""
        try:
            tasks = load_all_tasks()
            if not tasks:
                print("Warning: No tasks found in cache", file=sys.stderr)
                rumps.notification(
                    title="Todu Daily Review",
                    subtitle="No tasks",
                    message="No tasks found. Run sync first."
                )
                return

            project_map = load_project_registry()
            report = generate_daily_report(tasks, self.user_tz, project_map)

            # Save to ~/Vault/Daily-Review.md
            vault_path = Path.home() / "Vault" / "Daily-Review.md"
            vault_path.parent.mkdir(parents=True, exist_ok=True)

            with open(vault_path, 'w') as f:
                f.write(report)

            # Open in Obsidian using obsidian:// URI
            # Format: obsidian://open?vault=VaultName&file=FileName.md
            import urllib.parse
            vault_name = "Vault"  # Your vault name
            file_path = "Daily-Review.md"
            obsidian_uri = f"obsidian://open?vault={urllib.parse.quote(vault_name)}&file={urllib.parse.quote(file_path)}"

            subprocess.run(["open", obsidian_uri])

            rumps.notification(
                title="Todu Daily Review",
                subtitle="Review saved",
                message=f"Opening in Obsidian..."
            )

        except Exception as e:
            print(f"Daily review error: {e}", file=sys.stderr)
            rumps.notification(
                title="Todu Daily Review",
                subtitle="Error",
                message=str(e)
            )

    @rumps.clicked("📊 Daily Review")
    def daily_review(self, _):
        """Generate and save daily review to ~/Vault/Daily-Review.md."""
        # Start daily review generation in background thread
        thread = threading.Thread(target=self._generate_daily_review_background, daemon=True)
        thread.start()

    def _run_weekly_review_background(self):
        """Run weekly review script and save to ~/Vault/Weekly-Review.md."""
        try:
            weekly_review_script = CORE_SCRIPTS / "weekly-review.py"
            if not weekly_review_script.exists():
                print("Error: Weekly review script not found", file=sys.stderr)
                rumps.notification(
                    title="Todu Weekly Review",
                    subtitle="Error",
                    message="Weekly review script not found"
                )
                return

            vault_path = Path.home() / "Vault" / "Weekly-Review.md"

            # Run weekly review script with output to Vault
            result = subprocess.run(
                ["python3", str(weekly_review_script), "--output", str(vault_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                # Open in Obsidian using obsidian:// URI
                import urllib.parse
                vault_name = "Vault"  # Your vault name
                file_path = "Weekly-Review.md"
                obsidian_uri = f"obsidian://open?vault={urllib.parse.quote(vault_name)}&file={urllib.parse.quote(file_path)}"

                subprocess.run(["open", obsidian_uri])

                rumps.notification(
                    title="Todu Weekly Review",
                    subtitle="Review saved",
                    message=f"Opening in Obsidian..."
                )
            else:
                print(f"Weekly review failed: {result.stderr}", file=sys.stderr)
                rumps.notification(
                    title="Todu Weekly Review",
                    subtitle="Failed",
                    message="Check console for details"
                )

        except Exception as e:
            print(f"Weekly review error: {e}", file=sys.stderr)
            rumps.notification(
                title="Todu Weekly Review",
                subtitle="Error",
                message=str(e)
            )

    @rumps.clicked("📅 Weekly Review")
    def weekly_review(self, _):
        """Run weekly review skill and save to ~/Vault/Weekly-Review.md."""
        # Start weekly review in background thread
        thread = threading.Thread(target=self._run_weekly_review_background, daemon=True)
        thread.start()

    def cleanup(self):
        """Clean up resources before quitting."""
        if self.observer:
            self.observer.stop()
            self.observer.join()


def main():
    """Run the menu bar app."""
    app = ToduMenuBar()
    try:
        app.run()
    finally:
        app.cleanup()


if __name__ == "__main__":
    main()
