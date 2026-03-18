---
name: task-list
description: Search and list tasks. Use when user says "list tasks", "show tasks", "find tasks", "search tasks", "* priority tasks", "tasks in *", or similar. (plugin:todu)
allowed-tools: todu
---

# Search Tasks

Uses `todu task list` for structured filters and `todu task search` for
keyword search.

## Default Behavior

When the user asks for tasks without specifying a status, show active and
in-progress tasks by default:

```bash
todu task list --status active,inprogress [filters]
```

When the user specifies a status, query only that status.

Use keyword search when the user is clearly searching by title text:

```bash
todu task search "<keywords>" --format json
```

## Examples

- "show my tasks" → `todu task list --status active,inprogress`
- "tasks in todu-tests" → `todu task list --project todu-tests --status active,inprogress`
- "high priority bugs" → `todu task list --priority high --label bug --status active,inprogress`
- "show completed tasks" → `todu task list --status done`
- "show all tasks including done" → `todu task list`
- "overdue tasks" → `todu task list --overdue`
- "search tasks for auth" → `todu task search "auth" --format json`

## Available Filters

| Filter   | Flag         | Values                         |
|----------|--------------|--------------------------------|
| Project  | `--project`  | Project name or ID             |
| Status   | `--status`   | Comma-separated status values  |
| Priority | `--priority` | low, medium, high              |
| Label    | `--label`    | Any label                      |
| Overdue  | `--overdue`  | Flag                           |
| Today    | `--today`    | Flag                           |
| Sort     | `--sort`     | priority, dueDate, createdAt, updatedAt, title |
| Order    | `--asc`      | Ascending order                |

## Notes

- Use `todu task search` for title keyword search; use `todu task list` for structured filtering
- Display CLI output directly unless the user asks for a summary or prioritization
