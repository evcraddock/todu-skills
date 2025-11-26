---
name: nextactions
description: Use when user says "next action", "next actions", "what's next", "what should I work on next", "what do I need to do next", "next actions for *", or similar queries about what to work on. (plugin:core@todu)
---

# Next Actions

**This skill provides essential logic for determining next actions:**

- Parsing project name from user query if mentioned
- Running multiple status-filtered queries
- Displaying high-priority active tasks
- Displaying all active tasks from the default project (e.g., Inbox)
- Supporting project-specific next actions
- Formatting results in user-friendly display

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

3. **Build CLI Commands**
   - If user specifies a project, run TWO commands:
     - `todu task list --status inprogress --priority high --project <name>`
     - `todu task list --status active --priority high --project <name>`
   - If NO project specified, run THREE commands:
     - `todu task list --status inprogress --priority high`
     - `todu task list --status active --priority high`
     - `todu task list --status active --project <default-project>` (all
       priorities)
   - Do NOT validate project name - if invalid, commands will return no results

4. **Execute and Display Results**
   - Run the CLI commands
   - Combine and display the text output directly to the user
   - If showing default project tasks, group results clearly (e.g., "High
     Priority Tasks" and "Default Project Tasks")

## Example Interactions

### Example 1: Next actions (all projects)

**User**: "What are my next actions?"

**Skill**:

1. No project specified
2. Gets default project from `todu config show` → "Inbox"
3. Executes:
   - `todu task list --status inprogress --priority high`
   - `todu task list --status active --priority high`
   - `todu task list --status active --project Inbox`
4. Combines and displays the output directly to the user

### Example 2: Next actions for specific project

**User**: "Next actions for todu-skills"

**Skill**:

1. Extracts: project="todu-skills"
2. Executes (no default project query since user specified a project):
   - `todu task list --status inprogress --priority high --project todu-skills`
   - `todu task list --status active --priority high --project todu-skills`
3. Combines and displays the output directly to the user

### Example 3: What's next

**User**: "What should I work on next?"

**Skill**:

1. No project specified
2. Gets default project from `todu config show` → "Inbox"
3. Executes:
   - `todu task list --status inprogress --priority high`
   - `todu task list --status active --priority high`
   - `todu task list --status active --project Inbox`
4. Combines and displays the output directly to the user

## CLI Command Reference

**Get default project:**

```bash
todu config show
# Extract value after "Project:" in Defaults section (e.g., "Inbox")
```

**Next actions (all projects):**

```bash
todu task list --status inprogress --priority high
todu task list --status active --priority high
todu task list --status active --project Inbox  # default project tasks
```

**Next actions for specific project (no default project query):**

```bash
todu task list --status inprogress --priority high --project todu-skills
todu task list --status active --priority high --project todu-skills
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

## Notes

- Always search both "inprogress" and "active" statuses for high priority tasks
- Always include all active tasks from the default project (any priority)
- Get default project from `todu config show` → value after "Project:" in Defaults
- Display CLI output directly to user without modification
- Don't validate project names - let CLI handle invalid names gracefully
- Project names can be used with `--project` flag (not just IDs)
- Only include default project tasks when user does NOT specify a project
