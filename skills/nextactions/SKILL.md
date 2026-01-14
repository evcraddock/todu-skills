---
name: nextactions
description: Use when user says "next action", "next actions", "what's next", "what should I work on next", "what do I need to do next", "next actions for *", or similar queries about what to work on. (plugin:core@todu)
allowed-tools: todu
---

# Next Actions

**This skill provides essential logic for determining next actions:**

- Parsing project name from user query if mentioned
- Running status-filtered queries for high-priority active tasks
- Including all active tasks scheduled for today
- Including all active tasks from the default project (e.g., Inbox)
- Deduplicating results when tasks appear in multiple queries
- Sorting results by due date
- Displaying results in a single unified table

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new next actions request.

---

This skill shows the user's next actions by listing high priority active tasks
and all active tasks from the default project using the `todu task list` CLI
command.

## When to Use

- User explicitly mentions "next action" or "next actions"
- User asks "what should I work on next"
- User asks "what's next"

## What This Skill Does

1. **Parse Query**
   - Check if user mentioned a specific project name
   - Extract project name if present (e.g., "next actions for todu-skills")

2. **Get Default Project**
   - Run `todu config show` to get the default project name
   - Extract the value after "Project:" in the Defaults section (e.g., "Inbox")
   - If value is "(not set)" or empty, skip the default project query

3. **Build CLI Commands**
   - If user specifies a project, run TWO commands:
     - `todu task list --status active --priority high --project <name>`
     - `todu task list --status active --scheduled-date <YYYY-MM-DD> --project <name>`
       (today's date)
   - If NO project specified AND default project is set, run THREE commands:
     - `todu task list --status active --priority high`
     - `todu task list --status active --scheduled-date <YYYY-MM-DD>` (today's
       date)
     - `todu task list --status active --project <default-project>` (all
       priorities)
   - If NO project specified AND default project is NOT set, run TWO commands:
     - `todu task list --status active --priority high`
     - `todu task list --status active --scheduled-date <YYYY-MM-DD>` (today's
       date)
   - Do NOT validate project name - if invalid, commands will return no results

4. **Process and Display Results**
   - Combine results from all queries
   - Deduplicate tasks (remove duplicates by task ID)
   - Sort by due date (tasks with due dates first, earliest first; tasks
     without due dates last)
   - Display as a single unified table (no section headers)

## Example Interactions

### Example 1: Next actions (all projects, default project set)

**User**: "What are my next actions?"

**Skill**:

1. No project specified
2. Gets default project from `todu config show` → "Inbox"
3. Executes:
   - `todu task list --status active --priority high`
   - `todu task list --status active --scheduled-date 2025-12-01`
   - `todu task list --status active --project Inbox`
4. Deduplicates results, sorts by due date, displays single table

### Example 2: Next actions for specific project

**User**: "Next actions for todu-skills"

**Skill**:

1. Extracts: project="todu-skills"
2. Executes (no default project query since user specified a project):
   - `todu task list --status active --priority high --project todu-skills`
   - `todu task list --status active --scheduled-date 2025-12-01 --project todu-skills`
3. Deduplicates results, sorts by due date, displays single table

### Example 3: Next actions (no default project set)

**User**: "What's next?"

**Skill**:

1. No project specified
2. Gets default project from `todu config show` → "(not set)"
3. Executes (skip default project query):
   - `todu task list --status active --priority high`
   - `todu task list --status active --scheduled-date 2025-12-01`
4. Deduplicates results, sorts by due date, displays single table

## CLI Command Reference

**Get default project:**

```bash
todu config show
# Extract value after "Project:" in Defaults section
# If "(not set)" or empty, skip default project query
```

**Next actions (all projects, default project set):**

```bash
todu task list --status active --priority high
todu task list --status active --scheduled-date 2025-12-01  # today's scheduled tasks
todu task list --status active --project Inbox  # default project tasks
```

**Next actions (all projects, NO default project):**

```bash
todu task list --status active --priority high
todu task list --status active --scheduled-date 2025-12-01  # today's scheduled tasks
```

**Next actions for specific project:**

```bash
todu task list --status active --priority high --project todu-skills
todu task list --status active --scheduled-date 2025-12-01 --project todu-skills
```

## Natural Language Parsing

Parse these patterns from user queries:

**Project identification:**

- "next actions for PROJECT" → `--project PROJECT`
- "next actions in PROJECT" → `--project PROJECT`
- "what's next for PROJECT" → `--project PROJECT`
- "PROJECT next actions" → `--project PROJECT`

**Trigger phrases:**

- "next action" / "next actions"
- "what's next"
- "what should I work on next"
- "what do I need to do next"

## Output Format

Display results as a single markdown table sorted by due date:

| ID  | Title                    | Project     | Due Date   |
|-----|--------------------------|-------------|------------|
| 159 | Benefits Enrollment      | ntrs        | 2025-12-02 |
| 218 | Convert weekly-review... | todu-skills | -          |
| 45  | Review PR                | Inbox       | -          |

- Tasks with due dates appear first, sorted earliest to latest
- Tasks without due dates appear last
- No section headers - just one unified table
- If no tasks found, display "No next actions found"
- Status and Priority columns are omitted (status is always "active", priority
  is implicit from the query logic)

## Notes

- Only query "active" status (not "inprogress" - those are current, not next)
- Always include all active tasks scheduled for today (use current date in
  YYYY-MM-DD format)
- Always include all active tasks from the default project (any priority)
- Skip default project query if default project is "(not set)" or empty
- Deduplicate tasks by ID when combining results from multiple queries
- Sort final results by due date (earliest first, nulls last)
- Display as single table without section headers
- Don't validate project names - let CLI handle invalid names gracefully
- Project names can be used with `--project` flag (not just IDs)
- Only include default project tasks when user does NOT specify a project
