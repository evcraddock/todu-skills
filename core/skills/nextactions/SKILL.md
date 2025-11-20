---
name: nextactions
description: Use when user says "next action", "next actions", "what's next", "what should I work on next", "what do I need to do next", "next actions for *", or similar queries about what to work on. (plugin:core@todu)
---

# Next Actions

**This skill provides essential logic for determining next actions:**

- Parsing project name from user query if mentioned
- Running multiple status-filtered queries
- Displaying high-priority active tasks
- Supporting project-specific next actions
- Formatting results in user-friendly display

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new next actions request.

---

This skill shows the user's next actions by listing high priority active tasks
using the `todu task list` CLI command.

## When to Use

- User explicitly mentions "next action" or "next actions"
- User asks "what should I work on next"
- User asks "what's next"

## What This Skill Does

1. **Parse Query**
   - Check if user mentioned a specific project name
   - Extract project name if present (e.g., "next actions for todu-skills")

2. **Build CLI Commands**
   - **ALWAYS** run TWO commands to cover both statuses:
     - `todu task list --status inprogress --priority high`
     - `todu task list --status active --priority high`
   - If project name mentioned, add `--project <name>` to both commands
   - Do NOT validate project name - if invalid, commands will return no results

3. **Execute and Display Results**
   - Run both CLI commands
   - Combine and display the text output directly to the user

## Example Interactions

### Example 1: Next actions (all projects)

**User**: "What are my next actions?"

**Skill**:

1. No project specified
2. Executes:
   - `todu task list --status inprogress --priority high`
   - `todu task list --status active --priority high`
3. Combines and displays the output directly to the user

### Example 2: Next actions for specific project

**User**: "Next actions for todu-skills"

**Skill**:

1. Extracts: project="todu-skills"
2. Executes:
   - `todu task list --status inprogress --priority high --project todu-skills`
   - `todu task list --status active --priority high --project todu-skills`
3. Combines and displays the output directly to the user

### Example 3: What's next

**User**: "What should I work on next?"

**Skill**:

1. No project specified
2. Executes:
   - `todu task list --status inprogress --priority high`
   - `todu task list --status active --priority high`
3. Combines and displays the output directly to the user

## CLI Command Reference

**Next actions (all projects):**

```bash
todu task list --status inprogress --priority high
todu task list --status active --priority high
```

**Next actions for specific project:**

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

- Always search both "inprogress" and "active" statuses
- Always filter by "high" priority
- Display CLI output directly to user without modification
- Don't validate project names - let CLI handle invalid names gracefully
- Project names can be used with `--project` flag (not just IDs)
