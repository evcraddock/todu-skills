#!/usr/bin/env python3
"""
Unit tests for resolution utilities.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from git_context import (
    parse_repo_from_remote,
    detect_system_from_remote,
    get_base_url_from_remote,
    get_git_context,
    is_git_repository
)
from resolve_task import parse_filename


def test_parse_repo_from_remote():
    """Test parsing repo from various remote URL formats."""
    print("Testing parse_repo_from_remote...")

    # GitHub SSH
    assert parse_repo_from_remote('git@github.com:evcraddock/todu.git') == 'evcraddock/todu'
    assert parse_repo_from_remote('git@github.com:evcraddock/todu') == 'evcraddock/todu'

    # GitHub HTTPS
    assert parse_repo_from_remote('https://github.com/evcraddock/todu.git') == 'evcraddock/todu'
    assert parse_repo_from_remote('https://github.com/evcraddock/todu') == 'evcraddock/todu'

    # Forgejo SSH
    assert parse_repo_from_remote('git@forgejo.caradoc.com:erik/Vault.git') == 'erik/Vault'
    assert parse_repo_from_remote('git@forgejo.caradoc.com:erik/Vault') == 'erik/Vault'

    # Forgejo HTTPS
    assert parse_repo_from_remote('https://forgejo.caradoc.com/erik/Vault.git') == 'erik/Vault'
    assert parse_repo_from_remote('https://forgejo.caradoc.com/erik/Vault') == 'erik/Vault'

    print("✓ parse_repo_from_remote works correctly")


def test_detect_system_from_remote():
    """Test system detection from remote URLs."""
    print("\nTesting detect_system_from_remote...")

    assert detect_system_from_remote('git@github.com:evcraddock/todu.git') == 'github'
    assert detect_system_from_remote('https://github.com/evcraddock/todu') == 'github'

    assert detect_system_from_remote('git@forgejo.caradoc.com:erik/Vault.git') == 'forgejo'
    assert detect_system_from_remote('https://forgejo.caradoc.com/erik/Vault') == 'forgejo'

    assert detect_system_from_remote('git@gitea.example.com:user/repo.git') == 'forgejo'
    assert detect_system_from_remote('https://codeberg.org/user/repo') == 'forgejo'

    print("✓ detect_system_from_remote works correctly")


def test_get_base_url_from_remote():
    """Test extracting base URL from remote."""
    print("\nTesting get_base_url_from_remote...")

    assert get_base_url_from_remote('git@forgejo.caradoc.com:erik/Vault.git') == 'https://forgejo.caradoc.com'
    assert get_base_url_from_remote('https://forgejo.caradoc.com/erik/Vault') == 'https://forgejo.caradoc.com'
    assert get_base_url_from_remote('git@github.com:evcraddock/todu.git') == 'https://github.com'

    print("✓ get_base_url_from_remote works correctly")


def test_parse_filename():
    """Test parsing cache filenames."""
    print("\nTesting parse_filename...")

    # GitHub format
    result = parse_filename('github-evcraddock_todu-11.json')
    assert result is not None
    assert result['system'] == 'github'
    assert result['repo'] == 'evcraddock/todu'
    assert result['number'] == 11

    # Forgejo format
    result = parse_filename('forgejo-erik_Vault-5.json')
    assert result is not None
    assert result['system'] == 'forgejo'
    assert result['repo'] == 'erik/Vault'
    assert result['number'] == 5

    # Todoist format
    result = parse_filename('todoist-6c4gPG3vJhj9FMPp-123.json')
    assert result is not None
    assert result['system'] == 'todoist'
    assert result['repo'] == '6c4gPG3vJhj9FMPp'
    assert result['number'] == 123

    # Invalid formats
    assert parse_filename('invalid.json') is None
    assert parse_filename('github-repo.json') is None

    print("✓ parse_filename works correctly")


def test_git_context():
    """Test git context extraction from current repo."""
    print("\nTesting git_context...")

    # Test in todu repository (should work)
    todu_root = Path(__file__).resolve().parent.parent.parent

    context = get_git_context(todu_root)

    if context and context['is_git_repo']:
        assert context['repo'] is not None, "Should have detected repo"
        assert context['system'] is not None, "Should have detected system"
        assert context['branch'] is not None, "Should have detected branch"

        print(f"✓ Git context detected:")
        print(f"  - Repo: {context['repo']}")
        print(f"  - System: {context['system']}")
        print(f"  - Branch: {context['branch']}")
        print(f"  - Modified files: {len(context['modified_files'])}")
        print(f"  - Recent commits: {len(context['commits'])}")
    else:
        print("⚠ Not a git repository or no remote - skipping git context test")

    # Test is_git_repository
    assert is_git_repository(todu_root) is True, "todu should be a git repository"

    print("✓ git_context works correctly")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Resolution Utilities Tests")
    print("=" * 60)

    try:
        test_parse_repo_from_remote()
        test_detect_system_from_remote()
        test_get_base_url_from_remote()
        test_parse_filename()
        test_git_context()

        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
