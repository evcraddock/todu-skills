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

- Parsing user intent to determine if they want all projects or filtered by
  system
- Displaying CLI output directly to user
- Handling empty project registry gracefully
- Providing guidance on how to register projects

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new list request.

---

This skill lists all registered projects using the `todu` CLI.

## When to Use

- User explicitly mentions listing/showing/viewing projects
- User wants to see what projects are registered
- User wants to see projects for a specific system
- User asks "what projects do I have?"

## What This Skill Does

1. **Determine Filter Context**
   - If user mentions a specific system name - filter by that system
   - If user asks for "all" projects - show all regardless of priority
   - Otherwise - use default filters (high/medium priority)

2. **Load and Display Projects**
   - Call `todu project list` with appropriate filters
   - Display the CLI output directly to the user

## Example Interactions

**User**: "Show me my registered projects"
**Skill**:

- Calls: `todu project list --priority high --priority medium`
- Displays the CLI output to user

**User**: "List my projects for [system-name]"
**Skill**:

- Extracts system name from query
- Calls: `todu project list --system <system-name> --priority high --priority medium`
- Displays filtered results for that system only

**User**: "Show all my projects"
**Skill**:

- Calls: `todu project list`
- Displays all projects without default filters

**User**: "What projects do I have?"
**Skill**:

- Calls: `todu project list --priority high --priority medium`
- Displays the CLI output to user

## CLI Interface

```bash
# List projects with default filters (high/medium priority)
todu project list --priority high --priority medium

# List all projects without filters
todu project list

# Filter by specific system (with default filters)
todu project list --system <system-name> --priority high --priority medium
```

## Search Patterns

Natural language queries the skill should understand:

- "show my projects" → default filters (high/medium priority)
- "list my projects" → default filters (high/medium priority)
- "what projects do I have?" → default filters (high/medium priority)
- "show my [system-name] projects" → filter by system with default filters
- "show all my projects" → no filters, show everything
- "list all registered projects" → no filters, show everything

## Empty Registry Handling

If no projects are registered:

- Inform user that no projects are registered
- Provide guidance on how to register a project using the `project-register`
  skill

## Notes

- Projects are managed by the todu API backend
- Use this to see what projects can be used with sync or task creation
