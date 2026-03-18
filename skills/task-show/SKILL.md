---
name: task-show
description: View task details. Use when user says "show task #*", "view task #*", "details of task *", "take a look at task #*", or similar. (plugin:todu)
allowed-tools: todu
---

# View Task Details

Shows task details using JSON CLI output and returns a consistent templated
response.

## Process

### View by ID

1. Run: `todu task show <id> --format json`
2. Run: `todu note list --task <id> --format json`
3. Parse the task JSON and attached notes
4. Render output using the template below

### Search by title keywords

When the user provides keywords instead of an ID:

1. Run: `todu task search "<keywords>" --format json`
2. If one match: run `todu task show <id> --format json`
3. If multiple matches: ask the user to choose the task ID
4. Run: `todu note list --task <selected_id> --format json`
5. Render with the template below

### No ID provided

1. Try to infer from recent conversation context
2. If there is a likely match, ask for confirmation
3. If unclear, ask for the task ID or title keywords

## Output Template

Always return task details in this format:

```text
Task <id>: <title>

Status: <status>
Priority: <priority>
Project ID: <project_id>
External ID: <external_id or ->
Source URL: <source_url or ->
Created: <created_timestamp>
Updated: <updated_timestamp>

Description:
<full description or "(none)">

Notes (<count>):
- [<timestamp>] <author>
  <note line 1>
  <note line 2>

- [<timestamp>] <author>
  <note line 1>
```

Note formatting rules:

- Put metadata (`[timestamp] author`) on its own line
- Render note content on following indented lines (2 spaces)
- Preserve original newlines from note content
- Keep markdown headings and lists as plain text (do not strip or reformat)
- Add a blank line between notes for readability

If there are no notes:

```text
Notes (0):
- (none)
```

## CLI Commands

```bash
# View task (JSON)

todu task show <id> --format json

# View notes attached to the task

todu note list --task <id> --format json

# Search for tasks by title (JSON)

todu task search "<keywords>" --format json
```
