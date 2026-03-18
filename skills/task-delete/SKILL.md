---
name: task-delete
description: Delete tasks. Use when user says "delete task *", "remove task *", "trash task *", or similar. (plugin:todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Delete Task

Use this flow:

1. Show the task with `todu task show <id> --format json`
2. If needed, find it with `todu task search "<keywords>" --format json`
3. Ask for confirmation
4. Delete it with `todu task delete <id>`

## Examples

- "delete task 42" → show task, confirm, delete
- "remove the auth bug task" → search, confirm, delete

## Commands

```bash
todu task show <id> --format json
todu task search "<keywords>" --format json
todu task delete <id>
```

## Notes

- Always confirm before deleting
- Ask the user to choose if multiple tasks match
- If the user may mean cancel or done instead of delete, say so
