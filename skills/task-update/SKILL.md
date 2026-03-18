---
name: task-update
description: Update tasks/issues. Use when user says "update task #*", "mark task #* as *", "set priority on #*", "mark task done", "set task status to done", "quick close task", or similar. (plugin:todu)
allowed-tools: todu
---

# Update Task

Updates task properties using `todu task update`, `todu task start`,
`todu task done`, and `todu task cancel`.

## Closing Tasks - Note Required

**When completing a task, always add a note:**

1. If the user provides note text, use it
2. If no note text is provided, summarize the preceding activity on the task from the conversation and use that as the note

```bash
todu task done <id>
todu note add --task <id> "<summary of what was done>" --format json
```

## Natural Language Patterns

### Status Updates
- "mark task 39 as done" → `todu task done 39` + note
- "complete task 5" → `todu task done 5` + note
- "close task 20" → `todu task done 20` + note
- "start working on task 12" → `todu task start 12`
- "cancel task 18" → `todu task cancel 18`
- "set task 15 to active" → `todu task update 15 --status active`

### Priority
- "set priority high on task 20" → `todu task update 20 --priority high`

### Labels
- "add label bug to task 20" → show task, merge labels, then `todu task update 20 --label <full label set>`
- "remove label testing from task 5" → show task, subtract the label, then `todu task update 5 --label <remaining labels>`

### Other Fields
- "rename task 20" → `todu task update 20 --title "..."`
- "set task 20 due tomorrow" → `todu task update 20 --due <YYYY-MM-DD>`
- "schedule task 20 for Friday" → `todu task update 20 --scheduled <YYYY-MM-DD>`

## Examples

### Complete with provided note

**User**: "Close task 42: Fixed the authentication bug"

1. Runs: `todu task done 42`
2. Runs: `todu note add --task 42 "Fixed the authentication bug" --format json`

### Complete without note text (summarize activity)

**User**: "Mark task 39 as done"

1. Runs: `todu task done 39`
2. Summarizes preceding activity from the conversation
3. Runs: `todu note add --task 39 "<summary of work done>" --format json`

### Start work

**User**: "Start working on task 12"

Runs: `todu task start 12`

### Multiple updates

**User**: "Set task 15 to active with high priority"

Runs: `todu task update 15 --status active --priority high`

## CLI Commands

```bash
# Show current task when label changes require merge/replace logic

todu task show <id> --format json

# Start, complete, or cancel

todu task start <id>
todu task done <id>
todu task cancel <id>

# Update fields

todu task update <id> --status <status>
todu task update <id> --priority <low|medium|high>
todu task update <id> --title "New title"
todu task update <id> --description "New description"
todu task update <id> --due 2026-12-31
todu task update <id> --scheduled 2026-12-31
todu task update <id> --label label1 --label label2

# Add completion note

todu note add --task <id> "Note text" --format json
```

## Notes

- `todu task done` is the replacement for the old close command
- `todu task start` is the simplest way to mark a task in progress
- Labels are replaced as a full set when using `--label`, so read the current task first when the user asks to add or remove a single label
- When completing a task, always add a note (user-provided or summarized from activity)
- Notes must be valid markdown, professional, and specific
- Description must be valid markdown
