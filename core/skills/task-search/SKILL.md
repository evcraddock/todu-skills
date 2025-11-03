---
name: task-search
description: MANDATORY skill for searching tasks and issues across all registered projects. Use when user wants to find, list, show, or search tasks/issues. (plugin:core@todu)
---

# Search Tasks and Issues

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY search request.**

**This skill provides essential logic beyond just running scripts:**

- Parsing natural language search criteria from user query
- Prompting for clarification when filters are ambiguous
- Resolving project nicknames from the registry
- Formatting results in user-friendly display
- Detecting stale cache and suggesting sync
- Handling empty results gracefully
- Supporting cross-project searches

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new search request.

---

This skill searches locally cached tasks and issues across all registered
projects with filtering capabilities.

## When to Use

- User explicitly mentions searching/listing/finding tasks or issues
- User wants to search across all projects
- User wants to search a specific project by nickname
- Fast queries without hitting API (reads from local cache)

## What This Skill Does

1. **Determine Project Context**
   - If user mentions a project nickname - filter to that project
   - If in a git repo - detect which registered project it belongs to
   - Otherwise - search ALL projects and display unified results

2. **Parse Search Criteria**
   - Extract filters from user query
   - Prompt for clarification if needed
   - Common filters: project, status, assignee, labels

3. **Search Local Cache**
   - Invoke list-items script through plugin registry
   - Script reads from `~/.local/todu/issues/`
   - Returns matching items in requested format

4. **Display Results**
   - Show items in readable format
   - **IMPORTANT**: Display the unified todu ID (from `id` field), NOT system-specific numbers
   - Format: `#{id}` (e.g., `#66`, `#42`) - use the `id` field, NOT `systemData.number`
   - Include key details: todu ID, title, status, labels, project
   - Provide URLs for easy access
   - Group by project if showing multiple projects

## Example Interactions

**User**: "Show me my open tasks"
**Skill**:

- Detects current project context (if in a git repo)
- Invokes: `list-items --status open --format markdown`
- Displays:

  ```text
  Found 31 open items:

  #16: Fix Date format in daily report (priority:high)
    Project: todu
  #11: Create skill for downloading daily report (priority:high)
    Project: vault
  #58: Implement dark mode (enhancement, priority:medium)
    Project: daily
  ...
  ```

**User**: "Find bugs in the vault project"
**Skill**:

- Extracts: project=vault, labels=bug
- Invokes: `list-items --project vault --labels bug --format markdown`
- Shows filtered results from vault project

**User**: "Show high priority issues"
**Skill**:

- Searches for label="priority:high" across all projects
- Displays results grouped by project

**User**: "List vault issues"
**Skill**:

- Resolves "vault" from project registry
- Invokes: `list-items --project vault --format markdown`
- Displays: All issues from the vault project

## Script Interface

The script path is defined in the plugin's `todu.json` file. Invoke through
the plugin registry.

Common usage patterns:

```bash
# Search all projects
list-items --format markdown

# Filter by specific project
list-items --project vault --format markdown
list-items --project todu --format markdown

# Filter by status
list-items --status open --format markdown

# Filter by labels
list-items --labels "bug,priority:high" --format markdown

# Filter by assignee
list-items --assignee "username" --format markdown

# Combine filters
list-items --project vault --status open --labels bug --format markdown
```

Returns JSON array:

```json
[
  {
    "id": "156",
    "system": "forgejo",
    "type": "issue",
    "title": "Fix authentication timeout",
    "status": "open",
    "labels": ["bug", "priority:high"],
    "url": "https://forgejo.caradoc.com/owner/repo/issues/156",
    "assignees": [],
    "systemData": {
      "repo": "owner/repo",
      "number": 156
    }
  },
  {
    "id": "12345678",
    "system": "todoist",
    "type": "task",
    "title": "Review auth PR",
    "status": "open",
    "labels": ["priority:high", "review"],
    "url": "https://todoist.com/app/task/12345678",
    "systemData": {
      "project_id": "2203306141",
      "due": "2025-10-29"
    }
  }
]
```

## Search Patterns

Natural language queries the skill should understand:

- "show my tasks" → all items across all projects
- "list vault issues" → filter by project=vault
- "show todu tasks" → filter by project=todu
- "high priority tasks" → filter by labels containing "priority:high"
- "open tasks" / "active tasks" → filter by status=open
- "completed tasks" / "done tasks" → filter by status=closed
- "bugs" → filter by labels=bug
- "tasks assigned to me" → filter by assignee
- "urgent tasks due soon" → priority:high + may need to parse due dates
- "bugs in vault" → filter by project=vault, labels=bug

## Project Detection

When user doesn't specify a project:

1. Check if in a git repository
2. Check git remote against registered projects
3. If remote matches a registered project → suggest filtering to that project
4. Otherwise → search all projects

## Cache Management

- Cache location: `~/.local/todu/issues/`
- All projects write to consolidated issues directory
- If cache is empty: Inform user and suggest running sync
- If cache is stale (>1 hour): Offer to sync before searching

## Display Format

When showing results from multiple projects, group by project:

```text
Found 15 items:

## todu (8 items)
#42: Fix auth bug (bug, priority:high)
#38: Update docs (documentation)
...

## vault (5 items)
#11: Create daily report skill (priority:high)
#8: Update README (documentation)
...

## daily (2 items)
#58: Implement dark mode (enhancement, priority:medium)
#61: Review PR #42 (priority:high, review)
...
```

When showing results from single project, omit grouping.

## Notes

- All searches use local cache (fast, offline-capable)
- Cross-project search is the default behavior
- Can combine multiple filters for precise searches
- Uses consolidated cache at `~/.local/todu/issues/`
- No API calls = fast and works offline

## ID Display Format

**CRITICAL**: Always display the unified todu ID in the format `#{id}` when listing tasks.

- The `id` field in the JSON response contains the unified todu ID (numeric)
- Display format: `#{id}` (e.g., `#66`, `#42`)
- Do NOT display system-specific IDs from `systemData.number`
- Always use the `id` field, NOT `systemData.number`
- Users should reference tasks using the unified todu ID for consistency across systems

Example:

- JSON has: `"id": 66, "systemData": {"number": 4, "repo": "erik/homelab"}`
- Display as: `#66: Add location detection to umami`
- NOT as: `#4: Add location detection to umami`
