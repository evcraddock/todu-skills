---
name: core-habit-list
description: List and view habit templates. Use when user says "list habits", "show habits", "what habits am I tracking", "view my habits", "show my habits", "list tracked habits", or similar queries. (plugin:core@todu)
allowed-tools: todu, Bash
---

# List Habits

This skill lists and shows details of habit templates using
`todu template list --type habit` and `todu template show`.

## When to Use

- User wants to see their habits
- User says "list habits", "show habits", "what habits am I tracking", etc.
- User wants to see details of a specific habit
- User asks about their tracked habits

## What This Skill Does

1. **Parse Request for Filters**
   - Extract project name if specified
   - Extract active/inactive filter if mentioned
   - Extract specific template ID if user wants details

2. **Determine Command**
   - List all: `todu template list --type habit`
   - Show specific: `todu template show <id>`

3. **Execute Command**
   - Run with `--format json` for parsing if needed
   - Apply any filters (project, active status)

4. **Display Results**
   - Show habits in readable format
   - Include frequency/schedule
   - Show active/inactive status

## CLI Commands

**List all habits:**

```bash
todu template list --type habit
```

**List with filters:**

```bash
# Filter by project
todu template list --type habit --project myproject

# Filter by active status
todu template list --type habit --active true
todu template list --type habit --active false

# Combine filters
todu template list --type habit --project myproject --active true
```

**Show specific habit:**

```bash
todu template show <id>
```

## Available Filters

| Filter  | Flag        | Values              | Description              |
|---------|-------------|---------------------|--------------------------|
| Type    | `--type`    | habit               | Always "habit" for this  |
| Project | `--project` | Project name or ID  | Filter by project        |
| Active  | `--active`  | true, false         | Filter by active status  |
| Limit   | `--limit`   | Number (default 50) | Max results to return    |
| Skip    | `--skip`    | Number              | Pagination offset        |

## Natural Language Parsing

| User says                      | Parsed filter/action            |
|--------------------------------|---------------------------------|
| "list habits"                  | `--type habit`                  |
| "show habits"                  | `--type habit`                  |
| "what habits am I tracking"    | `--type habit`                  |
| "view my habits"               | `--type habit`                  |
| "habits in PROJECT"            | `--type habit --project PROJECT`|
| "active habits"                | `--type habit --active true`    |
| "paused habits"                | `--type habit --active false`   |
| "show habit #5"                | `todu template show 5`          |
| "details of habit 5"           | `todu template show 5`          |

## Example Interactions

### Example 1: List all habits

**User**: "Show me my habits"

**Skill**:

1. Executes: `todu template list --type habit`
2. Displays list of all habit templates

### Example 2: Filter by project

**User**: "List habits in mytest"

**Skill**:

1. Parses: project="mytest"
2. Executes: `todu template list --type habit --project mytest`
3. Displays filtered list

### Example 3: Show active only

**User**: "Show active habits"

**Skill**:

1. Parses: active=true
2. Executes: `todu template list --type habit --active true`
3. Displays only active habits

### Example 4: Show specific habit

**User**: "Show details of habit #11"

**Skill**:

1. Parses: id=11
2. Executes: `todu template show 11`
3. Displays full habit details including:
   - Name
   - Frequency (human-readable)
   - Next occurrences
   - Project
   - Active status

### Example 5: What habits am I tracking

**User**: "What habits am I tracking?"

**Skill**:

1. Executes: `todu template list --type habit`
2. Displays all tracked habits

## Output Format

**List output:**

```text
ID  TITLE       RECURRENCE              TYPE   ACTIVE  PROJECT
--  -----       ----------              ----   ------  -------
11  exercise    Daily                   habit  yes     mytest
12  meditate    Daily                   habit  yes     mytest
13  read        Weekly on Mon, Wed, Fri habit  yes     Inbox

Total: 3 templates
```

**Show output (single habit):**

```text
Template #11: exercise
============================================================

Status:       active
Type:         habit
Project ID:   62

Recurrence:   FREQ=DAILY;INTERVAL=1
              (Daily)
Timezone:     UTC
Start Date:   2025-11-28

Created:      2025-11-28 19:28:37
Updated:      2025-11-28 19:28:37

Next Occurrences:
  1. Sat, Nov 29, 2025
  2. Sun, Nov 30, 2025
  3. Mon, Dec 1, 2025
  4. Tue, Dec 2, 2025
  5. Wed, Dec 3, 2025
```

Display CLI output directly to the user.

## No Results Handling

If no habits match the filters, display:

```text
No habits found.
```

If filters were applied, suggest:

```text
No habits found. Try:
- Removing the project filter
- Including paused habits with "show all habits"
```

## Future Considerations

When todu adds streak tracking for habits, update this skill to show:

- Current streak (consecutive completions)
- Longest streak
- Completion rate (e.g., "85% this month")
- Last completed date

## Error Handling

- **Habit not found**: "Habit #X not found"
- **Project not found**: "Project 'X' not found. Available projects: ..."
- **Invalid ID**: "Please provide a valid habit ID"
- **CLI errors**: Parse and display error message

## Notes

- Always use `--type habit` to filter for habits (not recurring tasks)
- Default shows all habits (both active and inactive)
- Use `--active true` to show only active habits
- Use `--active false` to show paused habits
- Template IDs are numeric
- Display CLI output directly - it's already human-readable
