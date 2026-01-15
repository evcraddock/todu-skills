---
name: task-move
description: Move a task to a different project. Use when user says "move task #* to *", "transfer task #* to *", or similar. (plugin:todu)
allowed-tools: todu
---

# Move Task to Different Project

Moves a task to another project using `todu task move`.

## What the CLI Does

- Creates new task in target project with same fields
- Adds linking comments to both tasks
- Cancels the original task

## Examples

### Move task

**User**: "Move task 20 to todu-api"

1. Asks: "Move task #20 to todu-api?"
2. If confirmed: `todu task move 20 --project todu-api`

### Missing project

**User**: "Move task 20"

1. Asks: "Which project?"
2. User provides project
3. Confirms and moves

## CLI Commands

```bash
todu task move <id> --project <name>
```

## Notes

- Always confirm before moving (destructive operation)
- Original task is canceled after move
- Both tasks get linking comments for traceability
