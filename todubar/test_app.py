#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "rumps>=0.4.0",
#   "watchdog>=3.0.0"
# ]
# requires-python = ">=3.9"
# ///

"""
Test script to validate menu bar app functionality without launching GUI.
"""

import sys
from pathlib import Path

# Add core scripts to path
CORE_SCRIPTS = Path(__file__).parent.parent / "core" / "scripts"
sys.path.insert(0, str(CORE_SCRIPTS))

def test_imports():
    """Test that all required imports work."""
    print("Testing imports...")
    try:
        import rumps
        print("✓ rumps imported")
    except ImportError as e:
        print(f"✗ rumps import failed: {e}")
        return False

    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        print("✓ watchdog imported")
    except ImportError as e:
        print(f"✗ watchdog import failed: {e}")
        return False

    try:
        from report import (
            load_all_tasks,
            load_project_registry,
            parse_priority,
            parse_due_date,
            to_local_date,
            get_project_name,
            generate_daily_report
        )
        print("✓ report functions imported")
    except ImportError as e:
        print(f"✗ report import failed: {e}")
        return False

    return True


def test_data_loading():
    """Test loading task data."""
    print("\nTesting data loading...")
    from report import load_all_tasks, load_project_registry

    tasks = load_all_tasks()
    print(f"✓ Loaded {len(tasks)} tasks from cache")

    project_map = load_project_registry()
    print(f"✓ Loaded {len(project_map)} projects from registry")

    return True


def test_task_categorization():
    """Test task counting logic."""
    print("\nTesting task categorization...")
    from datetime import datetime
    from report import (
        load_all_tasks,
        load_project_registry,
        parse_priority,
        parse_due_date,
        to_local_date,
        get_project_name
    )

    tasks = load_all_tasks()
    project_map = load_project_registry()
    user_tz = datetime.now().astimezone().tzinfo
    today = datetime.now(user_tz).date()

    in_progress = 0
    waiting = 0
    high_priority = 0
    due_today = 0
    overdue = 0
    projects = {}

    for task in tasks:
        status = task.get("status", "")
        priority = parse_priority(task)

        if status in ["done", "closed", "canceled"]:
            continue

        if status == "in-progress":
            in_progress += 1

        if status == "waiting":
            waiting += 1

        if priority == "high":
            high_priority += 1

        due_date = parse_due_date(task)
        if due_date:
            due_local = to_local_date(due_date, user_tz).date()
            if due_local == today:
                due_today += 1
            elif due_local < today:
                overdue += 1

        project = get_project_name(task, project_map)
        if project:
            projects[project] = projects.get(project, 0) + 1

    print(f"✓ In Progress: {in_progress}")
    print(f"✓ Waiting: {waiting}")
    print(f"✓ High Priority: {high_priority}")
    print(f"✓ Due Today: {due_today}")
    print(f"✓ Overdue: {overdue}")
    print(f"✓ Projects: {len(projects)}")

    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Todu Menu Bar App - Validation Tests")
    print("=" * 60)

    try:
        if not test_imports():
            print("\n✗ Import tests failed")
            return 1

        if not test_data_loading():
            print("\n✗ Data loading tests failed")
            return 1

        if not test_task_categorization():
            print("\n✗ Task categorization tests failed")
            return 1

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        print("\nTo run the menu bar app:")
        print("  uv run menubar/app.py")
        print("\nNote: The app will run in the background as a menu bar icon.")
        return 0

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
