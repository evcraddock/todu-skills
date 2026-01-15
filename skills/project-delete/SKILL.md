---
name: project-delete
description: Delete registered projects. Use when user says "delete project *", "remove project *", "unregister project *", or similar. (plugin:todu)
allowed-tools: todu
---

# Delete Registered Project

Deletes a project from todu using `todu project remove`.

## Example Interactions

### Example 1: Project with tasks

**User**: "Delete the todu-tests project"

1. Runs `todu project list --format json` to find project ID
2. Runs `todu task list --project todu-tests --format json` → 5 tasks
3. Shows: "Project: todu-tests (5 tasks)"
4. Asks: "Delete project only" / "Delete with tasks" / "Cancel"
5. User selects: "Delete with tasks"
6. Runs `todu project remove 22 --cascade --force`

### Example 2: Project with no tasks

**User**: "Remove empty-project"

1. Finds project, counts 0 tasks
2. Asks: "Yes, delete" / "Cancel"
3. Runs `todu project remove 15 --force`

## CLI Commands

```bash
# Find project ID
todu project list --format json

# Count tasks
todu task list --project <name> --format json

# Delete project only (tasks become orphaned)
todu project remove <id> --force

# Delete project and tasks
todu project remove <id> --cascade --force
```

## Confirmation Options

**Has tasks**: "Delete project only" / "Delete with tasks" / "Cancel"
**No tasks**: "Yes, delete" / "Cancel"

## Notes

- Must use project ID (not name) for remove command
- `--cascade` deletes associated tasks
- `--force` skips CLI confirmation (we handle it)
- Without `--cascade`, tasks become orphaned (rarely useful)
