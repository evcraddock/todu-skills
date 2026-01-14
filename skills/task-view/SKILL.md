---
name: core-task-view
description: >-
  MANDATORY skill for viewing task/issue details with comments. NEVER call
  view scripts directly - ALWAYS use this skill via the Skill tool. Use when
  user says "show task #*", "view task #*", "show #*", "view #*",
  "show me task *", "view issue *", "details of task *", or similar queries
  to view a specific task. (plugin:core@todu)
allowed-tools: todu
---

# View Task/Issue Details (Unified)

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY view
request.**

**This skill provides essential logic:**

- Parsing task ID from natural language requests
- Description search when ID not provided
- Inferring task from conversation context
- Handling ambiguous matches with user prompts
- Displaying full details with comments

---

This skill displays full details of a task/issue including title, description,
status, labels, comments, and more.

## When to Use

- User wants to view/show/display a task or issue
- User provides task ID ("view task 20")
- User provides description to search ("show auth bug task")
- User references task from context ("show me that task")

## What This Skill Does

1. **Parse Task Identifier**
   - Extract task ID from user request
   - If no ID, try to infer from conversation context and ask for confirmation
   - If cannot infer, search by description if keywords provided
   - If no keywords, ask user for task ID

2. **Handle Ambiguous Matches** (for description search)
   - If single match: display it
   - If multiple matches: prompt user to select
   - If no matches: inform user and suggest alternatives

3. **Fetch and Display Task**
   - Run `todu task show <id>` to get full details
   - Display formatted task details
   - Include title, status, priority, labels, assignees
   - Show full description
   - List all comments with authors and timestamps
   - Display external URL if available

## Example Interactions

### Example 1: View by task ID

**User**: "View task 20"

**Skill**:

1. Parses: ID=20
2. Executes: `todu task show 20`
3. Displays:

```text
Task #20: Fix authentication bug
============================================================

Status:      active
Priority:    high
Project ID:  1
External ID: 11
Source URL:  https://github.com/evcraddock/todu/issues/11
Created:     2025-10-15 10:00:00
Updated:     2025-10-20 15:30:00

Description:
Users are experiencing authentication failures when logging in
with OAuth providers.

Labels: bug, auth

Assignees: evcraddock

Comments (3):
  alice - 2025-10-16: I can reproduce this
  bob - 2025-10-17: PR #12 should fix it
  evcraddock - 2025-10-20: Merged, testing now
```

### Example 2: View by description search

**User**: "Show me the auth bug"

**Skill**:

1. Parses: no ID, keywords="auth bug"
2. Executes: `todu task list --search "auth bug"`
3. Finds single match: task #20
4. Executes: `todu task show 20`
5. Displays task details

### Example 3: Ambiguous description search

**User**: "Show task about sync"

**Skill**:

1. Parses: no ID, keywords="sync"
2. Executes: `todu task list --search "sync"`
3. Finds 3 matches
4. Prompts user with AskUserQuestion:
   - Question: "Found 3 tasks matching 'sync'. Which one?"
   - Options:
     - "#15 - Fix sync timing issue (todu-skills)"
     - "#22 - Add sync progress bar (todu-skills)"
     - "#31 - Sync not working (Inbox)"
5. User selects #15
6. Executes: `todu task show 15`
7. Displays task details

### Example 4: Infer from context

**User**: (after discussing task #42) "Show me that task"

**Skill**:

1. Parses: no explicit ID
2. Infers from context: likely task #42
3. Asks: "Did you mean task #42: Fix authentication bug?"
4. User confirms: "Yes"
5. Executes: `todu task show 42`
6. Displays task details

### Example 5: No task ID or keywords

**User**: "Show me a task"

**Skill**:

1. Parses: no ID, no keywords, no context
2. Asks: "Which task would you like to view? Please provide the task ID or
   describe the task."
3. User provides: "the one about documentation"
4. Executes: `todu task list --search "documentation"`
5. Continues with search flow

## CLI Interface

**View task by ID:**

```bash
todu task show <task-id>
```

**Search for tasks:**

```bash
todu task list --search "<keywords>"
```

**List available systems:**

```bash
todu system list
```

**Example:**

```bash
todu task show 20
```

**Output:**

```text
Task #20: Fix authentication bug
============================================================

Status:      active
Priority:    high
Project ID:  1
External ID: 11
Source URL:  https://github.com/evcraddock/todu/issues/11
Created:     2025-10-15 10:00:00
Updated:     2025-10-20 15:30:00

Description:
Users are experiencing authentication failures when logging in
with OAuth providers.

Labels: bug, auth

Assignees: evcraddock

Comments (3):
  alice - 2025-10-16: I can reproduce this
  bob - 2025-10-17: PR #12 should fix it
  evcraddock - 2025-10-20: Merged, testing now
```

## Natural Language Parsing

| User says                | Parsed action                           |
|--------------------------|-----------------------------------------|
| "view task 20"           | `todu task show 20`                     |
| "show task #42"          | `todu task show 42`                     |
| "view issue 15"          | `todu task show 15`                     |
| "show me task 20"        | `todu task show 20`                     |
| "details of task 30"     | `todu task show 30`                     |
| "show auth bug"          | Search for "auth bug", then show        |
| "view the sync task"     | Search for "sync", then show            |
| "show me that task"      | Infer from context, confirm, then show  |

## Resolution Flow

1. **Extract task ID** from request (numbers after "task", "issue", "#")
2. **If ID found**: run `todu task show <id>`
3. **If no ID but keywords**: run `todu task list --search "<keywords>"`
   - Single match: show it
   - Multiple matches: ask user to select
   - No matches: inform user
4. **If no ID and no keywords**: try to infer from context
   - If can infer: ask for confirmation
   - If cannot infer: ask user for task ID or keywords

## Error Handling

- **Task not found**: "Task #X not found. Please check the task ID."
- **No matches for search**: "No tasks found matching 'X'. Try different
  keywords or provide the task ID directly."
- **Ambiguous matches**: Prompt user to select from list
- **No task ID provided**: Try to infer from context or ask user

## Notes

- Task ID is the unified todu ID (numeric)
- Use `todu task list --search` for description-based search
- Available systems can be found via `todu system list`
- External URL links to the original issue (GitHub, Forgejo, etc.)
- Comments are displayed with author and timestamp
- Try to infer task from conversation context when ID not provided
