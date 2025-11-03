---
name: core-task-view
description: MANDATORY skill for viewing task/issue details with comments. NEVER call view scripts directly - ALWAYS use this skill via the Skill tool. Use when user wants to view, show, or display details of a task/issue.
---

# View Task/Issue Details (Unified)

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY view request.**

**NEVER EVER call view scripts directly. This skill provides essential unified logic:**

- Unified ID resolution (e.g., "view issue 20")
- System-specific ID resolution (e.g., "view github #15")
- Description search resolution (e.g., "view auth bug")
- Plugin-based routing to correct view script
- Fetching fresh data from API (not just cache)
- Displaying full details with comments
- Handling ambiguous matches with user prompts

---

This skill displays full details of a task/issue from any system, including title, description, status, labels, comments, and more.

## When to Use

- User wants to view/show/display a task or issue
- User provides unified ID ("view issue 20")
- User provides system-specific ID ("view github #15")
- User provides description to search ("show auth bug task")

## What This Skill Does

1. **Resolve Task Identifier**
   - Parse identifier from user request
   - Try unified ID lookup first
   - Try system-specific format (e.g., "github #15")
   - Try description search if neither works
   - If multiple matches, prompt user to select

2. **Get System and Details**
   - Look up task in ID registry or cache
   - Determine which system owns this task
   - Get repo/project identifier

3. **Fetch Fresh Data**
   - Use plugin registry to get script path and build arguments
   - Call view script (system-agnostic via interface spec)
   - Script fetches fresh data from API (not cache)
   - Returns full details including comments

4. **Display Results**
   - Show formatted task details
   - Include title, status, labels, assignees
   - Show full description
   - List all comments with authors and timestamps
   - Display URL for viewing in browser

## Resolution Examples

### By Unified ID
**User**: "view issue 20"
- Looks up ID 20 in registry
- Finds `github-evcraddock_todu-11.json`
- Calls view script via registry.build_args()

### By System-Specific ID
**User**: "show github #15"
- Searches cache for github issue #15
- Finds in evcraddock/rott
- Calls view script with those details

### By Description
**User**: "view auth bug"
- Searches all cached issues for "auth"
- If single match: displays it
- If multiple: prompts user to select
- If none: "No tasks found matching 'auth bug'"

## Example Interactions

### Example 1: View by Unified ID

**User**: "View issue 20"

**Skill**:
1. Looks up unified ID 20 → github-evcraddock_todu-11.json
2. Parses: system=github, repo=evcraddock/todu, number=11
3. Calls view script via registry
4. Displays:

```
Issue #11: Fix authentication bug
Status: open | Priority: high
Labels: bug, status:todo
Assigned: @evcraddock
Created: 2025-10-15 | Updated: 2025-10-20

Description:
Users are experiencing authentication failures when...

Comments (3):
  @alice - 2025-10-16: I can reproduce this
  @bob - 2025-10-17: PR #12 should fix it
  @evcraddock - 2025-10-20: Merged, testing now

URL: https://github.com/evcraddock/todu/issues/11
Todu ID: 20
```

### Example 2: Ambiguous Description

**User**: "Show task about sync"

**Skill**:
1. Searches for "sync" in all tasks
2. Finds 3 matches
3. Prompts:
```
Found 3 tasks matching 'sync':
  [1] ID 15 - Fix sync timing issue (github)
  [2] ID 22 - Add sync progress bar (forgejo)
  [3] ID 31 - Todoist sync not working (todoist)

Which task would you like to view? (1-3)
```
4. User selects, then displays that task

## Implementation Pseudocode

```python
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))
from resolve_task import resolve_task, AmbiguousTaskError
from plugin_registry import get_registry

def view_task():
    # 1. Get identifier from user message
    identifier = extract_from_user_message()  # "20", "github #15", "auth bug"

    # 2. Resolve to system + task_data
    try:
        task = resolve_task(identifier)
    except AmbiguousTaskError as e:
        # Prompt user to select from matches
        task = prompt_user_to_select(e.matches)

    # 3. Get plugin and build args from interface spec
    registry = get_registry()
    script_path = registry.get_script_path(task['system'], 'view')
    args = registry.build_args(task['system'], 'view', task_data=task)

    # 4. Call view script (system-agnostic)
    result = subprocess.run([str(script_path)] + args, ...)

    # 5. Display formatted output
    display_task_details(result.stdout)
```

## Script Interface

All view scripts are called via the plugin registry's interface system. The skill uses `registry.build_args(system, 'view', task_data=task)` which automatically builds the correct arguments based on the system's interface specification in `todu.json`.

**Example (no hardcoded system checks needed):**
```python
# Works for ANY system (github, forgejo, todoist, future systems)
registry = get_registry()
script_path = registry.get_script_path(task['system'], 'view')
args = registry.build_args(task['system'], 'view', task_data=task)
result = subprocess.run([str(script_path)] + args, ...)
```

**Output** (JSON to stdout - same format for all systems):
```json
{
  "id": 20,
  "title": "Fix auth bug",
  "description": "...",
  "state": "open",
  "status": "inprogress",
  "labels": ["bug"],
  "assignees": ["@user"],
  "priority": "high",
  "dueDate": null,
  "createdAt": "2025-10-15T10:00:00Z",
  "updatedAt": "2025-10-20T15:30:00Z",
  "url": "https://...",
  "comments": [
    {
      "author": "@alice",
      "body": "I can reproduce this",
      "createdAt": "2025-10-16T09:00:00Z"
    }
  ]
}
```

## Error Handling

- **Task not found**: "Task '{identifier}' not found. Try syncing first?"
- **Ambiguous matches**: Prompt user to select from list
- **Authentication errors**: Show friendly message with token setup
- **Network errors**: Suggest viewing from cache if available

## Success Criteria

- ✅ "view issue 20" works (unified ID)
- ✅ "show task abc123" works (Todoist)
- ✅ "view github #32" works (system-specific)
- ✅ "show auth bug" works (description search)
- ✅ Fresh data fetched from API
- ✅ Comments displayed
- ✅ All three systems work
