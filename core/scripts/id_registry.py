"""
Unified ID registry for todu tasks/issues.

Manages a combined counter and index in a single JSON file:
{
  "next_id": 124,
  "index": {
    "1": "github_evcraddock_todu_11.json",
    "5": "todoist_6c4gPG4FgV6W82Gp.json"
  }
}
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple


REGISTRY_FILE = Path.home() / ".local" / "todu" / "id_registry.json"


def _read_registry() -> dict:
    """Read the registry file. Returns empty structure if file doesn't exist."""
    if not REGISTRY_FILE.exists():
        return {"next_id": 1, "index": {}}

    try:
        with open(REGISTRY_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        raise RuntimeError(f"Failed to read ID registry: {e}")


def _write_registry(registry: dict) -> None:
    """Atomically write the registry file."""
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write to temp file first, then rename for atomicity
    fd, temp_path = tempfile.mkstemp(
        dir=REGISTRY_FILE.parent,
        prefix='.id_registry_',
        suffix='.json.tmp'
    )

    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(registry, f, indent=2)

        # Atomic rename
        os.replace(temp_path, REGISTRY_FILE)
    except Exception as e:
        # Clean up temp file on error
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise RuntimeError(f"Failed to write ID registry: {e}")


def assign_id(filename: str) -> int:
    """
    Assign a new todu ID and register it with the given filename.

    Args:
        filename: The cache filename (e.g., "github_owner_repo_11.json")

    Returns:
        The assigned todu ID
    """
    registry = _read_registry()

    # Get next ID and increment
    todu_id = registry["next_id"]
    registry["next_id"] += 1

    # Add to index
    registry["index"][str(todu_id)] = filename

    # Write back atomically
    _write_registry(registry)

    return todu_id


def lookup_filename(todu_id: int) -> Optional[str]:
    """
    Look up the filename for a given todu ID.

    Args:
        todu_id: The todu ID to look up

    Returns:
        The filename, or None if not found
    """
    registry = _read_registry()
    return registry["index"].get(str(todu_id))


def lookup_id(filename: str) -> Optional[int]:
    """
    Look up the todu ID for a given filename.

    Args:
        filename: The cache filename to look up

    Returns:
        The todu ID, or None if not found
    """
    registry = _read_registry()

    # Reverse lookup
    for todu_id_str, fname in registry["index"].items():
        if fname == filename:
            return int(todu_id_str)

    return None


def update_filename(todu_id: int, new_filename: str) -> None:
    """
    Update the filename for an existing todu ID.
    Useful if a file is renamed but we want to preserve the ID.

    Args:
        todu_id: The todu ID to update
        new_filename: The new filename
    """
    registry = _read_registry()

    if str(todu_id) not in registry["index"]:
        raise ValueError(f"Todu ID {todu_id} not found in registry")

    registry["index"][str(todu_id)] = new_filename
    _write_registry(registry)


def remove_id(todu_id: int) -> None:
    """
    Remove a todu ID from the registry.
    Use when deleting a task/issue.

    Args:
        todu_id: The todu ID to remove
    """
    registry = _read_registry()

    if str(todu_id) in registry["index"]:
        del registry["index"][str(todu_id)]
        _write_registry(registry)


def clear_registry() -> None:
    """
    Clear the entire registry.
    Use when doing a full cache reset.
    """
    registry = {"next_id": 1, "index": {}}
    _write_registry(registry)


def get_stats() -> Tuple[int, int]:
    """
    Get registry statistics.

    Returns:
        Tuple of (next_id, total_items)
    """
    registry = _read_registry()
    return (registry["next_id"], len(registry["index"]))
