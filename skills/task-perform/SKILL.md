---
name: task-perform
description: Start working on a task or habit and follow its instructions. Use when user says "get started on task #*", "work on task #*", "handle task #*", "do task #*", "work on habit #*", "handle habit #*", "do habit #*", or similar. (plugin:todu)
allowed-tools: todu, Bash, Read, Write, Edit, AskUserQuestion
---

# Perform Task

Views a task/habit and follows the instructions in its description.

## Process

1. View the task: `todu task show <id>`
2. Update status to inprogress: `todu task update <id> --status inprogress`
3. Read and understand the task description
4. Follow the instructions in the description
5. When work is complete, add a comment using task-comment-create skill (summarizes activity)
6. Ask user if they want to close the task

## CLI Commands

```bash
# View task details
todu task show <id>

# Set status to inprogress
todu task update <id> --status inprogress

# Close only if user confirms
todu task close <id>
```

## Examples

### Work on task

**User**: "Get started on task 42"

1. Runs `todu task show 42` to view details
2. Runs `todu task update 42 --status inprogress`
3. Follows instructions in task description
4. When complete, uses task-comment-create skill to add summary comment
5. Asks: "Close task #42?" (Yes / No)
6. If yes, runs `todu task close 42`

### Handle habit

**User**: "Do habit 15"

1. Runs `todu task show 15` to view details
2. Runs `todu task update 15 --status inprogress`
3. Follows instructions in habit description
4. When complete, uses task-comment-create skill to add summary comment
5. Asks: "Close task #15?" (Yes / No)
6. If yes, runs `todu task close 15`

## Notes

- Always set status to inprogress before starting work
- Follow task description as instructions
- Always use task-comment-create skill when work is complete
- Ask user before closing task
