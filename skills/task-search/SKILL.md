---
name: task-search
description: Use when user says "list * tasks", "show * tasks", "find * tasks", "search * tasks", "* priority tasks", "tasks in *", "* bugs", "tasks assigned to *", or similar task listing/searching queries. (plugin:core@todu)
allowed-tools: todu
---

# Search Tasks and Issues

Search tasks using `todu task list` with natural language parsing.

## Default Behavior

**CRITICAL**: When status is NOT explicitly specified, run TWO commands:

```bash
todu task list --status inprogress [filters]
todu task list --status active [filters]
```

When status IS explicitly specified, run only that status.

Combine results from both queries, deduplicate by task ID, and display as a
single unified list.

## Examples

**"show me all my tasks"** (no status specified):

```bash
todu task list --status inprogress
todu task list --status active
```

**"list tasks in todu-tests"** (no status specified):

```bash
todu task list --project todu-tests --status inprogress
todu task list --project todu-tests --status active
```

**"show open tasks"** (status explicitly specified):

```bash
todu task list --status active
```

**"high priority bugs in todu-tests"** (no status specified):

```bash
todu task list --project todu-tests --priority high --label bug --status inprogress
todu task list --project todu-tests --priority high --label bug --status active
```

**"show completed tasks"** (status explicitly specified):

```bash
todu task list --status done
```

**"show all tasks including done"** (all statuses):

```bash
todu task list
```

**"tasks due this week"**:

```bash
todu task list --status inprogress --due-before 2025-12-05
todu task list --status active --due-before 2025-12-05
```

**"overdue tasks"** (due before today):

```bash
todu task list --status inprogress --due-before 2025-11-28
todu task list --status active --due-before 2025-11-28
```

## Natural Language Parsing

| User says                    | Parsed filter                           |
|------------------------------|-----------------------------------------|
| "tasks in PROJECT"           | `--project PROJECT`                     |
| "list PROJECT issues"        | `--project PROJECT`                     |
| "open tasks" / "active"      | `--status active`                       |
| "in progress" / "working on" | `--status inprogress`                   |
| "done" / "completed"         | `--status done`                         |
| "cancelled tasks"            | `--status cancelled`                    |
| "all tasks including done"   | no status filter                        |
| "high priority"              | `--priority high`                       |
| "medium priority"            | `--priority medium`                     |
| "low priority"               | `--priority low`                        |
| "bugs"                       | `--label bug`                           |
| "features"                   | `--label enhancement`                   |
| "assigned to USER"           | `--assignee USER`                       |
| "about TOPIC" / "find X"     | `--search TOPIC`                        |
| "due before DATE"            | `--due-before YYYY-MM-DD`               |
| "due after DATE"             | `--due-after YYYY-MM-DD`                |
| "due this week"              | `--due-before` (end of week)            |
| "overdue"                    | `--due-before` (today's date)           |

## Available Filters

| Filter           | Flag                 | Values                     |
|------------------|----------------------|----------------------------|
| Project          | `--project`          | Project name or ID         |
| Status           | `--status`           | inprogress, active, done   |
| Priority         | `--priority`         | low, medium, high          |
| Label            | `--label`            | Any label (repeatable)     |
| Assignee         | `--assignee`         | Any username               |
| Search           | `--search`           | Full-text search           |
| Due Before       | `--due-before`       | YYYY-MM-DD                 |
| Due After        | `--due-after`        | YYYY-MM-DD                 |
| Project Status   | `--project-status`   | active, done, cancelled    |
| Project Priority | `--project-priority` | low, medium, high          |

**Note**: Status also supports "cancelled". Labels use AND logic.

## Output Format

The CLI outputs a table:

```text
ID   TITLE                    STATUS      PRIORITY  PROJECT      DUE DATE
--   -----                    ------      --------  -------      --------
42   Fix authentication bug   active      high      todu-skills  2025-12-02
43   Update documentation     inprogress  medium    todu-skills  -
44   Review PR #123           active      low       Inbox        -

Total: 3 tasks
```

Display CLI output directly to the user.

## Combining Results

When running multiple queries (e.g., inprogress + active):

1. Run both commands
2. Combine results
3. Deduplicate by task ID (remove duplicates)
4. Display as a single unified table
5. If no tasks found, show "No tasks found matching your criteria"

## No Results Handling

If no tasks match the filters, display:

```text
No tasks found matching your criteria.
```

If filters were applied, suggest broadening the search:

```text
No tasks found. Try:
- Removing the priority filter
- Searching in a different project
- Including completed tasks with "show all tasks including done"
```

## Notes

- Default queries both "inprogress" and "active" statuses
- Use "all tasks including done" to see everything
- Labels use AND logic (all specified labels must match)
- Due date filters use YYYY-MM-DD format
- Project can be specified by name or ID
- Results are not limited - all matching tasks are shown
- Combine and deduplicate results when running multiple status queries
