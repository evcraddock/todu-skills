---
name: core-task-update
description: MANDATORY skill for updating tasks/issues. NEVER call update scripts directly - ALWAYS use this skill via the Skill tool. Use when user says "update task #*", "mark task #* as *", "close task #*", "set priority on #*", "change status of #*", "mark #* done", "complete task #*", "set #* to *", or similar queries to modify a task. NO EXCEPTIONS WHATSOEVER. (plugin:core@todu)
allowed-tools: todu
---

# Update Task/Issue (Unified)

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY update
request.**

**NEVER EVER call `todu task update` or `todu task close` directly. This skill
provides essential logic:**

- Natural language parsing ("mark task 39 as done", "set priority high on
  task 12")
- Field extraction (status, priority, labels, assignees, title, description)
- Task verification before updating
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
   - If no task ID, try to infer from context (recent task discussed) and ask
     for confirmation, OR ask user for task ID
   - Parse what to update (status, priority, labels, assignees, etc.)
   - Extract new values from natural language

2. **Verify Task and Show Context**
   - Run `todu task show <id>` to verify task exists
   - Display task title so user confirms they're updating the right task
   - Example: "Updating task #39: Fix authentication bug"

3. **Determine CLI Command**
   - "mark as done" / "close" → `todu task close <id>`
   - All other updates → `todu task update <id> [flags]`

4. **Build CLI Command**
   - Add appropriate flags based on parsed updates:
     - `--status <status>` (active, inprogress, waiting, canceled, done)
     - `--priority <priority>` (low, medium, high)
     - `--add-label <label>` (repeatable)
     - `--remove-label <label>` (repeatable)
     - `--add-assignee <user>` (repeatable)
     - `--remove-assignee <user>` (repeatable)
     - `--title <new title>`
     - `--description <new description>`
     - `--due <YYYY-MM-DD>`

5. **Execute Command**
   - Run the CLI command
   - Capture output

6. **Report Results**
   - Show what was updated
   - Confirm the changes
   - Display task ID

## Natural Language Patterns

The skill understands these natural language patterns:

### Status Updates

- "mark task 39 as done" → `todu task close 39`
- "set task 5 to waiting" → `todu task update 5 --status waiting`
- "start working on task 12" → `todu task update 12 --status inprogress`
- "start task 12" → `todu task update 12 --status inprogress`
- "working on task 12" → `todu task update 12 --status inprogress`
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

- "update description of task 20" → `todu task update 20 --description "..."`

### Due Date

- "set due date to 2025-12-31 on task 20" → `todu task update 20 --due 2025-12-31`
- "remove due date" → `--due ""`

## Example Interactions

### Example 1: Close task

**User**: "Mark task 39 as done"

**Skill**:

1. Parses: ID=39, action=close
2. Runs: `todu task show 39` → title="Fix authentication bug"
3. Shows: "Updating task #39: Fix authentication bug"
4. Executes: `todu task close 39`
5. Shows: "Task #39 closed successfully"

### Example 2: Update status

**User**: "Set task 5 to waiting"

**Skill**:

1. Parses: ID=5, update=status:waiting
2. Runs: `todu task show 5` → title="Review PR"
3. Shows: "Updating task #5: Review PR"
4. Executes: `todu task update 5 --status waiting`
5. Shows: "Task #5 updated: status=waiting"

### Example 3: Start working on task

**User**: "Start working on task 12"

**Skill**:

1. Parses: ID=12, update=status:inprogress
2. Runs: `todu task show 12` → title="Implement feature"
3. Shows: "Updating task #12: Implement feature"
4. Executes: `todu task update 12 --status inprogress`
5. Shows: "Task #12 updated: status=inprogress"

### Example 4: No task ID provided (infer from context)

**User**: (after discussing task #42) "Mark it as done"

**Skill**:

1. Parses: no explicit ID, action=close
2. Infers from context: likely task #42
3. Asks: "Did you mean task #42: Fix authentication bug?"
4. User confirms: "Yes"
5. Executes: `todu task close 42`
6. Shows: "Task #42 closed successfully"

### Example 5: No task ID provided (ask user)

**User**: "Set priority high"

**Skill**:

1. Parses: no ID, update=priority:high
2. No clear context to infer task
3. Asks: "Which task would you like to update? Please provide the task ID."
4. User provides: "task 20"
5. Runs: `todu task show 20` → title="Update docs"
6. Shows: "Updating task #20: Update docs"
7. Executes: `todu task update 20 --priority high`
8. Shows: "Task #20 updated: priority=high"

### Example 6: Multiple updates

**User**: "Set task 15 to active with high priority and assign to alice"

**Skill**:

1. Parses: ID=15, updates=[status:active, priority:high, add_assignee:alice]
2. Runs: `todu task show 15` → title="Deploy to prod"
3. Shows: "Updating task #15: Deploy to prod"
4. Executes: `todu task update 15 --status active --priority high
   --add-assignee alice`
5. Shows: "Task #15 updated: status=active, priority=high, assignee=alice"

## CLI Command Reference

**Verify task exists:**

```bash
todu task show <id>
```

**Close a task:**

```bash
todu task close <id>
```

**Update status:**

```bash
todu task update <id> --status active
todu task update <id> --status inprogress
todu task update <id> --status waiting
todu task update <id> --status done
todu task update <id> --status canceled
```

**Update priority:**

```bash
todu task update <id> --priority low
todu task update <id> --priority medium
todu task update <id> --priority high
```

**Add/remove labels:**

```bash
todu task update <id> --add-label bug
todu task update <id> --add-label bug --add-label enhancement
todu task update <id> --remove-label testing
```

**Add/remove assignees:**

```bash
todu task update <id> --add-assignee alice
todu task update <id> --add-assignee alice --add-assignee bob
todu task update <id> --remove-assignee alice
```

**Update title:**

```bash
todu task update <id> --title "New task title"
```

**Update description:**

```bash
todu task update <id> --description "New description"
```

**Update due date:**

```bash
todu task update <id> --due 2025-12-31
todu task update <id> --due ""  # remove due date
```

**Combine multiple updates:**

```bash
todu task update <id> --status active --priority high --add-label bug \
  --add-assignee alice
```

**Success output:**

```text
Task #39 closed successfully
Task #39 updated successfully
```

## Allowed Values

### Status Values

- `active` - Task is ready to work on
- `inprogress` - Currently working on this task
- `waiting` - Blocked/waiting on external factors
- `done` - Completed (prefer using `todu task close` instead)
- `canceled` - Abandoned/canceled

### Priority Values

- `low` - Low priority
- `medium` - Normal priority
- `high` - High priority

### Label Values

Any string value. Common conventions:

- `bug`, `enhancement`, `documentation`

### Assignee Values

Any username string. No validation at CLI level.

### Due Date Format

Must be in YYYY-MM-DD format or empty string to clear.

## Natural Language Parsing Guide

When parsing user requests:

1. **Extract Task ID**
   - Look for numbers: "task 39", "issue 20", "#15"
   - If not found: try to infer from conversation context
   - If can infer: ask for confirmation ("Did you mean task #X?")
   - If cannot infer: ask user for task ID

2. **Detect Action**
   - "close", "complete", "mark as done" → use `todu task close`
   - "start", "working on", "begin" → `--status inprogress`
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

- **Task ID missing**: Try to infer from context or ask user
- **Task not found**: "Task #X not found. Please check the task ID."
- **Invalid status**: "Invalid status. Use: active, inprogress, waiting,
  done, or canceled"
- **Invalid priority**: "Invalid priority. Use: low, medium, or high"
- **Invalid date format**: "Due date must be in YYYY-MM-DD format"
- **CLI errors**: Display the error message from the CLI

## Notes

- `todu task close` is a shortcut for setting status to "done"
- Multiple labels and assignees can be added/removed in one command
- Labels and assignees use `--add-X` and `--remove-X` flags
- Title and description are direct replacements (not append)
- Empty string for due date removes the due date
- Task ID must be provided or inferred - updates are per-task only
- Verify task exists before updating to show context to user
- Status "canceled" is spelled with one L
