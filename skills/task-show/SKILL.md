---
name: task-show
description: View task details. Use when user says "show task #*", "view task #*", "details of task *", "take a look at task #*", or similar. (plugin:todu)
allowed-tools: todu
---

# View Task Details

Shows task details using JSON CLI output and returns a consistent templated response.

## Process

### View by ID

1. Run: `todu task show <id> --format json`
2. Parse JSON (`task`, `comments`)
3. Render output using the template below

### Search by description

When user provides keywords instead of an ID:

1. Run: `todu task list --search "<keywords>" --format json`
2. If one match: run `todu task show <id> --format json`
3. If multiple matches: ask user to choose the task ID
4. Run: `todu task show <selected_id> --format json`
5. Render with the template below

### No ID provided

1. Try to infer from recent conversation context
2. If likely match: ask for confirmation
3. If unclear: ask for task ID or search keywords

## Output Template

Always return task details in this format:

```text
Task #<id>: <title>

Status: <status>
Priority: <priority>
Project ID: <project_id>
External ID: <external_id or ->
Source URL: <source_url or ->
Created: <created_timestamp>
Updated: <updated_timestamp>

Description:
<full description or "(none)">

Comments (<count>):
- [<timestamp>] <author>
  <comment line 1>
  <comment line 2>

- [<timestamp>] <author>
  <comment line 1>
```

Comment formatting rules:

- Put metadata (`[timestamp] author`) on its own line.
- Render comment body on following indented lines (2 spaces).
- Preserve original newlines from comment content.
- Keep markdown headings/lists as plain text (do not strip or reformat).
- Add a blank line between comments for readability.

If there are no comments:

```text
Comments (0):
- (none)
```

## CLI Commands

```bash
# View task (JSON)
todu task show <id> --format json

# Search for tasks (JSON)
todu task list --search "<keywords>" --format json
```

