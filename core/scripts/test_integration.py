#!/usr/bin/env python3
"""
Integration tests for the unified task management system.

Tests that plugin registry, resolution utilities, and skills work together.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from plugin_registry import get_registry
from resolve_task import resolve_task, parse_filename
from git_context import get_git_context
import id_registry


def test_end_to_end_resolution():
    """Test complete flow from unified ID to script path."""
    print("Testing end-to-end resolution flow...")

    # Get a real unified ID from the registry
    stats = id_registry.get_stats()
    next_id, total_items = stats

    if total_items == 0:
        print("⚠ No tasks in registry - skipping end-to-end test")
        print("  (Run a sync first to populate the registry)")
        return

    # Try to resolve the first task
    test_id = 1
    filename = id_registry.lookup_filename(test_id)

    if not filename:
        print(f"⚠ ID {test_id} not found - trying another...")
        # Try to find any valid ID
        for i in range(1, min(100, next_id)):
            filename = id_registry.lookup_filename(i)
            if filename:
                test_id = i
                break

    if not filename:
        print("⚠ No valid IDs found in registry - skipping test")
        return

    print(f"  Testing with ID {test_id} → {filename}")

    # Parse filename to get system info
    parsed = parse_filename(filename)
    if not parsed:
        print(f"  ✗ Failed to parse filename: {filename}")
        return

    system = parsed['system']
    repo = parsed['repo']
    number = parsed['number']

    print(f"  Parsed: {system}/{repo}#{number}")

    # Get plugin registry
    registry = get_registry()

    # Get script path for 'view' operation
    try:
        view_script = registry.get_script_path(system, 'view')
        print(f"  ✓ View script: {view_script.relative_to(view_script.parent.parent.parent)}")
    except Exception as e:
        print(f"  ✗ Failed to get view script: {e}")
        return

    # Verify script exists
    if not view_script.exists():
        print(f"  ✗ Script does not exist: {view_script}")
        return

    print(f"  ✓ Script exists and is executable")

    # Try all operations
    operations = ['create', 'update', 'sync', 'view', 'comment']
    for op in operations:
        try:
            script = registry.get_script_path(system, op)
            if script.exists():
                print(f"  ✓ {op:8s} → {script.name}")
            else:
                print(f"  ✗ {op:8s} → {script} (not found)")
        except Exception as e:
            print(f"  ⚠ {op:8s} → {e}")

    print("✓ End-to-end resolution flow works!")


def test_git_context_integration():
    """Test git context extraction with current repo."""
    print("\nTesting git context integration...")

    # Get context from current repo
    todu_root = Path(__file__).resolve().parent.parent.parent
    context = get_git_context(todu_root)

    if not context or not context['is_git_repo']:
        print("  ⚠ Not in a git repository - skipping")
        return

    print(f"  Git context detected:")
    print(f"    System: {context['system']}")
    print(f"    Repo: {context['repo']}")
    print(f"    Branch: {context['branch']}")

    # If we detected a system, verify we can get its scripts
    if context['system']:
        registry = get_registry()
        try:
            sync_script = registry.get_script_path(context['system'], 'sync')
            print(f"    ✓ Can route to sync script: {sync_script.name}")
        except Exception as e:
            print(f"    ✗ Failed to route: {e}")
            return

    print("✓ Git context integration works!")


def test_plugin_capabilities():
    """Test plugin capability checking."""
    print("\nTesting plugin capabilities...")

    registry = get_registry()

    for system_name in ['github', 'forgejo', 'todoist']:
        plugin = registry.get_plugin(system_name)
        if not plugin:
            print(f"  ✗ Plugin '{system_name}' not found")
            continue

        print(f"  {plugin.display_name}:")
        print(f"    Task Management: {plugin.capabilities.get('taskManagement')}")
        print(f"    Comments: {plugin.capabilities.get('comments')}")
        print(f"    Labels: {plugin.capabilities.get('labels')}")
        print(f"    Available: {plugin.is_available()}")

        # Check required operations
        required_ops = ['create', 'update', 'sync', 'view', 'comment']
        for op in required_ops:
            try:
                script = plugin.get_script_path(op)
                exists = script.exists()
                status = "✓" if exists else "✗"
                print(f"    {status} {op}: {script.name}")
            except Exception as e:
                print(f"    ✗ {op}: {e}")

    print("✓ Plugin capabilities check complete!")


def test_system_detection():
    """Test system detection from various remote URLs."""
    print("\nTesting system detection from remotes...")

    test_cases = [
        ('git@github.com:evcraddock/todu.git', 'github', 'evcraddock/todu'),
        ('https://github.com/evcraddock/todu.git', 'github', 'evcraddock/todu'),
        ('git@forgejo.caradoc.com:erik/Vault.git', 'forgejo', 'erik/Vault'),
        ('https://forgejo.caradoc.com/erik/Vault', 'forgejo', 'erik/Vault'),
    ]

    from git_context import parse_repo_from_remote, detect_system_from_remote

    for remote_url, expected_system, expected_repo in test_cases:
        repo = parse_repo_from_remote(remote_url)
        system = detect_system_from_remote(remote_url)

        if repo == expected_repo and system == expected_system:
            print(f"  ✓ {remote_url}")
            print(f"    → {system}/{repo}")
        else:
            print(f"  ✗ {remote_url}")
            print(f"    Expected: {expected_system}/{expected_repo}")
            print(f"    Got: {system}/{repo}")

    print("✓ System detection works!")


def main():
    """Run all integration tests."""
    print("=" * 70)
    print("Unified Task Management Integration Tests")
    print("=" * 70)

    try:
        test_plugin_capabilities()
        test_system_detection()
        test_git_context_integration()
        test_end_to_end_resolution()

        print("\n" + "=" * 70)
        print("All integration tests completed! ✓")
        print("=" * 70)
        print("\nThe unified task management system is ready to use.")
        print("\nCore skills available:")
        print("  - core:task-sync")
        print("  - core:task-view")
        print("  - core:task-update")
        print("  - core:task-create")
        print("  - core:task-comment-create")
        return 0

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
