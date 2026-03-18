---
name: task-perform
description: Start working on a task or habit and follow its instructions. Use when user says "do task #*", "perform task #*", "execute task #*", "handle task #*", "work on task #*", "do habit #*", "handle habit #*", "work on habit #*", or similar. (plugin:todu)
allowed-tools: todu, Bash, Read, Write, Edit, AskUserQuestion
---

# Perform Task or Habit

Views a task or habit and follows the instructions in its description.

## Process

### If the target is a task

1. View the task: `todu task show <id>`
2. Start the task: `todu task start <id>`
3. Read and understand the task description
4. Follow the instructions in the description
5. When work is complete, add a note using the task-comment-create skill
6. Ask the user if they want to mark the task done

### If the target is a habit

1. View the habit: `todu habit show <id>`
2. Read and understand the habit description
3. Perform the habit
4. Ask the user if they want to check in for today
5. If yes, run `todu habit check <id>`

## CLI Commands

```bash
# Task flow

todu task show <id>
todu task start <id>
todu task done <id>

# Habit flow

todu habit show <id>
todu habit check <id>
```

## Examples

### Work on a task

**User**: "Get started on task 42"

1. Runs `todu task show 42` to view details
2. Runs `todu task start 42`
3. Follows instructions in the task description
4. When complete, uses task-comment-create to add a summary note
5. Asks: "Mark task #42 done?" (Yes / No)
6. If yes, runs `todu task done 42`

### Perform a habit

**User**: "Do habit 15"

1. Runs `todu habit show 15` to view details
2. Follows instructions in the habit description
3. Asks: "Check in habit #15 for today?" (Yes / No)
4. If yes, runs `todu habit check 15`

## Notes

- Always start a task before working on it unless it is already in progress
- Use task-comment-create when work on a task is complete
- Ask the user before marking a task done or checking in a habit
