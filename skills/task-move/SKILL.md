---
name: core-task-move
description: Move a task to a different project. Use when user says "move task #* to *", "transfer task #* to *", "move #* to project *", or similar queries to move a task between projects. (plugin:core@todu)
allowed-tools: todu
---

# Move Task to Different Project

This skill moves a task from one project to another using the `todu task move`
command.

## When to Use

- User wants to move/transfer a task to a different project
- User says "move task X to project Y"
- User says "transfer task X to Y"

## What This Skill Does

1. **Parse Move Request**
   - Extract task ID from user's request
   - Extract target project name from request
   - If task ID missing: try to infer from context or ask user
   - If project missing: ask user for target project

2. **Get Task Details**
   - Run `todu task show <id>` to get task title
   - If task not found: report error

3. **Confirm with User**
   - Use AskUserQuestion to confirm the move
   - Show task ID, title, and target project
   - Example: "Move task #20: Fix auth bug to todu-api?"

4. **Execute Move**
   - If confirmed: run `todu task move <id> --project <name>`
   - If declined: cancel operation

5. **Report Results**
   - Show confirmation that task was moved
   - Display the new task ID if provided in output

## What the CLI Does

The `todu task move` command:

- Creates a new task in the target project with the same fields (title,
  description, priority, labels, assignees, due date)
- Adds linking comments to both tasks
- Cancels the original task

## Example Interactions

### Example 1: Move task by ID

**User**: "Move task 20 to todu-api"

**Skill**:

1. Parses: ID=20, project=todu-api
2. Runs: `todu task show 20` to get title
3. Asks: "Move task #20: Fix auth bug to todu-api?"
4. User confirms
5. Executes: `todu task move 20 --project todu-api`
6. Shows: "Task #20 moved to todu-api"

### Example 2: Move task with hash prefix

**User**: "Transfer #42 to Inbox"

**Skill**:

1. Parses: ID=42, project=Inbox
2. Runs: `todu task show 42` to get title
3. Asks: "Move task #42: Review PR to Inbox?"
4. User confirms
5. Executes: `todu task move 42 --project Inbox`
6. Shows: "Task #42 moved to Inbox"

### Example 3: Infer task from context

**User**: (after discussing task #15) "Move it to homelab"

**Skill**:

1. Parses: no explicit ID, project=homelab
2. Infers from context: likely task #15
3. Runs: `todu task show 15` to get title
4. Asks: "Move task #15: Deploy service to homelab?"
5. User confirms
6. Executes: `todu task move 15 --project homelab`
7. Shows: "Task #15 moved to homelab"

### Example 4: User declines confirmation

**User**: "Move task 30 to Finances"

**Skill**:

1. Parses: ID=30, project=Finances
2. Runs: `todu task show 30` to get title
3. Asks: "Move task #30: Update budget to Finances?"
4. User declines
5. Shows: "Move cancelled"

### Example 5: Missing project

**User**: "Move task 20"

**Skill**:

1. Parses: ID=20, no project
2. Asks: "Which project should task #20 be moved to?"
3. User provides: "todu-api"
4. Continues with normal flow

## CLI Command Reference

**Get task details:**

```bash
todu task show <id>
```

**Move task:**

```bash
todu task move <id> --project <name>
```

**Example:**

```bash
todu task move 20 --project todu-api
```

## Natural Language Parsing

| User says                      | Parsed values              |
|--------------------------------|----------------------------|
| "move task 20 to todu-api"     | ID=20, project=todu-api    |
| "transfer #42 to Inbox"        | ID=42, project=Inbox       |
| "move task 15 to homelab"      | ID=15, project=homelab     |
| "move it to Finances"          | ID=infer, project=Finances |
| "move task 20"                 | ID=20, project=ask         |

## Error Handling

- **Task ID missing**: Try to infer from context or ask user
- **Project missing**: Ask user for target project
- **Task not found**: "Task #X not found. Please check the task ID."
- **Project not found**: Display CLI error message
- **User declines**: "Move cancelled"

## Notes

- Task ID must be provided or inferred from context
- Project can be specified by name or ID
- The original task is canceled after the move
- Both tasks get linking comments for traceability
- Always confirm with user before executing (destructive operation)
