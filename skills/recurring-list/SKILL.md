---
name: recurring-list
description: List and view recurring task templates. Use when user says "list recurring tasks", "show recurring tasks", "what recurring tasks do I have", "view my recurring tasks", "show repeating tasks", "list scheduled tasks", or similar queries. (plugin:core@todu)
allowed-tools: todu, Bash
---

# List Recurring Tasks

This skill lists and shows details of recurring task templates using
`todu template list --type task` and `todu template show`.

## When to Use

- User wants to see their recurring tasks
- User says "list recurring tasks", "show recurring tasks", etc.
- User wants to see details of a specific recurring task
- User asks "what recurring tasks do I have"

## What This Skill Does

1. **Parse Request for Filters**
   - Extract project name if specified
   - Extract active/inactive filter if mentioned
   - Extract specific template ID if user wants details

2. **Determine Command**
   - List all: `todu template list --type task`
   - Show specific: `todu template show <id>`

3. **Execute Command**
   - Run with `--format json` for parsing if needed
   - Apply any filters (project, active status)

4. **Display Results**
   - Show recurring tasks in readable format
   - Include next occurrence dates
   - Show active/inactive status

## CLI Commands

**List all recurring tasks:**

```bash
todu template list --type task
```

**List with filters:**

```bash
# Filter by project
todu template list --type task --project myproject

# Filter by active status
todu template list --type task --active true
todu template list --type task --active false

# Combine filters
todu template list --type task --project myproject --active true

# Pagination
todu template list --type task --limit 10 --skip 0
```

**Show specific template:**

```bash
todu template show <id>
```

## Available Filters

| Filter  | Flag        | Values              | Description              |
|---------|-------------|---------------------|--------------------------|
| Type    | `--type`    | task                | Always "task" for this   |
| Project | `--project` | Project name or ID  | Filter by project        |
| Active  | `--active`  | true, false         | Filter by active status  |
| Limit   | `--limit`   | Number (default 50) | Max results to return    |
| Skip    | `--skip`    | Number              | Pagination offset        |

## Natural Language Parsing

| User says                         | Parsed filter/action               |
|-----------------------------------|------------------------------------|
| "list recurring tasks"            | `--type task`                      |
| "show recurring tasks"            | `--type task`                      |
| "recurring tasks in PROJECT"      | `--type task --project PROJECT`    |
| "active recurring tasks"          | `--type task --active true`        |
| "inactive recurring tasks"        | `--type task --active false`       |
| "paused recurring tasks"          | `--type task --active false`       |
| "show recurring task #5"          | `todu template show 5`             |
| "details of recurring task 5"     | `todu template show 5`             |
| "what recurring tasks do I have"  | `--type task`                      |

## Example Interactions

### Example 1: List all recurring tasks

**User**: "Show me my recurring tasks"

**Skill**:

1. Executes: `todu template list --type task`
2. Displays list of all recurring task templates

### Example 2: Filter by project

**User**: "List recurring tasks in todu-skills"

**Skill**:

1. Parses: project="todu-skills"
2. Executes: `todu template list --type task --project todu-skills`
3. Displays filtered list

### Example 3: Show active only

**User**: "Show active recurring tasks"

**Skill**:

1. Parses: active=true
2. Executes: `todu template list --type task --active true`
3. Displays only active templates

### Example 4: Show specific template

**User**: "Show details of recurring task #7"

**Skill**:

1. Parses: id=7
2. Executes: `todu template show 7`
3. Displays full template details including:
   - Title
   - Recurrence pattern (human-readable)
   - Next occurrences
   - Project
   - Active status

### Example 5: List inactive/paused

**User**: "Show paused recurring tasks"

**Skill**:

1. Parses: active=false
2. Executes: `todu template list --type task --active false`
3. Displays inactive templates

## Output Format

**List output:**

```text
ID   TITLE           RECURRENCE              PROJECT   STATUS   NEXT
--   -----           ----------              -------   ------   ----
7    Weekly review   Weekly on Fri           mytest    active   Dec 5, 2025
8    Daily standup   Daily                   mytest    active   Nov 29, 2025
9    Monthly report  Monthly on day 1        Inbox     active   Dec 1, 2025

Total: 3 recurring tasks
```

**Show output (single template):**

```text
Template #7: Weekly review
============================================================

Status:       active
Type:         task
Project ID:   62

Recurrence:   FREQ=WEEKLY;BYDAY=FR
              (Weekly on Fri)
Timezone:     UTC
Start Date:   2025-11-28

Created:      2025-11-28 19:23:29
Updated:      2025-11-28 19:23:29

Next Occurrences:
  1. Fri, Dec 5, 2025
  2. Fri, Dec 12, 2025
  3. Fri, Dec 19, 2025
  4. Fri, Dec 26, 2025
  5. Fri, Jan 2, 2026
```

Display CLI output directly to the user.

## No Results Handling

If no recurring tasks match the filters, display:

```text
No recurring tasks found.
```

If filters were applied, suggest:

```text
No recurring tasks found. Try:
- Removing the project filter
- Including inactive tasks with "show all recurring tasks"
```

## Error Handling

- **Template not found**: "Recurring task #X not found"
- **Project not found**: "Project 'X' not found. Available projects: ..."
- **Invalid ID**: "Please provide a valid template ID"
- **CLI errors**: Parse and display error message

## Notes

- Always use `--type task` to filter for recurring tasks (not habits)
- Default shows all recurring tasks (both active and inactive)
- Use `--active true` to show only active templates
- Use `--active false` to show paused/inactive templates
- Template IDs are numeric
- Results are paginated (default limit 50)
- Display CLI output directly - it's already human-readable
