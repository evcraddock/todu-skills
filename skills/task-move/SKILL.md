---
name: task-move
description: Move a task to a different project. Use when user says "move task #* to *", "transfer task #* to *", or similar. (plugin:todu)
allowed-tools: todu
---

# Move Task to Different Project

Moves a task to another project using `todu task move`.

## What the CLI Does

- Creates a new task in the target project with the same fields
- Adds linking notes to both tasks
- Cancels the original task

## Examples

### Move task

**User**: "Move task 20 to todu-api"

1. Asks: "Move task #20 to todu-api?"
2. If confirmed: `todu task move 20 todu-api`

### Missing project

**User**: "Move task 20"

1. Asks: "Which project?"
2. User provides project
3. Confirms and moves

## CLI Commands

```bash
todu task move <id> <project>
```

## Notes

- Always confirm before moving because the original task is canceled
- Both tasks receive linking notes for traceability
