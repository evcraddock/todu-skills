---
name: project-register
description: Register a new project. Use when user says "register project *", "add project *", or similar. (plugin:todu)
allowed-tools: todu
---

# Register Project

Registers a project using `todu project add`. Handles nickname conflicts.

## Process

1. Check if already registered via `todu project list --format json`
2. If exists, return success immediately
3. Generate nickname from repo/project name
4. Check for nickname conflicts
5. If conflict, ask user to choose alternative
6. Register with `todu project add`

## Examples

### External repo (GitHub/Forgejo)

**User**: "Register evcraddock/rott"

1. Checks project list → not found
2. Suggests nickname: "rott" → no conflict
3. Runs: `todu project add --name rott --system github --external-id evcraddock/rott --format json`

### Nickname conflict

**User**: "Register owner/repo-name"

1. Suggests "repo-name" → already exists
2. Asks user: "repo-name2" / "repo-name-owner" / Other
3. Registers with chosen nickname

### Local project

**User**: "Create a local project called shopping-list"

Runs: `todu project add --name shopping-list --format json`

## CLI Commands

```bash
# Check existing projects
todu project list --format json

# Get available systems
todu system list

# Register external project
todu project add --name <nickname> --system <system-name> --external-id <owner/repo> --format json

# Register local project
todu project add --name <nickname> --format json

# Optional flags
--priority <low|medium|high>
--description "text"
```

## Nickname Conflict Resolution

Ask user with options:
- "{nickname}2" - numbered suffix
- "{nickname}-{owner}" - include owner

## Notes

- Check `todu system list` for valid system names
- Project names must be unique across all systems
- Priority defaults to medium
