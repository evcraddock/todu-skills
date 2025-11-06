#!/usr/bin/env python3
"""
Tests for recurring task functionality.
"""

import json
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone

# Add core scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from recurring import (
    is_recurring,
    create_completion_record,
    update_recurring_task,
    add_completion_to_history,
    get_completion_history,
    get_recurring_task,
    _system_data_matches
)
from id_registry import assign_id, clear_registry


def setup_test_env():
    """Create temporary test directory."""
    temp_dir = Path(tempfile.mkdtemp(prefix="todu_test_"))
    issues_dir = temp_dir / "issues"
    issues_dir.mkdir(parents=True)
    return temp_dir, issues_dir


def teardown_test_env(temp_dir):
    """Clean up test directory."""
    shutil.rmtree(temp_dir)


def test_is_recurring():
    """Test recurring task detection."""
    print("Testing is_recurring...")

    # Task with recurring object
    recurring_task = {
        "id": 1,
        "title": "Weekly review",
        "recurring": {
            "pattern": "weekly",
            "interval": 1
        }
    }
    assert is_recurring(recurring_task), "Should detect recurring task"

    # Task without recurring object
    normal_task = {
        "id": 2,
        "title": "Normal task"
    }
    assert not is_recurring(normal_task), "Should not detect normal task as recurring"

    # Task with null recurring
    null_recurring = {
        "id": 3,
        "title": "Task",
        "recurring": None
    }
    assert not is_recurring(null_recurring), "Should not detect null recurring as recurring"

    print("✓ is_recurring tests passed")


def test_create_completion_record():
    """Test completion record creation."""
    print("Testing create_completion_record...")

    temp_dir, issues_dir = setup_test_env()

    # Monkey patch ISSUES_DIR
    import recurring
    original_issues_dir = recurring.ISSUES_DIR
    recurring.ISSUES_DIR = issues_dir

    try:
        clear_registry()

        task_data = {
            "id": 1,
            "system": "github",
            "type": "issue",
            "title": "Weekly review",
            "description": "Review all tasks",
            "state": "open",
            "status": "open",
            "url": "https://github.com/test/repo/issues/1",
            "createdAt": "2025-11-01T10:00:00Z",
            "updatedAt": "2025-11-04T10:00:00Z",
            "labels": ["recurring:weekly"],
            "assignees": [],
            "priority": "high",
            "dueDate": "2025-11-08",
            "systemData": {
                "repo": "test/repo",
                "number": 1
            },
            "recurring": {
                "pattern": "weekly",
                "interval": 1,
                "nextDue": "2025-11-08",
                "completions": []
            }
        }

        completed_at = "2025-11-08T14:30:00Z"
        completion = create_completion_record(task_data, completed_at)

        # Verify completion record
        assert completion["id"] is not None, "Should have todu ID"
        assert completion["system"] == "github", "Should preserve system"
        assert completion["title"] == "Weekly review", "Should preserve title"
        assert completion["status"] == "done", "Should have done status"
        assert completion["completedAt"] == completed_at, "Should have completion timestamp"
        assert completion["systemData"]["repo"] == "test/repo", "Should preserve systemData"
        assert completion["systemData"]["number"] == 1, "Should preserve issue number"

        # Verify file was created
        completion_files = list(issues_dir.glob("github-*-completion-*.json"))
        assert len(completion_files) == 1, "Should create one completion file"

        print("✓ create_completion_record tests passed")

    finally:
        recurring.ISSUES_DIR = original_issues_dir
        teardown_test_env(temp_dir)


def test_update_recurring_task():
    """Test recurring task update."""
    print("Testing update_recurring_task...")

    task_data = {
        "id": 1,
        "title": "Weekly review",
        "state": "closed",
        "status": "done",
        "dueDate": "2025-11-08",
        "completedAt": "2025-11-08T14:30:00Z",
        "recurring": {
            "pattern": "weekly",
            "interval": 1,
            "nextDue": "2025-11-08",
            "completions": []
        }
    }

    updated = update_recurring_task(task_data, "2025-11-15")

    assert updated["dueDate"] == "2025-11-15", "Should update due date"
    assert updated["recurring"]["nextDue"] == "2025-11-15", "Should update nextDue"
    assert updated["state"] == "open", "Should reopen task"
    assert updated["status"] == "open", "Should reset status"
    assert "completedAt" not in updated, "Should remove completedAt"

    print("✓ update_recurring_task tests passed")


def test_add_completion_to_history():
    """Test adding completion to history."""
    print("Testing add_completion_to_history...")

    task_data = {
        "id": 1,
        "recurring": {
            "pattern": "weekly",
            "completions": []
        }
    }

    # Add first completion
    add_completion_to_history(task_data, 123, "2025-11-08T14:30:00Z")
    assert len(task_data["recurring"]["completions"]) == 1
    assert task_data["recurring"]["completions"][0]["completionId"] == 123

    # Add second completion
    add_completion_to_history(task_data, 124, "2025-11-01T16:45:00Z")
    assert len(task_data["recurring"]["completions"]) == 2

    # Should be sorted with most recent first
    assert task_data["recurring"]["completions"][0]["completedAt"] == "2025-11-08T14:30:00Z"
    assert task_data["recurring"]["completions"][1]["completedAt"] == "2025-11-01T16:45:00Z"

    print("✓ add_completion_to_history tests passed")


def test_system_data_matches():
    """Test systemData matching."""
    print("Testing _system_data_matches...")

    # GitHub/Forgejo matching
    data1 = {"repo": "owner/repo", "number": 42}
    data2 = {"repo": "owner/repo", "number": 42}
    data3 = {"repo": "owner/repo", "number": 43}
    data4 = {"repo": "other/repo", "number": 42}

    assert _system_data_matches(data1, data2), "Should match same repo and number"
    assert not _system_data_matches(data1, data3), "Should not match different number"
    assert not _system_data_matches(data1, data4), "Should not match different repo"

    # Todoist matching
    todoist1 = {"task_id": "abc123", "project_id": "proj456"}
    todoist2 = {"task_id": "abc123", "project_id": "proj999"}  # Different project OK
    todoist3 = {"task_id": "xyz789", "project_id": "proj456"}

    assert _system_data_matches(todoist1, todoist2), "Should match same task_id"
    assert not _system_data_matches(todoist1, todoist3), "Should not match different task_id"

    print("✓ _system_data_matches tests passed")


def test_get_completion_history():
    """Test querying completion history."""
    print("Testing get_completion_history...")

    temp_dir, issues_dir = setup_test_env()

    # Monkey patch ISSUES_DIR
    import recurring
    original_issues_dir = recurring.ISSUES_DIR
    recurring.ISSUES_DIR = issues_dir

    try:
        clear_registry()

        # Create original recurring task
        original_task = {
            "id": 1,
            "system": "github",
            "type": "issue",
            "title": "Weekly review",
            "status": "open",
            "systemData": {"repo": "test/repo", "number": 1},
            "recurring": {"pattern": "weekly", "completions": []}
        }

        # Create two completion records
        completion1 = create_completion_record(original_task, "2025-11-01T14:30:00Z")
        completion2 = create_completion_record(original_task, "2025-11-08T14:30:00Z")

        # Query completions
        completions = get_completion_history("github", {"repo": "test/repo", "number": 1})

        assert len(completions) == 2, "Should find both completions"
        assert completions[0]["id"] == completion2["id"], "Should be sorted by date (most recent first)"
        assert completions[1]["id"] == completion1["id"]

        # Query for non-existent task
        no_completions = get_completion_history("github", {"repo": "other/repo", "number": 99})
        assert len(no_completions) == 0, "Should return empty list for non-existent task"

        print("✓ get_completion_history tests passed")

    finally:
        recurring.ISSUES_DIR = original_issues_dir
        teardown_test_env(temp_dir)


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running recurring task tests...")
    print("=" * 60)

    try:
        test_is_recurring()
        test_create_completion_record()
        test_update_recurring_task()
        test_add_completion_to_history()
        test_system_data_matches()
        test_get_completion_history()

        print("=" * 60)
        print("✅ All recurring task tests passed!")
        print("=" * 60)
        return 0

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
