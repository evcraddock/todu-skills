---
name: nextactions
description: Show next actions to work on. Use when user says "next actions", "what's next", "what should I work on", or similar. (plugin:todu)
allowed-tools: todu
---

# Next Actions

Shows tasks that need attention by querying:
1. Tasks with status "inprogress"
2. Tasks with status "active" AND priority "high"
3. Tasks in the Inbox project
4. Active tasks due today or earlier

## CLI Commands

```bash
todu task list --status inprogress
todu task list --status active --priority high
todu task list --project Inbox
todu task list --status active --due-before <tomorrow YYYY-MM-DD>
```

## Process

1. Run all three queries
2. Deduplicate by task ID
3. Sort by due date (earliest first, nulls last)
4. Display as single table

## Output Format

| ID  | Title               | Project | Due Date   |
|-----|---------------------|---------|------------|
| 159 | Benefits Enrollment | ntrs    | 2025-12-02 |
| 218 | Review PR           | Inbox   | -          |

If no tasks found: "No next actions found"
