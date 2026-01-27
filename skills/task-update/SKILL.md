---
name: task-update
description: Update tasks/issues. Use when user says "update task #*", "mark task #* as *", "set priority on #*", "mark task done", "set task status to done", "quick close task", or similar. (plugin:todu)
allowed-tools: todu
---

# Update Task

Updates task properties using `todu task update` and `todu task close`.

## Closing Tasks - Comment Required

**When closing/completing a task, always add a comment:**

1. If user provides comment text: use it
2. If no comment text provided: summarize the preceding activity on the task from the conversation and use that as the comment

```bash
todu task close <id>
todu task comment <id> -m "<summary of what was done>" --format json
```

## Natural Language Patterns

### Status Updates
- "mark task 39 as done" → `todu task close 39` + comment
- "complete task 5" → `todu task close 5` + comment
- "close task 20" → `todu task close 20` + comment
- "start working on task 12" → `todu task update 12 --status inprogress`
- "set task 5 to waiting" → `todu task update 5 --status waiting`

### Priority
- "set priority high on task 20" → `todu task update 20 --priority high`

### Labels
- "add label bug to task 20" → `todu task update 20 --add-label bug`
- "remove label testing from task 5" → `todu task update 5 --remove-label testing`

### Assignees
- "assign task 20 to alice" → `todu task update 20 --add-assignee alice`

## Examples

### Close with provided comment

**User**: "Close task 42: Fixed the authentication bug"

1. Runs: `todu task close 42`
2. Runs: `todu task comment 42 -m "Fixed the authentication bug" --format json`

### Close without comment (summarize activity)

**User**: "Mark task 39 as done"

1. Runs: `todu task close 39`
2. Summarizes preceding activity from conversation
3. Runs: `todu task comment 39 -m "<summary of work done>" --format json`

### Update status

**User**: "Start working on task 12"

Runs: `todu task update 12 --status inprogress`

### Multiple updates

**User**: "Set task 15 to active with high priority"

Runs: `todu task update 15 --status active --priority high`

## CLI Commands

```bash
# Close task
todu task close <id>

# Update status
todu task update <id> --status <active|inprogress|waiting|done|canceled>

# Update priority
todu task update <id> --priority <low|medium|high>

# Labels
todu task update <id> --add-label <label>
todu task update <id> --remove-label <label>

# Assignees
todu task update <id> --add-assignee <user>
todu task update <id> --remove-assignee <user>

# Other fields
todu task update <id> --title "New title"
todu task update <id> --description "New description"
todu task update <id> --due 2025-12-31

# Add comment
todu task comment <id> -m "Comment text" --format json
```

## Notes

- `todu task close` is shortcut for status "done"
- When closing, always add a comment (user-provided or summarized from activity)
- Comments must be valid markdown, professional and detailed
- Status "canceled" is spelled with one L
- Description must be valid markdown
