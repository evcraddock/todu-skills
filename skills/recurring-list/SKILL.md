---
name: recurring-list
description: List recurring task templates. Use when user says "list recurring tasks", "show recurring tasks", or similar. (plugin:todu)
allowed-tools: todu, Bash
---

# List Recurring Tasks

Lists recurring task templates using `todu template list --type task`.

## CLI Commands

```bash
# List all recurring tasks
todu template list --type task

# Filter by project
todu template list --type task --project myproject

# Filter by active status
todu template list --type task --active true
todu template list --type task --active false

# Show specific template
todu template show <id>
```

## Examples

- "show recurring tasks" → `todu template list --type task`
- "recurring tasks in todu-skills" → `--type task --project todu-skills`
- "active recurring tasks" → `--type task --active true`
- "paused recurring tasks" → `--type task --active false`
- "show recurring task #7" → `todu template show 7`

## Notes

- Always use `--type task` (not habit)
- Default shows both active and inactive
- Display CLI output directly
