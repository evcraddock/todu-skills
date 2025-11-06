#!/usr/bin/env python3
"""
Test interface argument building for all plugins.
"""

import sys
from pathlib import Path

# Add core/scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from plugin_registry import get_registry


def test_github_interface():
    """Test GitHub interface argument building."""
    print("Testing GitHub interface...")

    registry = get_registry()
    plugin = registry.get_plugin('github')

    # Test view operation
    task_data = {
        'systemData': {
            'repo': 'evcraddock/todu',
            'number': 42
        }
    }
    args = plugin.build_args('view', task_data=task_data)
    expected = ['--repo', 'evcraddock/todu', '--issue', '42']
    assert args == expected, f"Expected {expected}, got {args}"
    print(f"  ✓ view: {args}")

    # Test update operation
    params = {
        'status': 'inprogress',
        'priority': 'high'
    }
    args = plugin.build_args('update', task_data=task_data, params=params)
    assert '--repo' in args and 'evcraddock/todu' in args
    assert '--issue' in args and '42' in args
    assert '--status' in args and 'inprogress' in args
    assert '--priority' in args and 'high' in args
    print(f"  ✓ update: {args}")

    # Test comment operation
    params = {'body': 'This is a test comment'}
    args = plugin.build_args('comment', task_data=task_data, params=params)
    assert '--body' in args and 'This is a test comment' in args
    print(f"  ✓ comment: {args}")

    # Test sync operation
    params = {'repo': 'evcraddock/todu'}
    args = plugin.build_args('sync', params=params)
    assert args == ['--repo', 'evcraddock/todu']
    print(f"  ✓ sync: {args}")

    # Test create operation
    params = {
        'repo': 'evcraddock/todu',
        'title': 'Test issue',
        'body': 'This is a test',
        'labels': 'bug,priority:high'
    }
    args = plugin.build_args('create', params=params)
    assert '--repo' in args
    assert '--title' in args
    assert '--body' in args
    assert '--labels' in args
    print(f"  ✓ create: {args}")

    print("✓ GitHub interface tests passed")


def test_forgejo_interface():
    """Test Forgejo interface argument building."""
    print("\nTesting Forgejo interface...")

    registry = get_registry()
    plugin = registry.get_plugin('forgejo')

    # Test view operation
    task_data = {
        'systemData': {
            'repo': 'erik/Vault',
            'number': 8
        }
    }
    args = plugin.build_args('view', task_data=task_data)
    expected = ['--repo', 'erik/Vault', '--issue', '8']
    assert args == expected, f"Expected {expected}, got {args}"
    print(f"  ✓ view: {args}")

    # Test update operation
    params = {'status': 'done'}
    args = plugin.build_args('update', task_data=task_data, params=params)
    assert '--status' in args and 'done' in args
    print(f"  ✓ update: {args}")

    print("✓ Forgejo interface tests passed")


def test_todoist_interface():
    """Test Todoist interface argument building."""
    print("\nTesting Todoist interface...")

    registry = get_registry()
    plugin = registry.get_plugin('todoist')

    # Test view operation
    task_data = {
        'systemData': {
            'task_id': '6c4gPG4FgV6W82Gp'
        }
    }
    args = plugin.build_args('view', task_data=task_data)
    expected = ['--task-id', '6c4gPG4FgV6W82Gp']
    assert args == expected, f"Expected {expected}, got {args}"
    print(f"  ✓ view: {args}")

    # Test update operation
    params = {'status': 'done'}
    args = plugin.build_args('update', task_data=task_data, params=params)
    assert '--task-id' in args and '6c4gPG4FgV6W82Gp' in args
    assert '--status' in args and 'done' in args
    print(f"  ✓ update: {args}")

    # Test comment operation
    params = {'body': 'Test comment'}
    args = plugin.build_args('comment', task_data=task_data, params=params)
    assert '--task-id' in args
    assert '--body' in args and 'Test comment' in args
    print(f"  ✓ comment: {args}")

    # Test sync operation
    params = {'project_id': '6f9j9mGWwQrvvRHF'}
    args = plugin.build_args('sync', params=params)
    assert args == ['--project-id', '6f9j9mGWwQrvvRHF']
    print(f"  ✓ sync: {args}")

    # Test create operation
    params = {
        'project_id': '6f9j9mGWwQrvvRHF',
        'title': 'Test task',
        'priority': 'high'
    }
    args = plugin.build_args('create', params=params)
    assert '--project-id' in args
    assert '--title' in args
    assert '--priority' in args
    print(f"  ✓ create: {args}")

    print("✓ Todoist interface tests passed")


def test_registry_build_args():
    """Test registry-level build_args method."""
    print("\nTesting registry build_args...")

    registry = get_registry()

    # Test GitHub via registry
    task_data = {
        'systemData': {
            'repo': 'evcraddock/todu',
            'number': 42
        }
    }
    args = registry.build_args('github', 'view', task_data=task_data)
    assert args == ['--repo', 'evcraddock/todu', '--issue', '42']
    print(f"  ✓ github view via registry: {args}")

    # Test Todoist via registry
    task_data = {
        'systemData': {
            'task_id': 'abc123'
        }
    }
    args = registry.build_args('todoist', 'view', task_data=task_data)
    assert args == ['--task-id', 'abc123']
    print(f"  ✓ todoist view via registry: {args}")

    print("✓ Registry build_args tests passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Interface System Tests")
    print("=" * 60)

    try:
        test_github_interface()
        test_forgejo_interface()
        test_todoist_interface()
        test_registry_build_args()

        print("\n" + "=" * 60)
        print("All interface tests passed! ✓")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
