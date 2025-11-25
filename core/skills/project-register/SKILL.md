---
name: core-project-register
description: >-
  MANDATORY skill for registering projects with nickname conflict resolution.
  NEVER call 'todu project add' directly - ALWAYS use this skill via the
  Skill tool. Use when user says "register project", "add project",
  "register *", "add * project", "register repo *", or similar queries to
  register a new project. (plugin:core@todu)
---

# Register Project

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY project
registration.**

**NEVER EVER call `todu project add` directly. This skill provides essential
logic beyond just running the CLI command:**

- Checking if project is already registered (avoiding duplicates)
- Generating smart nickname suggestions from repo/project names
- Handling nickname conflicts with user interaction via AskUserQuestion
- Providing clear feedback about registration status
- Proper error handling and JSON parsing

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new registration request.

---

This skill registers a project (GitHub repo, Forgejo repo, or local project) in
the project registry with intelligent nickname handling and conflict resolution.

## When to Use

- Before syncing a repo for the first time
- User explicitly requests to register a project
- Any operation that needs to ensure a project is registered
- Called by sync skills before syncing
- When creating a local-only project for task management

## What This Skill Does

1. **Check if Already Registered**
   - Run `todu project list --format json` to get all registered projects
   - Search for matching `external_id` (repo for GitHub/Forgejo) or matching
     `name` (for local projects)
   - If already registered, return the project name and success immediately
   - If not registered, proceed to step 2

2. **Generate Nickname Suggestion**
   - For GitHub/Forgejo repos: Extract repo name from owner/repo format
     (e.g., "evcraddock/todu" → "todu")
   - For local projects: Use provided project name or generate from context
   - Normalize to lowercase, replace spaces with hyphens

3. **Check for Nickname Conflicts**
   - Use the project list from step 1
   - Check if suggested nickname already exists in `name` field
   - If no conflict, proceed to register
   - If conflict exists, go to step 4

4. **Resolve Nickname Conflict (if needed)**
   - Use AskUserQuestion to present options:
     - Option 1: Suggested nickname with number appended (e.g., "todu2",
       "todu3")
     - Option 2: Suggested nickname with different variation
     - Option 3: User can select "Other" to provide custom nickname
   - Get user's choice
   - Check again if new nickname conflicts
   - If still conflicts, ask again with different suggestions
   - Continue until unique nickname is found

5. **Register the Project**
   - Run `todu project add` with:
     - `--name <chosen-nickname>` (this is the project name/nickname)
     - `--system <github|forgejo>` (optional - defaults to local if omitted)
     - `--external-id <owner/repo>` (for GitHub/Forgejo, auto-generated for
       local)
     - `--format json` (for structured output)
   - Parse the output to confirm success
   - Return success with registration details

## Example Interactions

**User**: (via sync skill) "Sync evcraddock/rott"
**Skill**:

- Runs: `todu project list --format json`
- Checks if evcraddock/rott is registered → Not found
- Suggests nickname: "rott"
- Checks for conflicts → No conflict
- Runs: `todu project add --name rott --system github
  --external-id evcraddock/rott --format json`
- Returns: "✅ Registered project 'rott' (evcraddock/rott)"

**User**: (via sync skill) "Sync evcraddock/todu"
**Skill**:

- Runs: `todu project list --format json`
- Checks if evcraddock/todu is registered → Already registered as "todu"
- Returns: "✅ Project 'todu' already registered (evcraddock/todu)"

**User**: (via sync skill) "Sync owner/repo-name" (nickname conflict exists)
**Skill**:

- Runs: `todu project list --format json`
- Checks if owner/repo-name is registered → Not found
- Suggests nickname: "repo-name"
- Checks for conflicts → "repo-name" already exists!
- Uses AskUserQuestion:

  ```text
  Question: "The nickname 'repo-name' is already in use. Choose a nickname:"
  Options:
    - "repo-name2" (suggested alternative)
    - "repo-name-owner" (variation with owner)
    - [Other - user can type custom]
  ```

- User selects: "repo-name2"
- Runs: `todu project add --name repo-name2 --system github
  --external-id owner/repo-name --format json`
- Returns: "✅ Registered project 'repo-name2' (owner/repo-name)"

## CLI Interface

**List all projects** (check if already registered):

```bash
todu project list --format json
```

Returns array of projects:

```json
[
  {
    "id": 1,
    "name": "todu",
    "description": "",
    "system_id": 1,
    "external_id": "evcraddock/todu",
    "status": "active",
    "sync_strategy": "bidirectional",
    "last_synced_at": "2025-11-19T20:15:43Z",
    "created_at": "2025-11-19T19:53:12Z",
    "updated_at": "2025-11-19T20:37:01Z"
  }
]
```

**Register new project**:

```bash
# GitHub
todu project add \
  --name <nickname> \
  --system github \
  --external-id <owner/repo> \
  --format json

# Forgejo
todu project add \
  --name <nickname> \
  --system forgejo \
  --external-id <owner/repo> \
  --format json

# Local (no external sync, system defaults to local)
todu project add \
  --name <nickname> \
  --format json
```

**Note**: The `--format json` flag may not currently output JSON for the `add`
command. Parse the text output or use `todu project show <id> --format json` to
verify registration.

Output on success (text format):

```text
Created project 2: rott
  System: 1
  External ID: evcraddock/rott
  Status: active
  Sync Strategy: bidirectional
```

## Nickname Conflict Resolution Flow

When a nickname conflict is detected:

1. **Generate Alternatives**:
   - Numbered: "nickname2", "nickname3", etc.
   - With owner: "nickname-owner"
   - With system: "nickname-gh", "nickname-fg", "nickname-td"

2. **Ask User**:

```python
AskUserQuestion(
    questions=[{
        "question": f"The nickname '{suggested}' is already in use for "
                    f"another project. Choose a nickname for {repo_or_project}:",
        "header": "Nickname",
        "multiSelect": false,
        "options": [
            {
                "label": f"{suggested}2",
                "description": "Add number suffix"
            },
            {
                "label": f"{suggested}-{owner}",
                "description": "Include owner/context in nickname"
            }
        ]
    }]
)
```

1. **Validate Choice**:
   - Check if user's chosen nickname also conflicts
   - If conflicts, ask again with different suggestions
   - Continue until unique nickname is found

## Integration Points

This skill is called by:

- `github:task-sync` - Before syncing GitHub repos
- `forgejo:task-sync` - Before syncing Forgejo repos
- `github:task-create` - Before creating issues in unregistered repos
- `forgejo:task-create` - Before creating issues in unregistered repos

## Notes

- Already-registered projects return success immediately (no duplicate
  registration)
- Nickname suggestions are smart: derived from repo/project name
- Conflict resolution is user-driven via AskUserQuestion
- All registration uses the `todu project add` CLI command
- Project names (nicknames) must be unique across all systems
- Use `todu project list --format json` to check for existing projects and
  conflicts
- Error handling: Check CLI exit codes and parse output for error messages
- The CLI stores projects in the todu database (configured via config.yaml)
