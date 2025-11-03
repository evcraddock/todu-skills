---
name: core-task-comment-create
description: MANDATORY skill for adding comments to tasks/issues. NEVER call comment scripts directly - ALWAYS use this skill via the Skill tool. Use when user wants to add a comment to a task/issue.
---

# Add Comment to Task/Issue (Unified)

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY comment request.**

**NEVER EVER call comment scripts directly. This skill provides essential unified logic:**

- Unified ID resolution ("comment on issue 20")
- System-specific ID resolution ("add comment to github #15")
- Description search resolution ("comment on auth bug")
- Plugin-based routing to correct comment script
- Comment body prompting if not provided
- Handling ambiguous task matches

---

This skill adds comments to tasks/issues in any system.

## When to Use

- User wants to add a comment to a task/issue
- User says "comment on issue X"
- User says "add note to task Y"
- User provides comment with task identifier

## What This Skill Does

1. **Parse Comment Request**
   - Extract task identifier (ID, description, etc.)
   - Extract comment body if provided in request
   - If no body, will prompt user

2. **Resolve Task**
   - Use resolve_task() to find system + repo + number
   - Handle ambiguous matches with user prompts
   - Validate task exists

3. **Get Comment Body** (if not provided)
   - Prompt user for comment text
   - Can be multi-line
   - Support markdown formatting

4. **Route to Comment Script**
   - Use plugin registry to get script path and build arguments
   - Call comment script (system-agnostic via interface spec)

5. **Display Confirmation**
   - Show that comment was added
   - Display comment body
   - Show task URL

## Example Interactions

### Example 1: Comment with Body Included

**User**: "Comment on issue 20 saying 'Fixed in PR #42'"

**Skill**:
1. Parses: ID=20, body="Fixed in PR #42"
2. Resolves ID 20 → github-evcraddock_todu-11
3. System=github, repo=evcraddock/todu, number=11
4. Calls comment script via registry.build_args()
5. Shows:
```
✅ Added comment to issue #11 (evcraddock/todu)

Comment:
  Fixed in PR #42

URL: https://github.com/evcraddock/todu/issues/11#comment-123456
```

### Example 2: Comment with Prompt

**User**: "Add a comment to issue 15"

**Skill**:
1. Parses: ID=15, body=null
2. Resolves task
3. Prompts: "Enter comment (markdown supported):"
4. User enters:
```
Tested the fix and it works well.

Some notes:
- Performance is better
- No regressions found
- Ready to deploy
```
5. Adds comment
6. Shows confirmation

### Example 3: Comment by Description

**User**: "Comment on the auth bug: this is still happening in production"

**Skill**:
1. Parses: description="auth bug", body="this is still happening in production"
2. Searches for "auth bug" → finds ID 22
3. Resolves → forgejo-erik_vault-8
4. Calls forgejo comment script
5. Shows confirmation

### Example 4: Ambiguous Task

**User**: "Add comment to sync task"

**Skill**:
1. Searches for "sync" → finds 3 matches
2. Prompts:
```
Found 3 tasks matching 'sync':
  [1] ID 15 - Fix sync timing issue (github)
  [2] ID 22 - Add sync progress bar (forgejo)
  [3] ID 31 - Todoist sync not working (todoist)

Which task? (1-3)
```
3. User selects #2
4. Prompts for comment body
5. Adds comment

## Natural Language Parsing

The skill understands these patterns:

- "comment on issue 20 saying 'text here'"
- "add comment to task 15: text here"
- "comment on auth bug with 'text'"
- "note on issue 20: text here"
- "add note to github #42 saying text"

## Implementation Pseudocode

```python
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))
from resolve_task import resolve_task, AmbiguousTaskError
from plugin_registry import get_registry

def add_comment():
    # 1. Parse user message
    identifier, body = parse_comment_request(user_message)

    # 2. Resolve task
    try:
        task = resolve_task(identifier)
    except AmbiguousTaskError as e:
        task = prompt_user_to_select(e.matches)

    # 3. Get comment body if not provided
    if not body:
        body = prompt_multiline("Enter comment (markdown supported):")

    # 4. Get script path and build args from interface
    registry = get_registry()
    script_path = registry.get_script_path(task['system'], 'comment')
    args = registry.build_args(task['system'], 'comment',
                                task_data=task, params={'body': body})

    # 5. Call script (system-agnostic)
    result = subprocess.run([str(script_path)] + args, ...)

    # 7. Display confirmation
    output = json.loads(result.stdout)
    print(f"✅ Added comment to {task['system']} issue #{task['number']}")
    print(f"\nComment:\n  {body}\n")
    print(f"URL: {output['url']}")
```

## Script Interface

All comment scripts are called via the plugin registry's interface system. The skill uses `registry.build_args(system, 'comment', task_data=task, params={'body': body})` which automatically builds the correct arguments.

**System-agnostic approach:**
```python
# Works for ANY system
registry = get_registry()
script_path = registry.get_script_path(task['system'], 'comment')
args = registry.build_args(task['system'], 'comment',
                            task_data=task,
                            params={'body': 'Comment text here'})
result = subprocess.run([str(script_path)] + args, ...)
```

**Output** (JSON to stdout - same format for all systems):
```json
{
  "created": true,
  "comment_id": "123456",
  "body": "Comment text here",
  "url": "https://github.com/owner/repo/issues/15#comment-123456",
  "created_at": "2025-11-03T10:00:00Z"
}
```

## Markdown Support

Comments support markdown formatting:

```markdown
**Bold text**
*Italic text*
- Bullet points
- More points

Code blocks:
\`\`\`python
def hello():
    print("world")
\`\`\`

Links: [text](url)
```

## Multi-line Comments

When prompting for comment body:

1. Show instructions: "Enter comment (markdown supported, empty line to finish):"
2. Accept multiple lines
3. Stop on empty line or EOF
4. Preserve formatting

## Error Handling

- **Task not found**: "Task '{identifier}' not found. Try syncing first?"
- **Ambiguous matches**: Prompt user to select from list
- **Empty comment**: "Comment body cannot be empty. Please enter a comment."
- **Authentication errors**: Show token setup instructions
- **Network errors**: Suggest retry

## System Capabilities

Comment capabilities vary by system. Check `plugin.capabilities.comments` to determine support level. All systems support basic comments, but markdown rendering and features differ.

## Success Criteria

- ✅ "comment on issue 20" works (unified ID)
- ✅ "add comment to task abc123" works (Todoist)
- ✅ "comment on github #32" works (system-specific)
- ✅ "comment on auth bug" works (description search)
- ✅ Comment body prompted if not provided
- ✅ Markdown formatting preserved
- ✅ All three systems work
- ✅ Confirmation displayed with URL
