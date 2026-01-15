---
name: habit-list
description: List and view habits. Use when user says "list habits", "show habits", "what habits am I tracking", "view my habits", "show my habits", "list tracked habits", or similar queries. (plugin:todu)
allowed-tools: todu, Bash
---

# List Habits

Show today's habit tasks using `todu task list --scheduled-date`.

## Command

```bash
todu task list --scheduled-date $(date +%Y-%m-%d)
```

## Optional Filters

| Filter    | Flag                | Example                  |
|-----------|---------------------|--------------------------|
| Project   | `--project`         | `--project myproject`    |
| Status    | `--status`          | `--status open` or `done`|

Display CLI output directly to the user.
