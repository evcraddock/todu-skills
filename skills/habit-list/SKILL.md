---
name: habit-list
description: List and view habits. Use when user says "list habits", "show habits", "what habits am I tracking", "view my habits", "show my habits", "list tracked habits", or similar queries. (plugin:todu)
allowed-tools: todu, Bash
---

# List Habits

Lists habits using `todu habit list` and shows details with `todu habit show` when
needed.

## Default Behavior

When the user asks broadly what habits they are tracking, show active habits by
default.

## CLI Commands

```bash
# Default view

todu habit list --active

# Show all habits

todu habit list

# Filter by project

todu habit list --project <project>

# Filter by status

todu habit list --active

todu habit list --paused

# Show specific habit details

todu habit show <id>
```

## Examples

- "show my habits" → `todu habit list --active`
- "show all habits" → `todu habit list`
- "paused habits" → `todu habit list --paused`
- "habits in wellness" → `todu habit list --project wellness`
- "show habit 7" → `todu habit show 7`

## Notes

- Default to active habits unless the user asks for paused or all habits
- Use `todu habit show <id>` for full streak and schedule details
- Display CLI output directly unless the user asks for a summary
