---
name: nextactions
description: Show next actions to work on. Use when user says "next actions", "what's next", "what should I work on", or similar. (plugin:todu)
allowed-tools: todu
---

# Next Actions

Shows tasks that need attention by querying:
1. Tasks with status `inprogress`
2. Tasks with status `active` and priority `high`
3. Active or in-progress tasks in the `Inbox` project
4. Active tasks due or scheduled today
5. Active overdue tasks

## CLI Commands

```bash
todu task list --status inprogress
todu task list --status active --priority high
todu task list --project Inbox --status active,inprogress
todu task list --status active --today
todu task list --status active --overdue
```

## Process

1. Run the relevant queries
2. Deduplicate by task ID
3. Sort by due date (earliest first, nulls last)
4. Display as a single list or table

## Output Format

| ID  | Title               | Project | Due Date   |
|-----|---------------------|---------|------------|
| 159 | Benefits Enrollment | ntrs    | 2026-03-19 |
| 218 | Review PR           | Inbox   | -          |

If no tasks are found: `No next actions found`.
