---
name: recurring-list
description: List recurring task templates. Use when user says "list recurring tasks", "show recurring tasks", or similar. (plugin:todu)
allowed-tools: todu, Bash
---

# List Recurring Tasks

Lists recurring task templates using `todu recurring list`.

## CLI Commands

```bash
# List all recurring tasks

todu recurring list

# Filter by project

todu recurring list --project myproject

# Filter by active status

todu recurring list --active
todu recurring list --paused

# Show a specific template

todu recurring show <id>
```

## Examples

- "show recurring tasks" → `todu recurring list`
- "recurring tasks in todu-skills" → `todu recurring list --project todu-skills`
- "active recurring tasks" → `todu recurring list --active`
- "paused recurring tasks" → `todu recurring list --paused`
- "show recurring task #7" → `todu recurring show 7`

## Notes

- Default output includes both active and paused templates
- Use `todu recurring show <id>` for full details
- Display CLI output directly unless the user asks for a summary
