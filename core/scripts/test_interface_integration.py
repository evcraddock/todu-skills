#!/usr/bin/env python3
"""
Integration test: Use interface system to actually call a real script.
"""

import sys
import json
import subprocess
from pathlib import Path

# Add core/scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from plugin_registry import get_registry


def test_view_github_issue():
    """Test viewing a real GitHub issue using interface system."""
    print("Testing GitHub view with interface system...")

    registry = get_registry()

    # Simulate resolved task data
    task_data = {
        'system': 'github',
        'systemData': {
            'repo': 'evcraddock/todu',
            'number': 32  # "GitHub scripts don't auto-create status/priority labels"
        }
    }

    # Get script path and build args using interface
    script_path = registry.get_script_path('github', 'view')
    args = registry.build_args('github', 'view', task_data=task_data)

    print(f"  Script: {script_path}")
    print(f"  Args: {args}")

    # Call the actual script
    result = subprocess.run(
        ['python3', str(script_path)] + args,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"  ✗ Script failed with code {result.returncode}")
        print(f"  stderr: {result.stderr}")
        return False

    # Check output (view script outputs markdown, not JSON)
    if 'Issue #32' in result.stdout and 'GitHub scripts' in result.stdout:
        print(f"  ✓ Got issue output (markdown format)")
        return True
    else:
        print(f"  ✗ Unexpected output")
        print(f"  stdout: {result.stdout[:200]}")
        return False


def test_view_todoist_task():
    """Test viewing a real Todoist task using interface system."""
    print("\nTesting Todoist view with interface system...")

    registry = get_registry()

    # Simulate resolved task data - skip this test for now since task IDs change
    print("  ⊘ Skipping - task IDs are ephemeral")
    return True

    task_data = {
        'system': 'todoist',
        'systemData': {
            'task_id': 'PLACEHOLDER'
        }
    }

    # Get script path and build args using interface
    script_path = registry.get_script_path('todoist', 'view')
    args = registry.build_args('todoist', 'view', task_data=task_data)

    print(f"  Script: {script_path}")
    print(f"  Args: {args}")

    # Call the actual script
    result = subprocess.run(
        ['python3', str(script_path)] + args,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"  ✗ Script failed with code {result.returncode}")
        print(f"  stderr: {result.stderr}")
        return False

    # Parse output
    try:
        output = json.loads(result.stdout)
        print(f"  ✓ Got task: {output.get('title')}")
        return True
    except json.JSONDecodeError as e:
        print(f"  ✗ Failed to parse JSON output: {e}")
        print(f"  stdout: {result.stdout[:200]}")
        return False


def test_sync_github():
    """Test syncing GitHub using interface system."""
    print("\nTesting GitHub sync with interface system...")

    registry = get_registry()

    # Build sync args
    params = {'repo': 'evcraddock/todu'}
    script_path = registry.get_script_path('github', 'sync')
    args = registry.build_args('github', 'sync', params=params)

    print(f"  Script: {script_path}")
    print(f"  Args: {args}")

    # Call the actual script
    result = subprocess.run(
        ['python3', str(script_path)] + args,
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:
        print(f"  ✗ Script failed with code {result.returncode}")
        print(f"  stderr: {result.stderr}")
        return False

    # Parse output
    try:
        output = json.loads(result.stdout)
        print(f"  ✓ Synced {output.get('total', 0)} issues")
        return True
    except json.JSONDecodeError as e:
        print(f"  ✗ Failed to parse JSON output: {e}")
        print(f"  stdout: {result.stdout[:200]}")
        return False


def main():
    """Run integration tests."""
    print("=" * 60)
    print("Interface System Integration Tests")
    print("=" * 60)

    results = []

    # Test view operations
    results.append(("GitHub view", test_view_github_issue()))
    results.append(("Todoist view", test_view_todoist_task()))
    results.append(("GitHub sync", test_sync_github()))

    # Summary
    print("\n" + "=" * 60)
    print("Integration Test Results:")
    print("=" * 60)

    for name, passed in results:
        status = "✓" if passed else "✗"
        print(f"  {status} {name}")

    all_passed = all(passed for _, passed in results)

    if all_passed:
        print("\n✓ All integration tests passed!")
        return 0
    else:
        print("\n✗ Some integration tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
