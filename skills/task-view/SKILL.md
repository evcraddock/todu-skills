---
name: task-view
description: View task details. Use when user says "show task #*", "view task #*", "details of task *", "take a look at task #*", or similar. (plugin:todu)
allowed-tools: todu
---

# View Task Details

Displays full task details using `todu task show`.

## Examples

### View by ID

**User**: "View task 20"

Runs: `todu task show 20`

### Search by description

**User**: "Show me the auth bug"

1. Runs: `todu task list --search "auth bug"`
2. If single match: `todu task show <id>`
3. If multiple matches: ask user to select

### No ID provided

**User**: "Show me that task"

1. Try to infer from conversation context
2. If can infer: ask for confirmation
3. If cannot: ask for task ID or keywords

## CLI Commands

```bash
# View task
todu task show <id>

# Search for tasks
todu task list --search "<keywords>"
```

## Notes

- Display CLI output directly
- If no ID, try context inference or search by keywords
- Multiple search matches: prompt user to select
