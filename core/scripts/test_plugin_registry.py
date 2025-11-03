#!/usr/bin/env python3
"""
Unit tests for plugin_registry.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from plugin_registry import Plugin, PluginRegistry, get_registry


def test_plugin_discovery():
    """Test that all plugins are discovered correctly."""
    print("Testing plugin discovery...")

    # Get todu root (3 levels up from this script)
    todu_root = Path(__file__).resolve().parent.parent.parent

    registry = PluginRegistry(todu_root)

    # Should discover github, forgejo, and todoist
    assert 'github' in registry.plugins, "GitHub plugin not discovered"
    assert 'forgejo' in registry.plugins, "Forgejo plugin not discovered"
    assert 'todoist' in registry.plugins, "Todoist plugin not discovered"

    print(f"✓ Discovered {len(registry.plugins)} plugins: {', '.join(registry.plugins.keys())}")


def test_plugin_metadata():
    """Test that plugin metadata is loaded correctly."""
    print("\nTesting plugin metadata...")

    todu_root = Path(__file__).resolve().parent.parent.parent
    registry = PluginRegistry(todu_root)

    # Test GitHub plugin
    github = registry.get_plugin('github')
    assert github is not None, "GitHub plugin not found"
    assert github.system == 'github', f"Expected system 'github', got '{github.system}'"
    assert github.display_name == 'GitHub', f"Expected displayName 'GitHub', got '{github.display_name}'"
    assert github.capabilities.get('taskManagement') is True, "GitHub should have taskManagement capability"
    assert github.capabilities.get('comments') is True, "GitHub should have comments capability"

    print(f"✓ GitHub plugin: {github.display_name} v{github.version}")

    # Test Forgejo plugin
    forgejo = registry.get_plugin('forgejo')
    assert forgejo is not None, "Forgejo plugin not found"
    assert forgejo.system == 'forgejo', f"Expected system 'forgejo', got '{forgejo.system}'"
    assert forgejo.display_name == 'Forgejo', f"Expected displayName 'Forgejo', got '{forgejo.display_name}'"

    print(f"✓ Forgejo plugin: {forgejo.display_name} v{forgejo.version}")

    # Test Todoist plugin
    todoist = registry.get_plugin('todoist')
    assert todoist is not None, "Todoist plugin not found"
    assert todoist.system == 'todoist', f"Expected system 'todoist', got '{todoist.system}'"
    assert todoist.display_name == 'Todoist', f"Expected displayName 'Todoist', got '{todoist.display_name}'"

    print(f"✓ Todoist plugin: {todoist.display_name} v{todoist.version}")


def test_script_path_resolution():
    """Test that script paths are resolved correctly."""
    print("\nTesting script path resolution...")

    todu_root = Path(__file__).resolve().parent.parent.parent
    registry = PluginRegistry(todu_root)

    # Test GitHub scripts
    github = registry.get_plugin('github')
    create_path = github.get_script_path('create')
    assert create_path.exists(), f"GitHub create script not found: {create_path}"
    assert create_path.name == 'create-issue.py', f"Expected create-issue.py, got {create_path.name}"

    print(f"✓ GitHub create script: {create_path.relative_to(todu_root)}")

    sync_path = github.get_script_path('sync')
    assert sync_path.exists(), f"GitHub sync script not found: {sync_path}"
    assert sync_path.name == 'sync-issues.py', f"Expected sync-issues.py, got {sync_path.name}"

    print(f"✓ GitHub sync script: {sync_path.relative_to(todu_root)}")

    # Test Todoist scripts (different naming convention)
    todoist = registry.get_plugin('todoist')
    create_path = todoist.get_script_path('create')
    assert create_path.exists(), f"Todoist create script not found: {create_path}"
    assert create_path.name == 'create-task.py', f"Expected create-task.py, got {create_path.name}"

    print(f"✓ Todoist create script: {create_path.relative_to(todu_root)}")


def test_registry_script_path():
    """Test registry-level script path resolution."""
    print("\nTesting registry script path resolution...")

    todu_root = Path(__file__).resolve().parent.parent.parent
    registry = PluginRegistry(todu_root)

    # Test via registry
    path = registry.get_script_path('github', 'create')
    assert path.exists(), f"Script not found via registry: {path}"

    print(f"✓ Registry script path resolution: {path.relative_to(todu_root)}")

    # Test error handling - invalid system
    try:
        registry.get_script_path('invalid_system', 'create')
        assert False, "Should have raised ValueError for invalid system"
    except ValueError as e:
        print(f"✓ Correct error for invalid system: {e}")

    # Test error handling - invalid operation
    try:
        registry.get_script_path('github', 'invalid_operation')
        assert False, "Should have raised ValueError for invalid operation"
    except ValueError as e:
        print(f"✓ Correct error for invalid operation: {e}")


def test_plugin_requirements():
    """Test plugin requirements checking."""
    print("\nTesting plugin requirements...")

    todu_root = Path(__file__).resolve().parent.parent.parent
    registry = PluginRegistry(todu_root)

    github = registry.get_plugin('github')

    # Check requirements
    assert 'env' in github.requirements, "GitHub should have env requirements"
    assert 'GITHUB_TOKEN' in github.requirements['env'], "GitHub should require GITHUB_TOKEN"

    # Test availability (depends on environment)
    has_token = os.environ.get('GITHUB_TOKEN') is not None
    is_available = github.is_available()

    if has_token:
        assert is_available, "GitHub should be available when GITHUB_TOKEN is set"
        print("✓ GitHub is available (GITHUB_TOKEN is set)")
    else:
        assert not is_available, "GitHub should not be available when GITHUB_TOKEN is not set"
        print("✓ GitHub is not available (GITHUB_TOKEN not set)")


def test_available_systems():
    """Test get_available_systems() output."""
    print("\nTesting available systems list...")

    todu_root = Path(__file__).resolve().parent.parent.parent
    registry = PluginRegistry(todu_root)

    systems = registry.get_available_systems()

    assert len(systems) == 3, f"Expected 3 systems, got {len(systems)}"

    # Check structure
    for system in systems:
        assert 'system' in system, "System dict should have 'system' key"
        assert 'displayName' in system, "System dict should have 'displayName' key"
        assert 'description' in system, "System dict should have 'description' key"
        assert 'available' in system, "System dict should have 'available' key"
        assert 'requirements' in system, "System dict should have 'requirements' key"

        print(f"✓ {system['displayName']}: available={system['available']}")


def test_singleton_pattern():
    """Test that get_registry() returns singleton."""
    print("\nTesting singleton pattern...")

    registry1 = get_registry()
    registry2 = get_registry()

    assert registry1 is registry2, "get_registry() should return same instance"

    print("✓ Singleton pattern works correctly")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Plugin Registry Tests")
    print("=" * 60)

    try:
        test_plugin_discovery()
        test_plugin_metadata()
        test_script_path_resolution()
        test_registry_script_path()
        test_plugin_requirements()
        test_available_systems()
        test_singleton_pattern()

        print("\n" + "=" * 60)
        print("All tests passed! ✓")
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
