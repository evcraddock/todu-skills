---
name: task-search
description: skill for listing or searching tasks and issues across all registered projects. Use when user wants to find, list, or search tasks/issues. (plugin:core@todu)
---

# Search Tasks and Issues

Search tasks using `todu task list` with natural language parsing.

## Default Behavior

**CRITICAL**: When status is NOT explicitly specified, run TWO commands:

```bash
todu task list --status inprogress [filters]
todu task list --status active [filters]
```

When status IS explicitly specified, run only that status.

## Examples

**"show me all my tasks"** (no status specified):

```bash
todu task list --status inprogress
todu task list --status active
```

**"list tasks in todu-tests"** (no status specified):

```bash
todu task list --project todu-tests --status inprogress
todu task list --project todu-tests --status active
```

**"show open tasks"** (status explicitly specified):

```bash
todu task list --status active
```

**"high priority bugs in todu-tests"** (no status specified):

```bash
todu task list --project todu-tests --priority high --label bug --status inprogress
todu task list --project todu-tests --priority high --label bug --status active
```

## Natural Language Parsing

- **Project**: "tasks in PROJECT", "list PROJECT issues" → `--project PROJECT`
- **Status**: "open/active" → `active`, "in progress/working" → `inprogress`,
  "done/completed/closed" → `done`, "cancelled" → `cancelled`
- **Priority**: "high/medium/low priority" → `--priority high/medium/low`
- **Label**: "bugs" → `--label bug`, "features" → `--label enhancement`
- **Assignee**: "assigned to USER" → `--assignee USER`
- **Search**: "about TOPIC", "find KEYWORD" → `--search TOPIC`

## Available Filters

- `--project <name|id>` - Filter by project
- `--status <status>` - inprogress, active, done, cancelled
- `--priority <priority>` - low, medium, high
- `--label <label>` - Repeatable for multiple labels (AND logic)
- `--assignee <username>` - Filter by assignee
- `--search <text>` - Full-text search

Display CLI output directly to the user.
