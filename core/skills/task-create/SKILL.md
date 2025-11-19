---
name: core-task-create
description: MANDATORY skill for creating tasks/issues in any system. NEVER call create scripts directly - ALWAYS use this skill via the Skill tool. Use when user wants to create an issue or task.
---

# Create Task/Issue (Unified)

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY create request.**

**NEVER EVER call `todu task create` directly. This skill provides essential
logic beyond just running the CLI:**

- Project selection and validation
- Interactive prompts for required and optional fields
- Handling project selection when ambiguous
- Providing clear feedback about created tasks

---

This skill creates new tasks in the todu database using the `todu task create`
CLI command.

## When to Use

- User wants to create a task
- User says "create task" or "new task"
- User provides project context ("create task in todu-skills")
- User wants to add a task to a specific project

## What This Skill Does

1. **Identify Project**
   - Extract project name from user's request
   - If not provided, run `todu project list --format json` and ask which
     project to use

2. **Gather Required Fields**
   - **Title** (required): Use AskUserQuestion with "Other" option for text
     input

3. **Ask About Optional Fields**
   - Use AskUserQuestion: "Would you like to add optional details?"
   - Options: "Yes, add details" or "No, create with just title"

4. **Gather Optional Fields** (if user selected yes)
   - **Description**: Ask for task description
   - **Priority**: Use AskUserQuestion (low/medium/high)
   - **Labels**: Ask for comma-separated labels
   - **Due Date**: Ask for date in YYYY-MM-DD format
   - **Assignees**: Ask for comma-separated usernames

5. **Create Task**
   - Build CLI command: `todu task create --project <name> --title <title>`
   - Add optional flags if provided
   - Use `--format json` for parsing output
   - Execute command

6. **Display Confirmation**
   - Show created task details (ID, title, project)
   - Display external URL if available
   - Show success message

## Example Interactions

### Example 1: Create task with just title

**User**: "Create a task in todu-skills"

**Skill**:

1. Identifies project: "todu-skills"
2. Asks for title: "Fix authentication bug"
3. Asks: "Would you like to add optional details?"
   - User selects: "No, create with just title"
4. Executes: `todu task create --project todu-skills --title "Fix
   authentication bug" --format json`
5. Shows: "✅ Created task #42: Fix authentication bug (todu-skills)"

### Example 2: Create task with all details

**User**: "Create a new task"

**Skill**:

1. Runs `todu project list --format json`
2. Asks which project:
   - todu-skills
   - todu-tests
   - my-project
3. User selects: "todu-skills"
4. Asks for title: "Implement user authentication"
5. Asks: "Would you like to add optional details?"
   - User selects: "Yes, add details"
6. Gathers optional fields:
   - Description: "Add JWT-based authentication with refresh tokens"
   - Priority: "high"
   - Labels: "feature, auth, security"
   - Due date: "2025-12-31"
   - Assignees: "alice, bob"
7. Executes: `todu task create --project todu-skills --title "Implement user
   authentication" --description "Add JWT-based authentication with refresh
   tokens" --priority high --label feature --label auth --label security --due
   2025-12-31 --assignee alice --assignee bob --format json`
8. Shows: "✅ Created task #43: Implement user authentication (todu-skills)"

### Example 3: Project not specified

**User**: "Create a task"

**Skill**:

1. Runs `todu project list --format json`
2. Asks: "Which project should this task belong to?"
   - todu-skills
   - todu-tests
   - my-project
3. User selects: "todu-tests"
4. Continues with title and optional fields prompts

## CLI Interface

**List all projects** (to select which project to create task in):

```bash
todu project list --format json
```

Returns array of projects with id, name, description, etc.

**Create task** (requires project name and title):

```bash
# Minimal - just project and title
todu task create --project <name> --title <title> --format json

# With all optional fields
todu task create \
  --project <name> \
  --title <title> \
  --description <text> \
  --priority <low|medium|high> \
  --label <label1> --label <label2> \
  --assignee <user1> --assignee <user2> \
  --due <YYYY-MM-DD> \
  --format json
```

**Example:**

```bash
# Create task with just title
todu task create --project todu-skills --title "Fix bug" --format json

# Create task with all fields
todu task create \
  --project todu-skills \
  --title "Implement feature" \
  --description "Add user authentication" \
  --priority high \
  --label feature --label auth \
  --assignee alice \
  --due 2025-12-31 \
  --format json
```

**Output format**: The CLI outputs JSON when `--format json` is used. Parse
the output to extract task ID, title, and other details.

## Prompting Strategy

1. **Project Selection**:
   - If mentioned in request: extract and use
   - If not mentioned: list all projects and ask user to select

2. **Title** (required):
   - Use AskUserQuestion with "Other" option for text input
   - Clear, concise summary of the task

3. **Optional Fields Gate**:
   - Ask: "Would you like to add optional details?"
   - Options: "Yes, add details" / "No, create with just title"
   - Only gather optional fields if user selects "Yes"

4. **Optional Fields** (if requested):
   - **Description**: Ask for task description (text input)
   - **Priority**: Use AskUserQuestion with options (low/medium/high)
   - **Labels**: Ask for comma-separated labels
   - **Due Date**: Ask for date in YYYY-MM-DD format
   - **Assignees**: Ask for comma-separated usernames

## Error Handling

- **No projects exist**: Inform user they need to register a project first
- **Project not found**: List available projects and suggest correct name
- **Invalid date format**: Explain YYYY-MM-DD format and ask again
- **CLI errors**: Parse error output and show message
- **Missing title**: Prompt user for title (required field)

## Notes

- Project name can be used (not just ID) for --project flag
- Title is the only required field besides project
- Labels and assignees are repeatable flags (can specify multiple)
- Due date must be in YYYY-MM-DD format
- Always use --format json for parsing output
- Task is created in "active" status by default
