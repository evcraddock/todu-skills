---
name: core-task-create
description: MANDATORY skill for creating tasks/issues in any system. NEVER call create scripts directly - ALWAYS use this skill via the Skill tool. Use when user wants to create an issue or task.
---

# Create Task/Issue (Unified)

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY create request.**

**NEVER EVER call create scripts directly. This skill provides essential unified logic:**

- Automatic system detection from git remote
- Project resolution and registration
- Git context extraction for rich issue details
- Plugin-based routing to correct create script
- Interactive prompts for title, description, labels
- Handling project selection when ambiguous

---

This skill creates new tasks/issues in any registered system with rich context from git.

## When to Use

- User wants to create an issue or task
- User says "create issue" or "new task"
- User provides explicit system ("create github issue")
- User provides project context ("create issue in vault")

## What This Skill Does

1. **Determine Target System and Project**
   - If explicit: "create github issue in evcraddock/todu"
   - If in git repo: detect from remote URL
   - If todoist: require project name/nickname
   - If ambiguous: prompt user

2. **Ensure Project is Registered**
   - Call `core:project-register` skill
   - Handle nickname conflicts
   - Auto-register if not exists

3. **Extract Git Context** (if available)
   - Current branch
   - Recent commits
   - Modified files
   - Include in issue description

4. **Gather Issue Details**
   - Prompt for title (required)
   - Prompt for description (optional, but include git context)
   - Prompt for labels (optional)
   - Prompt for priority (optional)
   - Prompt for assignees (optional, GitHub/Forgejo only)

5. **Route to Create Script**
   - Use plugin registry to get script path
   - Call system-specific create script:
     - GitHub: `github/scripts/create-issue.py`
     - Forgejo: `forgejo/scripts/create-issue.py`
     - Todoist: `todoist/scripts/create-task.py`

6. **Display Confirmation**
   - Show created issue/task details
   - Display URL
   - Show todu unified ID (after sync)

## Example Interactions

### Example 1: Create from Git Repo

**User**: "Create an issue" (while in evcraddock/todu repo)

**Skill**:
1. Detects git remote → github.com:evcraddock/todu
2. Determines: system=github, repo=evcraddock/todu
3. Ensures project registered as "todu"
4. Extracts git context:
   - Branch: feature/auth-fix
   - Commits: "Add login validation", "Fix cookie expiry"
   - Modified: src/auth.py, tests/test_auth.py
5. Prompts:
   - Title: "Fix authentication timeout bug"
   - Description: (pre-fills with git context)
   ```
   ## Context
   Branch: feature/auth-fix

   Recent commits:
   - Add login validation
   - Fix cookie expiry

   Modified files:
   - src/auth.py
   - tests/test_auth.py

   ## Description
   [User fills in details here]
   ```
   - Labels: "bug, auth"
   - Priority: "high"
6. Calls `github/scripts/create-issue.py`
7. Shows: "✅ Created issue #42: Fix authentication timeout bug"
   URL: https://github.com/evcraddock/todu/issues/42

### Example 2: Create Explicit System + Repo

**User**: "Create a github issue in evcraddock/rott"

**Skill**:
1. Parses: system=github, repo=evcraddock/rott
2. Ensures project registered
3. No git context (not in that repo)
4. Prompts for title, description, labels
5. Creates issue
6. Shows confirmation

### Example 3: Create Todoist Task

**User**: "Create a task in my daily project"

**Skill**:
1. Identifies: system=todoist
2. Resolves "daily" → todoist project 6f9j9mGWwQrvvRHF
3. Prompts for:
   - Title: "Review pull requests"
   - Description: "Check pending PRs in todu and vault repos"
   - Priority: "medium"
   - Due date: "today"
4. Calls `todoist/scripts/create-task.py`
5. Shows: "✅ Created task: Review pull requests (todoist-home)"

### Example 4: Ambiguous System

**User**: "Create an issue"

**Skill**:
1. Not in git repo, no context
2. Prompts: "Which system would you like to use?"
   - GitHub (2 projects)
   - Forgejo (2 projects)
   - Todoist (2 projects)
3. User selects: "GitHub"
4. Prompts: "Which project?"
   - evcraddock/todu
   - evcraddock/rott
5. User selects: "evcraddock/todu"
6. Proceeds with creation

## Git Context Extraction

When creating from a git repository, automatically include:

```markdown
## Git Context

**Branch**: feature/auth-fix

**Recent Commits**:
- abc1234 Add login validation
- def5678 Fix cookie expiry
- ghi9012 Update auth tests

**Modified Files**:
- M src/auth.py
- M tests/test_auth.py
- A src/utils/session.py

---

## Description
[User's description here]
```

## Implementation Pseudocode

```python
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))
from plugin_registry import get_registry
from git_context import get_git_context

def create_task():
    # 1. Determine target
    system, repo = determine_target(user_message)

    if not system:
        # Try git context
        context = get_git_context()
        if context and context['system']:
            system = context['system']
            repo = context['repo']

    # 2. Ensure registered
    # Call core:project-register

    # 3. Extract git context
    git_info = get_git_context() if system in ['github', 'forgejo'] else None

    # 4. Prompt for details
    title = prompt("Title: ")
    description = prompt_with_git_context("Description: ", git_info)
    labels = prompt("Labels (comma-separated): ")
    priority = prompt("Priority (low/medium/high): ")

    # 5. Get create script
    registry = get_registry()
    script_path = registry.get_script_path(system, 'create')

    # 6. Call script
    args = build_create_args(repo, title, description, labels, priority)
    result = subprocess.run([str(script_path)] + args, ...)

    # 7. Display confirmation
    output = json.loads(result.stdout)
    print(f"✅ Created {system} issue #{output['number']}: {title}")
    print(f"URL: {output['url']}")
```

## Script Interface

All create scripts follow this interface:

**GitHub/Forgejo Input**:
```bash
$SCRIPT_PATH --repo "owner/repo" \
  --title "Fix auth bug" \
  --body "Description here" \
  [--labels "bug,priority:high"] \
  [--assignees "@user1,@user2"] \
  [--priority high]
```

**Todoist Input**:
```bash
$SCRIPT_PATH --project-id "abc123" \
  --title "Review PRs" \
  --body "Description" \
  [--priority high] \
  [--due-date "2025-11-03"]
```

**Output** (JSON to stdout):
```json
{
  "created": true,
  "number": 42,
  "title": "Fix auth bug",
  "url": "https://github.com/owner/repo/issues/42",
  "system": "github",
  "repo": "owner/repo"
}
```

## System-Specific Details

### GitHub
- Supports: labels, assignees, milestones, projects
- Auto-detects from git remote
- Rich git context in description

### Forgejo
- Supports: labels, assignees, milestones
- Auto-detects from git remote
- Rich git context in description

### Todoist
- Requires project ID or nickname
- Supports: priority, due date, labels (as tags)
- No git context (personal tasks)

## Prompting Strategy

1. **Title** (always required):
   - Clear, concise summary
   - Examples shown to user

2. **Description** (optional but recommended):
   - Pre-populated with git context if available
   - User can add details below context

3. **Labels** (optional):
   - Suggest common labels based on title
   - E.g., "bug" if title contains "fix" or "error"

4. **Priority** (optional):
   - Default: medium
   - Accept: low, medium, high, urgent

5. **Assignees** (optional, GitHub/Forgejo only):
   - Accept @username format
   - Validate against repo collaborators

## Error Handling

- **No system context**: Prompt user to select
- **Project not found**: Offer to register
- **Authentication errors**: Show token setup
- **Validation errors**: Explain format and retry
- **Network errors**: Suggest retry

## Success Criteria

- ✅ "create issue" in git repo detects system
- ✅ "create github issue" explicit works
- ✅ "create todoist task" requires project
- ✅ Git context included when available
- ✅ All three systems work
- ✅ Interactive prompts guide user
