---
name: task-list
description: Search and list tasks. Use when user says "list tasks", "show tasks", "find tasks", "search tasks", "* priority tasks", "tasks in *", or similar. (plugin:todu)
allowed-tools: todu
---

# Search Tasks

Search tasks using `todu task list`.

## Default Behavior

When status NOT specified, query both statuses and combine results:

```bash
todu task list --status inprogress [filters]
todu task list --status active [filters]
```

When status IS specified, query only that status.

## Examples

- "show my tasks" → `--status inprogress` + `--status active`
- "tasks in todu-tests" → `--project todu-tests --status inprogress` + `--status active`
- "high priority bugs" → `--priority high --label bug --status inprogress` + `--status active`
- "show completed tasks" → `--status done`
- "show all tasks including done" → no status filter
- "overdue tasks" → `--due-before <today>`

## Available Filters

| Filter   | Flag           | Values                        |
|----------|----------------|-------------------------------|
| Project  | `--project`    | Project name or ID            |
| Status   | `--status`     | active, inprogress, waiting, done, canceled |
| Priority | `--priority`   | low, medium, high             |
| Label    | `--label`      | Any label (repeatable)        |
| Assignee | `--assignee`   | Username                      |
| Search   | `--search`     | Full-text search              |
| Due      | `--due-before` | YYYY-MM-DD                    |
|          | `--due-after`  | YYYY-MM-DD                    |

## Notes

- Combine and deduplicate results when querying multiple statuses
- Display CLI output directly
