---
name: task-search
description: MANDATORY skill for searching tasks and issues across all registered projects. Use when user wants to find, list, show, or search tasks/issues. (plugin:core@todu)
---

# Search Tasks and Issues

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY search request.**

**This skill provides essential logic beyond just running the CLI:**

- Parsing natural language search criteria from user query
- Prompting for clarification when filters are ambiguous
- Resolving project names from user requests
- Formatting results in user-friendly display
- Grouping by project when showing multiple projects
- Handling empty results gracefully
- Supporting cross-project searches

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new search request.

---

This skill searches tasks across all registered projects using the `todu task
list` CLI command with filtering capabilities.

## When to Use

- User explicitly mentions searching/listing/finding tasks or issues
- User wants to search across all projects
- User wants to search a specific project by name
- User wants to filter tasks by status, priority, labels, or assignees

## What This Skill Does

1. **Parse Search Criteria**
   - Extract filters from user's natural language query
   - Common patterns:
     - Project name: "tasks in todu-tests", "list vault issues"
     - Status: "open tasks", "done tasks", "active tasks"
     - Priority: "high priority tasks", "low priority"
     - Labels: "bugs", "show enhancement tasks"
     - Assignee: "tasks assigned to alice", "my tasks"
     - Search text: "tasks about authentication"

2. **Build CLI Command**
   - Start with base: `todu task list --format json`
   - Add filters based on extracted criteria:
     - `--project <name>` (project name or ID)
     - `--status <status>` (active, done, archived)
     - `--priority <priority>` (low, medium, high)
     - `--label <label>` (repeatable for multiple labels)
     - `--assignee <username>`
     - `--search <text>` (full-text search)
     - `--limit 500` (max limit to get more results than default 50)

3. **Execute and Parse Results**
   - Run the CLI command
   - Parse JSON output
   - Extract task details and project information

4. **Format and Display**
   - **CRITICAL**: Always display unified todu ID as `#{id}`
   - Group by project if multiple projects in results
   - Show key fields: ID, title, status, priority, labels
   - Keep display concise and readable
   - Provide project context for each task

## Example Interactions

### Example 1: Search all tasks

**User**: "Show me all my tasks"

**Skill**:

1. Executes: `todu task list --format json --limit 500`
2. Fetches all projects to map project IDs to names
3. Groups results by project
4. Displays:

```text
Found 45 tasks across 3 projects:

## todu-tests (15 tasks)
#33: Sample task for testing (active, priority:high) [testing, sample]
#34: Another test task (active, priority:medium) [testing]
#35: Completed test task (done)
...

## test-github-repo (20 tasks)
#40: Fix GitHub integration (active, priority:high) [bug]
#41: Update documentation (active) [docs]
...

## test-forgejo-repo (10 tasks)
#50: Add Forgejo sync (active, priority:medium) [feature]
...
```

### Example 2: Filter by project

**User**: "List tasks in todu-tests"

**Skill**:

1. Extracts: project="todu-tests"
2. Executes: `todu task list --project todu-tests --format json --limit 500`
3. Displays:

```text
Found 15 tasks in todu-tests:

#33: Sample task for testing (active, priority:high) [testing, sample]
#34: Another test task (active, priority:medium) [testing]
#35: Completed test task (done)
...
```

### Example 3: Filter by status

**User**: "Show open tasks"

**Skill**:

1. Extracts: status="active" (maps "open" to "active")
2. Executes: `todu task list --status active --format json --limit 500`
3. Groups by project and displays active tasks

### Example 4: Multiple filters

**User**: "Show high priority bugs in todu-tests"

**Skill**:

1. Extracts: project="todu-tests", priority="high", label="bug"
2. Executes: `todu task list --project todu-tests --priority high --label bug
   --format json --limit 1000`
3. Displays filtered results

### Example 5: Search text

**User**: "Find tasks about authentication"

**Skill**:

1. Extracts: search="authentication"
2. Executes: `todu task list --search authentication --format json --limit
   500`
3. Displays tasks matching the search term

## CLI Command Reference

**List all tasks:**

```bash
todu task list --format json --limit 500
```

**Filter by project:**

```bash
todu task list --project todu-tests --format json --limit 500
todu task list --project 32 --format json --limit 500  # by ID
```

**Filter by status:**

```bash
todu task list --status active --format json --limit 500
todu task list --status done --format json --limit 500
```

**Filter by priority:**

```bash
todu task list --priority high --format json --limit 500
todu task list --priority medium --format json --limit 500
todu task list --priority low --format json --limit 500
```

**Filter by labels:**

```bash
todu task list --label bug --format json --limit 500
todu task list --label bug --label priority:high --format json --limit 500
```

**Filter by assignee:**

```bash
todu task list --assignee alice --format json --limit 500
```

**Full-text search:**

```bash
todu task list --search "authentication" --format json --limit 500
```

**Combine multiple filters:**

```bash
todu task list --project todu-tests --status active --priority high \
  --label bug --format json --limit 500
```

## JSON Output Format

The CLI returns an array of task objects:

```json
[
  {
    "id": 33,
    "external_id": "",
    "title": "Sample task for testing",
    "description": "This is a sample task",
    "project_id": 32,
    "status": "active",
    "priority": "high",
    "created_at": "2025-11-19T23:38:45.549852Z",
    "updated_at": "2025-11-19T23:38:45.549852Z",
    "labels": [
      {"id": 1, "name": "testing"},
      {"id": 2, "name": "sample"}
    ],
    "assignees": ["alice", "bob"]
  }
]
```

## Natural Language Parsing

Parse these patterns from user queries:

**Project identification:**

- "tasks in PROJECT" → `--project PROJECT`
- "list PROJECT issues" → `--project PROJECT`
- "PROJECT tasks" → `--project PROJECT`

**Status filtering:**

- "open tasks" / "active tasks" → `--status active`
- "done tasks" / "completed tasks" / "closed tasks" → `--status done`
- "archived tasks" → `--status archived`

**Priority filtering:**

- "high priority" → `--priority high`
- "medium priority" → `--priority medium`
- "low priority" → `--priority low`

**Label filtering:**

- "bugs" → `--label bug`
- "features" / "enhancements" → `--label enhancement`
- "tasks with label NAME" → `--label NAME`

**Assignee filtering:**

- "tasks assigned to USER" → `--assignee USER`
- "my tasks" → `--assignee CURRENT_USER` (if known)

**Text search:**

- "tasks about TOPIC" → `--search TOPIC`
- "find KEYWORD" → `--search KEYWORD`

## Display Formatting

### Multiple Projects

When results span multiple projects, group by project name:

```text
Found 45 tasks across 3 projects:

## todu-tests (15 tasks)
#33: Sample task for testing (active, priority:high) [testing, sample]
#34: Another test task (active, priority:medium) [testing]

## test-github-repo (20 tasks)
#40: Fix integration (active, priority:high) [bug]
#41: Update docs (active) [docs]
```

### Single Project

When filtering to one project, skip grouping:

```text
Found 15 tasks in todu-tests:

#33: Sample task for testing (active, priority:high) [testing, sample]
#34: Another test task (active, priority:medium) [testing]
#35: Completed test task (done)
```

### Task Display Format

Each task line should include:

- `#{id}:` - Unified todu ID (from `id` field)
- Title
- Status (if not obvious from context)
- Priority (if set)
- Labels in brackets `[label1, label2]`

**Example:**

```text
#33: Sample task for testing (active, priority:high) [testing, sample]
```

## Project Name Resolution

To map project IDs to names for grouping:

1. Run: `todu project list --format json`
2. Build a map of `id → name`
3. Use when grouping results by project

## Error Handling

**No tasks found:**

```text
No tasks found matching your criteria.
```

**No projects exist:**

```text
No projects registered. Register a project first using the project-register skill.
```

**Invalid filter values:**

- Validate status: must be "active", "done", or "archived"
- Validate priority: must be "low", "medium", or "high"
- If invalid, use closest match or omit filter and inform user

## Notes

- Always use `--format json` for parsing
- Use `--limit 500` to get maximum results (API limit is 500)
- Labels in the CLI output are objects with `id` and `name` fields
- Display label names only, not IDs
- Group by project when showing cross-project results
- The `id` field is the unified todu ID - always display as `#{id}`
- Project names can be used with `--project` flag (not just IDs)
- Multiple `--label` flags can be combined (AND logic)

## ID Display Format

**CRITICAL**: Always display the unified todu ID in the format `#{id}` when
listing tasks.

- The `id` field in the JSON response contains the unified todu ID (numeric)
- Display format: `#{id}` (e.g., `#66`, `#42`, `#33`)
- This is the ID users should reference when viewing, updating, or commenting on
  tasks
- Consistent ID format across all systems (GitHub, Forgejo, Todoist, Local)

Example:

- JSON has: `"id": 33, "project_id": 32`
- Display as: `#33: Sample task for testing`
