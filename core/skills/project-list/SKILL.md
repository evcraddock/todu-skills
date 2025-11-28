---
name: project-list
description: >-
  Use when user says
  "list projects", "show projects", "list my projects", "show all projects",
  "what projects", "view projects", or similar queries to list registered
  projects. (plugin:core@todu)
allowed-tools: todu
---

# List Registered Projects

This skill lists registered projects using the `todu` CLI and displays the
output directly to the user.

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new list request.

---

## When to Use

- User explicitly mentions listing/showing/viewing projects
- User wants to see what projects are registered
- User wants to see projects for a specific system
- User asks "what projects do I have?"

## What This Skill Does

1. **Determine Filter Context**
   - Default: show all active projects (no priority filter)
   - If user mentions a specific system name: filter by that system
   - If user mentions a specific priority: filter by that priority
   - If user asks for "done" or "completed" projects: filter by done status
   - If user asks for "all" projects: show all regardless of status

2. **Load and Display Projects**
   - Call `todu project list` with appropriate filters
   - Display the CLI output directly to the user

## Example Interactions

**User**: "Show me my projects"
**Skill**:

- Calls: `todu project list --status active`
- Displays the CLI output to user

**User**: "List my projects for github"
**Skill**:

- Extracts system name from query
- Calls: `todu project list --system github --status active`
- Displays filtered results for that system only

**User**: "Show all my projects"
**Skill**:

- Calls: `todu project list`
- Displays all projects without filters (includes done projects)

**User**: "Show my high priority projects"
**Skill**:

- Calls: `todu project list --priority high --status active`
- Displays high priority active projects

**User**: "Show done projects"
**Skill**:

- Calls: `todu project list --status done`
- Displays completed/done projects

**User**: "What projects do I have?"
**Skill**:

- Calls: `todu project list --status active`
- Displays the CLI output to user

## CLI Interface

```bash
# List active projects (default)
todu project list --status active

# List all projects (including done)
todu project list

# Filter by specific system
todu project list --system github --status active

# Filter by priority
todu project list --priority high --status active
todu project list --priority medium --status active
todu project list --priority low --status active

# Show done/completed projects
todu project list --status done
```

**Output format example:**

```text
ID   NAME         SYSTEM   STATUS   PRIORITY
--   ----         ------   ------   --------
1    todu-skills  github   active   high
2    inbox        local    active   medium
3    old-project  github   done     low
```

## Search Patterns

Natural language queries the skill should understand:

**Default (active projects):**

- "show my projects" → `--status active`
- "list my projects" → `--status active`
- "what projects do I have?" → `--status active`

**System filter:**

- "show my github projects" → `--system github --status active`
- "list projects for local" → `--system local --status active`

**Priority filter:**

- "show high priority projects" → `--priority high --status active`
- "show low priority projects" → `--priority low --status active`
- "list medium priority projects" → `--priority medium --status active`

**Status filter:**

- "show done projects" → `--status done`
- "show completed projects" → `--status done`
- "list finished projects" → `--status done`

**All projects (no filters):**

- "show all my projects" → no filters
- "list all registered projects" → no filters
- "show everything" → no filters

## Empty Registry Handling

If no projects are registered:

- Inform user that no projects are registered
- Provide guidance on how to register a project using the `project-register`
  skill

## Notes

- Projects are managed by the todu API backend
- Default behavior shows active projects only (hides done projects)
- Use "all" keyword to include done projects
- Use this to see what projects can be used with sync or task creation
