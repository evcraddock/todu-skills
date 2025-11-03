---
name: core-task-update
description: MANDATORY skill for updating tasks/issues. NEVER call update scripts directly - ALWAYS use this skill via the Skill tool. Use when user wants to update, modify, mark, set, or change a task/issue. NO EXCEPTIONS WHATSOEVER.
---

# Update Task/Issue (Unified)

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY update request.**

**NEVER EVER call update scripts directly. This skill provides essential unified logic:**

- Unified ID resolution ("update issue 20")
- Natural language parsing ("mark issue 5 as done", "set priority high on task 12")
- System-specific ID resolution ("update github #15")
- Description search resolution ("mark auth bug as in-progress")
- Plugin-based routing to correct update script
- Validation of allowed values
- Handling ambiguous matches

---

This skill updates properties of tasks/issues in any system: status, priority, labels, assignees, close/reopen.

## When to Use

- User wants to update/modify/change a task property
- User wants to mark a task as done/complete/in-progress
- User wants to set priority or add labels
- User wants to close or cancel a task
- User wants to reopen a task
- User provides ANY update instruction for a task

## What This Skill Does

1. **Parse Update Request**
   - Extract task identifier (ID, description, etc.)
   - Parse what to update (status, priority, close, etc.)
   - Extract new values

2. **Resolve Task**
   - Use resolve_task() to find system + repo + number
   - Handle ambiguous matches with user prompts
   - Validate task exists

3. **Validate Updates**
   - Check allowed values for status/priority
   - Validate against system capabilities
   - Warn if unsupported (e.g., labels on Todoist)

4. **Route to Update Script**
   - Use plugin registry to get script path and build arguments
   - Call update script (system-agnostic via interface spec)

5. **Report Results**
   - Show what was updated
   - Display new values
   - Show task URL

## Natural Language Shortcuts

The skill understands these natural language patterns:

- **Status updates**:
  - "mark issue 20 as done" → status: done
  - "set task 5 to in-progress" → status: inprogress
  - "start working on issue 12" → status: inprogress
  - "mark as todo" → status: todo
  - "mark as waiting" → status: waiting
  - "set to blocked" → status: waiting
  - "waiting on external review" → status: waiting

- **Close/Complete**:
  - "close issue 20" → close with default reason
  - "complete task 5" → close/complete
  - "cancel issue 15" → close as cancelled
  - "mark as done" → complete

- **Priority**:
  - "set priority high on issue 20" → priority: high
  - "make task 5 urgent" → priority: urgent
  - "set priority low" → priority: low

- **Reopen**:
  - "reopen issue 20" → reopen
  - "unclose task 5" → reopen

## Example Interactions

### Example 1: Update Status by Unified ID

**User**: "Mark issue 20 as in-progress"

**Skill**:

1. Parses: ID=20, update=status:inprogress
2. Resolves ID 20 → github-evcraddock_todu-11
3. System=github, repo=evcraddock/todu, number=11
4. Calls update script via registry.build_args()
5. Shows: "✅ Updated issue #11 (evcraddock/todu) → Status: in-progress"

### Example 2: Close by Description

**User**: "Close the auth bug"

**Skill**:

1. Parses: description="auth bug", action=close
2. Searches for "auth bug" → finds ID 15
3. Resolves → forgejo-erik_vault-8
4. Calls update script via registry
5. Shows: "✅ Closed issue #8 (erik/Vault)"

### Example 3: Set Priority

**User**: "Set priority high on issue 5"

**Skill**:

1. Parses: ID=5, update=priority:high
2. Resolves → system + repo + number
3. Validates "high" is allowed priority
4. Calls update script with --priority high
5. Shows: "✅ Updated priority: high"

### Example 4: Multiple Updates

**User**: "Mark issue 20 as in-progress with high priority"

**Skill**:

1. Parses: ID=20, updates=[status:inprogress, priority:high]
2. Resolves task
3. Calls update script with both flags
4. Shows: "✅ Updated issue #20: status=in-progress, priority=high"

### Example 5: Ambiguous Match

**User**: "Mark sync task as done"

**Skill**:

1. Searches for "sync" → finds 3 matches
2. Prompts:

```
Found 3 tasks matching 'sync':
  [1] ID 15 - Fix sync timing issue
  [2] ID 22 - Add sync progress bar
  [3] ID 31 - Todoist sync not working

Which task? (1-3)
```

3. User selects #2
4. Updates that task

## Implementation Pseudocode

```python
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))
from resolve_task import resolve_task, AmbiguousTaskError
from plugin_registry import get_registry

def update_task():
    # 1. Parse user message
    identifier, updates = parse_update_request(user_message)
    # e.g., identifier="20", updates={'status': 'inprogress'}

    # 2. Resolve task
    try:
        task = resolve_task(identifier)
    except AmbiguousTaskError as e:
        task = prompt_user_to_select(e.matches)

    # 3. Validate updates
    validate_updates(updates, task['system'])

    # 4. Get script path and build args from interface
    registry = get_registry()
    script_path = registry.get_script_path(task['system'], 'update')
    args = registry.build_args(task['system'], 'update',
                                task_data=task, params=updates)

    # 5. Call script (system-agnostic)
    result = subprocess.run([str(script_path)] + args, ...)

    # 7. Display result
    print(f"✅ Updated {task['system']} issue #{task['number']}")
```

## Script Interface

All update scripts are called via the plugin registry's interface system. The skill uses `registry.build_args(system, 'update', task_data=task, params=updates)` which automatically builds the correct arguments.

**System-agnostic approach:**

```python
# Works for ANY system
registry = get_registry()
script_path = registry.get_script_path(task['system'], 'update')
args = registry.build_args(task['system'], 'update',
                            task_data=task,
                            params={'status': 'inprogress', 'priority': 'high'})
result = subprocess.run([str(script_path)] + args, ...)
```

**Output** (JSON to stdout - same format for all systems):

```json
{
  "updated": true,
  "changes": {
    "status": "inprogress",
    "priority": "high"
  },
  "url": "https://...",
  "title": "Fix auth bug"
}
```

## Allowed Values

### Status

- `todo` - Not started
- `inprogress` - Currently working on it
- `waiting` - Blocked/waiting on external factors
- `done` - Completed
- `canceled` - Abandoned/cancelled

### Priority

- `low` - Low priority
- `medium` - Normal priority
- `high` - High priority
- `urgent` - Critical/urgent

### Common Labels (GitHub/Forgejo)

- `bug`, `enhancement`, `documentation`
- `status:todo`, `status:inprogress`, `status:waiting`, `status:done`
- `priority:low`, `priority:medium`, `priority:high`

## Error Handling

- **Task not found**: "Task '{identifier}' not found"
- **Ambiguous matches**: Prompt user to select
- **Invalid value**: "'{value}' is not valid for {field}. Allowed: ..."
- **Unsupported operation**: "System '{system}' doesn't support {operation}"
- **Authentication errors**: Show token setup instructions
- **Network errors**: Suggest retry

## Success Criteria

- ✅ "mark issue 20 as done" works
- ✅ "set priority high on issue 5" works
- ✅ "close the auth bug" searches and updates
- ✅ "start working on task 12" sets status to inprogress
- ✅ Validation works (rejects invalid values)
- ✅ All three systems work
- ✅ Natural language parsing works
