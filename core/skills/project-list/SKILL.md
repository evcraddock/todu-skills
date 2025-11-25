---
name: project-list
description: >-
  MANDATORY skill for listing registered projects. Use when user says
  "list projects", "show projects", "list my projects", "show all projects",
  "what projects", "view projects", or similar queries to list registered
  projects. (plugin:core@todu)
---

# List Registered Projects

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY list
projects request.**

**NEVER EVER call `todu project list` directly. This skill provides essential
logic beyond just running the CLI:**

- Parsing user intent to determine if they want all projects or filtered by
  system
- Fetching system information to map system IDs to names
- Formatting results in user-friendly display
- Handling empty project registry gracefully
- Providing guidance on how to register projects

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new list request.

---

This skill lists all registered projects using the `todu` CLI.

## When to Use

- User explicitly mentions listing/showing/viewing projects
- User wants to see what projects are registered
- User wants to see projects for a specific system (GitHub, Forgejo, local)
- User asks "what projects do I have?"

## What This Skill Does

1. **Determine Filter Context**
   - If user mentions "GitHub projects" - filter to system=github
   - If user mentions "Forgejo projects" - filter to system=forgejo
   - If user mentions "Local projects" - filter to system=local
   - Otherwise - show ALL registered projects

2. **Fetch System Information**
   - Call `todu system list --format json` to get system ID to name mapping
   - Build lookup table: system_id → identifier (e.g., 1 → "github")

3. **Load Projects**
   - Call `todu project list --format json` with optional `--system <name>`
     filter
   - Parse JSON response containing project details

4. **Display Results**
   - Group projects by system identifier (github, forgejo, local)
   - For each project show:
     - Name (bold)
     - External ID (repo path or project ID)
     - Created date
   - Show count of total registered projects

## Example Interactions

**User**: "Show me my registered projects"
**Skill**:

- Calls: `todu system list --format json` (to get system mapping)
- Calls: `todu project list --format json`
- Displays:

  ```text
  # Registered Projects (3)

  ## GITHUB

  **todu-api**
  - Repo: `evcraddock/todu-api`
  - Added: 2025-11-17T15:40:09Z

  ## FORGEJO

  **ishould**
  - Repo: `erik/ishould`
  - Added: 2025-11-17T15:45:41Z

  ## LOCAL

  **ntrs-mdu**
  - Project ID: `34f70dd7-ec1c-446a-a9ea-549fe79cf82b`
  - Added: 2025-11-17T15:47:13Z
  ```

**User**: "List my GitHub projects"
**Skill**:

- Extracts: system=github
- Calls: `todu system list --format json`
- Calls: `todu project list --format json --system github`
- Shows filtered results for GitHub only

**User**: "What projects do I have?"
**Skill**:

- Calls: `todu system list --format json`
- Calls: `todu project list --format json`
- Shows all registered projects grouped by system

## CLI Interface

```bash
# Get system information (for mapping system_id to identifier)
todu system list --format json

# List all projects
todu project list --format json

# Filter by specific system
todu project list --format json --system github
todu project list --format json --system forgejo
todu project list --format json --system local
```

System list returns:

```json
[
  {
    "id": 1,
    "identifier": "github",
    "name": "github.com",
    "url": "https://api.github.com",
    "created_at": "2025-11-17T15:38:31.934508Z",
    "updated_at": "2025-11-17T15:38:31.934508Z"
  }
]
```

Project list returns:

```json
[
  {
    "id": 1,
    "name": "todu-api",
    "system_id": 1,
    "external_id": "evcraddock/todu-api",
    "status": "active",
    "sync_strategy": "bidirectional",
    "last_synced_at": "2025-11-19T20:39:25.146981Z",
    "created_at": "2025-11-17T15:40:09.070442Z",
    "updated_at": "2025-11-19T20:39:25.22584Z"
  }
]
```

## Search Patterns

Natural language queries the skill should understand:

- "show my projects" → all projects
- "list my projects" → all projects
- "what projects are registered?" → all projects
- "show my GitHub projects" → filter by system=github
- "show my Forgejo projects" → filter by system=forgejo
- "show my Local projects" → filter by system=local
- "list all registered projects" → all projects

## Empty Registry Handling

If no projects are registered (empty JSON array):

- Inform user that no projects are registered
- Provide guidance on how to register a project using the `project-register`
  skill

## Display Format

Projects are grouped by system for clarity:

```text
# Registered Projects (5)

## GITHUB (2 projects)
**todu-api**
- Repo: `evcraddock/todu-api`
- Added: 2025-11-17T15:40:09Z

**todu.sh**
- Repo: `evcraddock/todu.sh`
- Added: 2025-11-17T15:41:13Z

## FORGEJO (2 projects)
**ishould**
- Repo: `erik/ishould`
- Added: 2025-11-17T15:45:41Z

**Vault**
- Repo: `erik/Vault`
- Added: 2025-11-17T15:45:41Z

## LOCAL (1 project)
**ntrs-mdu**
- Project ID: `34f70dd7-ec1c-446a-a9ea-549fe79cf82b`
- Added: 2025-11-17T15:47:13Z
```

## Implementation Details

1. **Fetch systems**: Call `todu system list --format json` to build
   system_id → identifier map
2. **Fetch projects**: Call `todu project list --format json` (optionally
   with `--system <name>`)
3. **Group by system**: Use `system_id` to look up system `identifier`, group
   projects
4. **Format output**: Display grouped projects in markdown with counts
5. **Handle empty**: If projects array is empty, show helpful message

## Notes

- Projects are managed by the todu API backend
- Each project has a name (not nickname) used for display
- Each project is associated with exactly one system via `system_id`
- The `external_id` contains the repo path or project identifier
- Registration dates are in `created_at` field (ISO 8601 format)
- Use this to see what projects can be used with sync or task creation
