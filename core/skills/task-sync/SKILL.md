---
name: core-task-sync
description: MANDATORY skill for syncing tasks/issues across all systems. NEVER call sync scripts directly - ALWAYS use this skill via the Skill tool. Use when user wants to sync any task system (GitHub, Forgejo, Todoist).
---

# Sync Tasks/Issues (Unified)

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY sync request.**

**NEVER EVER call sync scripts directly. This skill provides essential unified logic:**

- Automatic system detection from git remote or project nickname
- Ensuring project is registered before syncing (via core:project-register skill)
- Plugin-based routing to correct sync script
- Extracting repository from git remote automatically
- Prompting for which repo/project to sync when ambiguous
- Determining optimal sync strategy (full vs incremental)
- Formatting sync results in user-friendly summary
- Handling authentication errors gracefully
- Reporting what changed (new, updated, deleted)

Even if you've invoked this skill before in the conversation, you MUST invoke it again for each new sync request.

---

This skill syncs tasks/issues from any registered system (GitHub, Forgejo, Todoist) and stores them locally in normalized format.

## When to Use

- User explicitly mentions syncing/updating issues or tasks
- User says "sync" without specifying a system
- User wants to sync a specific project by nickname
- User provides a repo identifier (e.g., "owner/repo")

## What This Skill Does

1. **Determine Target System and Project**
   - If explicit identifier provided (e.g., "sync vault"), resolve via nickname
   - If in git repository, detect system from remote URL
   - If ambiguous, ask user which system/project to sync
   - Extract repo/project identifier

2. **Ensure Project is Registered**
   - Call the `core:project-register` skill with repo info
   - Skill handles nickname conflicts with user interaction
   - If already registered, continues immediately
   - If not registered, registers with smart nickname suggestion

3. **Route to Appropriate Sync Script**
   - Use plugin registry to get correct script path for system
   - Call system-specific sync script:
     - GitHub: `github/scripts/sync-issues.py`
     - Forgejo: `forgejo/scripts/sync-issues.py`
     - Todoist: `todoist/scripts/sync-tasks.py`
   - Script fetches from API and normalizes to standard format
   - Saves to `~/.local/todu/issues/*.json`
   - Updates unified ID registry
   - Updates sync metadata in `~/.local/todu/projects.json`

4. **Report Results**
   - Show how many items were synced
   - Report any new or updated items
   - Display sync timestamp
   - Show total task count for project

## Resolution Strategy

The skill determines which system and project to sync using this priority:

1. **Explicit project nickname**: "sync vault" → lookup in projects.json
2. **Explicit system + repo**: "sync github evcraddock/todu"
3. **Git remote detection**: If in git repo, extract from origin URL
4. **User prompt**: If ambiguous or no context, ask user

## Examples

### Example 1: Sync by Nickname

**User**: "Sync vault"

**Skill**:
1. Resolves "vault" → {system: forgejo, repo: erik/Vault}
2. Gets script path from plugin registry
3. Calls `forgejo/scripts/sync-issues.py --repo erik/Vault`
4. Shows: "✅ Synced 12 issues from Forgejo (erik/Vault) - 2 new, 1 updated"

### Example 2: Sync from Git Repository

**User**: "Sync" (while in evcraddock/todu git repo)

**Skill**:
1. Detects git remote → github.com:evcraddock/todu
2. Determines system: github, repo: evcraddock/todu
3. Ensures project registered as "todu"
4. Calls `github/scripts/sync-issues.py --repo evcraddock/todu`
5. Shows: "✅ Synced 1 issue from GitHub (evcraddock/todu) - 0 new, 0 updated"

### Example 3: Sync Explicit Repo

**User**: "Sync github evcraddock/rott"

**Skill**:
1. Parses explicit format → system: github, repo: evcraddock/rott
2. Ensures project registered
3. Calls `github/scripts/sync-issues.py --repo evcraddock/rott`
4. Shows sync results

### Example 4: Ambiguous Request

**User**: "Sync my tasks"

**Skill**:
1. Not in git repo, no context
2. Lists available systems with task counts:
   - GitHub: 2 projects (13 tasks)
   - Forgejo: 2 projects (12 tasks)
   - Todoist: 2 projects (2 tasks)
3. Asks: "Which project would you like to sync?"
4. User selects or provides nickname
5. Syncs selected project

## Implementation Steps

```python
import sys
import json
import subprocess
from pathlib import Path

# Import utilities
sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))
from plugin_registry import get_registry
from git_context import get_git_context

def sync_task():
    # 1. Determine target (from user input or git context)
    identifier = extract_identifier_from_user_message()

    if not identifier:
        # Try git context
        context = get_git_context()
        if context and context['repo']:
            identifier = context['repo']
            system = context['system']

    # 2. Resolve to system + repo
    if identifier:
        # Check if it's a nickname
        project = resolve_project(identifier)
        if project:
            system = project['system']
            repo = project['repo']

    # 3. Ensure project is registered
    # Call core:project-register skill

    # 4. Get script path from registry
    registry = get_registry()
    script_path = registry.get_script_path(system, 'sync')

    # 5. Call sync script
    result = subprocess.run(
        [str(script_path), '--repo', repo],
        capture_output=True,
        text=True
    )

    # 6. Parse and display results
    output = json.loads(result.stdout)
    print(f"✅ Synced {output['total']} from {system}")
```

## Script Interface

All sync scripts follow this interface:

**Input**:
```bash
$SCRIPT_PATH --repo "identifier" [--since "timestamp"]
```

**Output** (JSON to stdout):
```json
{
  "synced": 45,
  "new": 3,
  "updated": 2,
  "total": 45,
  "timestamp": "2025-11-03T00:00:00Z"
}
```

## Error Handling

- **Authentication errors**: Show friendly message with token setup instructions
- **Project not found**: Offer to register the project
- **Network errors**: Report error and suggest retry
- **Invalid identifier**: Explain format and ask for clarification

## Success Criteria

- ✅ "sync vault" works (nickname resolution)
- ✅ "sync todu" works (from git remote or nickname)
- ✅ "sync" in git repo works (auto-detection)
- ✅ "sync github evcraddock/todu" works (explicit)
- ✅ Results formatted and displayed clearly
- ✅ All three systems (GitHub, Forgejo, Todoist) work
