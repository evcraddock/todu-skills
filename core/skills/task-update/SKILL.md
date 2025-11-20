---
name: core-task-update
description: MANDATORY skill for updating tasks/issues. NEVER call update scripts directly - ALWAYS use this skill via the Skill tool. Use when user wants to update, modify, mark, set, or change a task/issue. NO EXCEPTIONS WHATSOEVER.
---

# Update Task/Issue (Unified)

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY update request.**

**NEVER EVER call `todu task update` or `todu task close` directly. This skill
provides essential logic:**

- Natural language parsing ("mark task 39 as done", "set priority high on task 12")
- Field extraction (status, priority, labels, assignees, title, description)
- Command selection (update vs close)
- Validation of values
- Providing clear feedback about changes

---

This skill updates properties of tasks using the `todu task update` and
`todu task close` CLI commands.

## When to Use

- User wants to update/modify/change a task property
- User wants to mark a task as done/complete/in-progress
- User wants to set priority or add labels
- User wants to close or cancel a task
- User wants to add or remove assignees
- User provides ANY update instruction for a task

## What This Skill Does

1. **Parse Update Request**
   - Extract task ID from user's request
   - Parse what to update (status, priority, labels, assignees, etc.)
   - Extract new values from natural language

2. **Determine CLI Command**
   - "mark as done" / "close" → `todu task close <id>`
   - All other updates → `todu task update <id> [flags]`

3. **Build CLI Command**
   - Add appropriate flags based on parsed updates:
     - `--status <status>` (active, waiting, done, canceled)
     - `--priority <priority>` (low, medium, high)
     - `--add-label <label>` (repeatable)
     - `--remove-label <label>` (repeatable)
     - `--add-assignee <user>` (repeatable)
     - `--remove-assignee <user>` (repeatable)
     - `--title <new title>`
     - `--description <new description>`
     - `--due <YYYY-MM-DD>`
     - `--format json`

4. **Execute Command**
   - Run the CLI command
   - Capture output

5. **Report Results**
   - Show what was updated
   - Confirm the changes
   - Display task ID

## Natural Language Patterns

The skill understands these natural language patterns:

### Status Updates

- "mark task 39 as done" → `todu task close 39`
- "set task 5 to waiting" → `todu task update 5 --status waiting`
- "start working on task 12" → `todu task update 12 --status active`
- "mark as active" → `--status active`
- "set to canceled" → `--status canceled`

### Close/Complete

- "close task 20" → `todu task close 20`
- "complete task 5" → `todu task close 5`
- "mark task 15 as done" → `todu task close 15`

### Priority

- "set priority high on task 20" → `todu task update 20 --priority high`
- "make task 5 low priority" → `todu task update 5 --priority low`
- "set priority medium" → `--priority medium`

### Labels

- "add label bug to task 20" → `todu task update 20 --add-label bug`
- "add labels bug and enhancement" → `--add-label bug --add-label enhancement`
- "remove label testing from task 5" → `todu task update 5 --remove-label testing`

### Assignees

- "assign task 20 to alice" → `todu task update 20 --add-assignee alice`
- "assign to alice and bob" → `--add-assignee alice --add-assignee bob`
- "unassign bob from task 5" → `todu task update 5 --remove-assignee bob`

### Title

- "rename task 20 to 'Fix auth bug'" → `todu task update 20 --title "Fix auth bug"`
- "change title to 'New title'" → `--title "New title"`

### Description

- "update description of task 20" → `todu task update 20 --description "New description"`

### Due Date

- "set due date to 2025-12-31 on task 20" → `todu task update 20 --due 2025-12-31`
- "remove due date" → `--due ""`

## Example Interactions

### Example 1: Close Task

**User**: "Mark task 39 as done"

**Skill**:

1. Parses: ID=39, action=close
2. Executes: `todu task close 39 --format json`
3. Shows: "✅ Task #39 closed successfully"

### Example 2: Update Status

**User**: "Set task 5 to waiting"

**Skill**:

1. Parses: ID=5, update=status:waiting
2. Executes: `todu task update 5 --status waiting --format json`
3. Shows: "✅ Task #5 updated: status=waiting"

### Example 3: Set Priority

**User**: "Set priority high on task 12"

**Skill**:

1. Parses: ID=12, update=priority:high
2. Executes: `todu task update 12 --priority high --format json`
3. Shows: "✅ Task #12 updated: priority=high"

### Example 4: Add Labels

**User**: "Add labels bug and enhancement to task 20"

**Skill**:

1. Parses: ID=20, add_labels=[bug, enhancement]
2. Executes: `todu task update 20 --add-label bug --add-label enhancement
   --format json`
3. Shows: "✅ Task #20 updated: added labels [bug, enhancement]"

### Example 5: Multiple Updates

**User**: "Set task 15 to active with high priority and assign to alice"

**Skill**:

1. Parses: ID=15, updates=[status:active, priority:high, add_assignee:alice]
2. Executes: `todu task update 15 --status active --priority high
   --add-assignee alice --format json`
3. Shows: "✅ Task #15 updated: status=active, priority=high, assignee=alice"

### Example 6: Remove Label

**User**: "Remove label testing from task 8"

**Skill**:

1. Parses: ID=8, remove_labels=[testing]
2. Executes: `todu task update 8 --remove-label testing --format json`
3. Shows: "✅ Task #8 updated: removed label [testing]"

## CLI Command Reference

**Close a task:**

```bash
todu task close <id> --format json
```

**Update status:**

```bash
todu task update <id> --status active --format json
todu task update <id> --status waiting --format json
todu task update <id> --status done --format json
todu task update <id> --status canceled --format json
```

**Update priority:**

```bash
todu task update <id> --priority low --format json
todu task update <id> --priority medium --format json
todu task update <id> --priority high --format json
```

**Add/remove labels:**

```bash
todu task update <id> --add-label bug --format json
todu task update <id> --add-label bug --add-label enhancement --format json
todu task update <id> --remove-label testing --format json
```

**Add/remove assignees:**

```bash
todu task update <id> --add-assignee alice --format json
todu task update <id> --add-assignee alice --add-assignee bob --format json
todu task update <id> --remove-assignee alice --format json
```

**Update title:**

```bash
todu task update <id> --title "New task title" --format json
```

**Update description:**

```bash
todu task update <id> --description "New description" --format json
```

**Update due date:**

```bash
todu task update <id> --due 2025-12-31 --format json
todu task update <id> --due "" --format json  # remove due date
```

**Combine multiple updates:**

```bash
todu task update <id> --status active --priority high --add-label bug \
  --add-assignee alice --format json
```

## Output Format

Both `todu task update` and `todu task close` output success messages:

- `todu task close 39` → "Task #39 closed successfully"
- `todu task update 39 --priority high` → "Task #39 updated successfully"

Always use `--format json` flag for consistent parsing, even though the output
is currently text-based.

## Allowed Values

### Status Values

- `active` - Task is active/in progress
- `waiting` - Blocked/waiting on external factors
- `done` - Completed (prefer using `todu task close` instead)
- `canceled` - Abandoned/cancelled

### Priority Values

- `low` - Low priority
- `medium` - Normal priority
- `high` - High priority

### Label Values

Any string value. Common conventions:

- `bug`, `enhancement`, `documentation`
- `priority:high`, `priority:medium`, `priority:low`
- `status:active`, `status:waiting`, `status:done`

### Assignee Values

Any username string. No validation at CLI level.

### Due Date Format

Must be in YYYY-MM-DD format or empty string to clear.

## Natural Language Parsing Guide

When parsing user requests:

1. **Extract Task ID**
   - Look for numbers: "task 39", "issue 20", "#15"
   - Task ID is required - if not found, ask user

2. **Detect Action**
   - "close", "complete", "mark as done" → use `todu task close`
   - Everything else → use `todu task update`

3. **Extract Updates**
   - Status: "set to active", "mark as waiting", "change to canceled"
   - Priority: "priority high", "make it low priority", "set priority medium"
   - Labels: "add label X", "remove label Y", "labels X and Y"
   - Assignees: "assign to X", "assigned to X and Y", "unassign X"
   - Title: "rename to X", "change title to X"
   - Description: "update description to X", "set description to X"
   - Due: "due 2025-12-31", "set due date to X"

4. **Handle Multiple Updates**
   - Combine all flags in a single command
   - Example: "--status active --priority high --add-label bug"

## Error Handling

- **Task ID missing**: "Please specify a task ID"
- **Task not found**: "Task #X not found"
- **Invalid status**: "Invalid status. Use: active, waiting, done, or canceled"
- **Invalid priority**: "Invalid priority. Use: low, medium, or high"
- **Invalid date format**: "Due date must be in YYYY-MM-DD format"
- **CLI errors**: Display the error message from the CLI

## Success Criteria

- ✅ "mark task 39 as done" → closes task
- ✅ "set priority high on task 5" → updates priority
- ✅ "add label bug to task 20" → adds label
- ✅ "assign to alice" → adds assignee
- ✅ "set task 12 to waiting with high priority" → multiple updates
- ✅ Natural language parsing works
- ✅ All update types supported

## Notes

- Always use `--format json` flag for consistency
- `todu task close` is a shortcut for setting status to "done"
- Multiple labels and assignees can be added/removed in one command
- Labels and assignees use `--add-X` and `--remove-X` flags
- Title and description are direct replacements (not append)
- Empty string for due date removes the due date
- Task ID must be provided (no description search)
