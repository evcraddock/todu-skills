---
name: project-delete
description: Delete registered projects. Use when user says "delete project *", "remove project *", "unregister project *", or similar. (plugin:todu)
allowed-tools: todu
---

# Delete Registered Project

Deletes a project from todu using `todu project delete`.

## Example Interactions

### Example 1: Project with tasks

**User**: "Delete the todu-tests project"

1. Runs `todu project show todu-tests --format json` to verify the project
2. Runs `todu task list --project todu-tests --format json` to count remaining tasks
3. Shows: "Project: todu-tests (5 visible tasks)"
4. Asks: "Yes, delete" / "Cancel"
5. User selects: "Yes, delete"
6. Runs `todu project delete todu-tests`

### Example 2: Project with no visible tasks

**User**: "Remove empty-project"

1. Verifies the project exists
2. Shows the project details
3. Asks: "Yes, delete" / "Cancel"
4. Runs `todu project delete empty-project`

## CLI Commands

```bash
# Verify the project

todu project show <ref> --format json

# Count visible tasks for context

todu task list --project <name> --format json

# Delete after explicit confirmation

todu project delete <ref>
```

## Confirmation Options

"Yes, delete" / "Cancel"

Only delete if the user explicitly confirms.

## Notes

- The current CLI accepts a project name or ID as `<ref>`
- Surface remaining task count before deletion so the user understands impact
- If the CLI rejects deletion because dependent data still exists, tell the user what still needs to be moved or removed first
