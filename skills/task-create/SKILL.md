---
name: task-create
description: MANDATORY skill for creating tasks/issues in any system. NEVER call create scripts directly - ALWAYS use this skill via the Skill tool. Use when user says "create a task", "create an issue", "add a task", "add an issue", "new task", "create task for *", "add task to *", or similar queries to create a new task. (plugin:core@todu)
allowed-tools: todu
---

# Create Task/Issue (Unified)

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY create
request.**

**NEVER EVER call `todu task create` directly. This skill provides essential
logic beyond just running the CLI:**

- Parsing task details directly from user request
- Project selection and validation
- Using default project when available
- Interactive prompts only for missing required fields
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

1. **Parse Request for Details**
   - Extract project name if provided (e.g., "create task in todu-skills")
   - Extract title if provided (e.g., "called 'Fix the bug'" or after colon)
   - Extract priority if mentioned (e.g., "high priority task")
   - Extract status if mentioned (e.g., "waiting task") - defaults to active
   - Extract other optional fields if mentioned

2. **Identify Project**
   - If parsed from request: use it
   - If not provided: check for default project via `todu config show`
   - If default project exists: use it (inform user which project)
   - If no default: run `todu project list --format json` and ask user

3. **Gather Missing Required Fields**
   - **Title** (required): Only ask if not parsed from request

4. **Handle Optional Fields**
   - Only prompt for fields user explicitly mentioned but didn't provide value
   - Don't ask "would you like to add details?" - just use what was provided
   - If user says "with description" but didn't provide it, ask for description
   - If user provided everything needed, just create the task

5. **Create Task**
   - Build CLI command: `todu task create --project <name> --title <title>`
   - Add optional flags only if values were provided
   - Use `--format json` for parsing output
   - Execute command

6. **Display Confirmation**
   - Show created task details (ID, title, project)
   - Display external URL if available
   - Show success message

## Example Interactions

### Example 1: Full details in request

**User**: "Create a high priority task in todu-skills: Fix authentication bug"

**Skill**:

1. Parses: project="todu-skills", title="Fix authentication bug", priority=high
2. Executes: `todu task create --project todu-skills --title "Fix
   authentication bug" --priority high --format json`
3. Shows: "Created task #42: Fix authentication bug (todu-skills)"

### Example 2: Using default project

**User**: "Create a task: Update documentation"

**Skill**:

1. Parses: title="Update documentation", no project specified
2. Runs `todu config show` → default project is "Inbox"
3. Shows: "Using default project: Inbox"
4. Executes: `todu task create --project Inbox --title "Update documentation"
   --format json`
5. Shows: "Created task #43: Update documentation (Inbox)"

### Example 3: Minimal request

**User**: "Create a task"

**Skill**:

1. Parses: no project, no title
2. Runs `todu config show` → default project is "Inbox"
3. Asks for title: "What should this task be called?"
4. User provides: "Review PR #123"
5. Executes: `todu task create --project Inbox --title "Review PR #123"
   --format json`
6. Shows: "Created task #44: Review PR #123 (Inbox)"

### Example 4: No default project

**User**: "Create a task called 'Fix bug'"

**Skill**:

1. Parses: title="Fix bug", no project
2. Runs `todu config show` → default project is "(not set)"
3. Runs `todu project list --format json`
4. Asks: "Which project should this task belong to?"
   - todu-skills
   - todu-tests
   - my-project
5. User selects: "todu-skills"
6. Executes: `todu task create --project todu-skills --title "Fix bug"
   --format json`
7. Shows: "Created task #45: Fix bug (todu-skills)"

### Example 5: With multiple optional fields

**User**: "Create a task in todu-skills: Implement auth, high priority, due
2025-12-31"

**Skill**:

1. Parses: project="todu-skills", title="Implement auth", priority=high,
   due="2025-12-31"
2. Executes: `todu task create --project todu-skills --title "Implement auth"
   --priority high --due 2025-12-31 --format json`
3. Shows: "Created task #46: Implement auth (todu-skills)"

### Example 6: Waiting status

**User**: "Create a waiting task in Inbox: Wait for client response"

**Skill**:

1. Parses: project="Inbox", title="Wait for client response", status=waiting
2. Executes: `todu task create --project Inbox --title "Wait for client
   response" --status waiting --format json`
3. Shows: "Created task #47: Wait for client response (Inbox) [waiting]"

## Direct Parsing Patterns

Parse these patterns from user requests:

| User says                             | Parsed fields        |
|---------------------------------------|----------------------|
| "create task in PROJECT"              | project = PROJECT    |
| "create task called 'TITLE'"          | title = TITLE        |
| "create task: TITLE"                  | title = TITLE        |
| "create high priority task"           | priority = high      |
| "create low priority task"            | priority = low       |
| "create waiting task"                 | status = waiting     |
| "create task due 2025-12-31"          | due = 2025-12-31     |
| "create task with description 'TEXT'" | description = TEXT   |
| "create task labeled bug"             | labels = [bug]       |
| "create task assigned to alice"       | assignees = [alice]  |

Combine multiple patterns - e.g., "Create a high priority task in todu-skills:
Fix bug" parses project, priority, and title.

## CLI Interface

**Get default project:**

```bash
todu config show
# Extract value after "Project:" in Defaults section
# If "(not set)" or empty, ask user to select project
```

**List all projects** (if no default):

```bash
todu project list --format json
```

Returns array of projects with id, name, description, etc.

**Create task:**

```bash
# Minimal - just project and title
todu task create --project <name> --title <title> --format json

# With all optional fields
todu task create \
  --project <name> \
  --title <title> \
  --description <text> \
  --priority <low|medium|high> \
  --status <active|waiting> \
  --label <label1> --label <label2> \
  --assignee <user1> --assignee <user2> \
  --due <YYYY-MM-DD> \
  --format json
```

**Success output:**

```json
{
  "id": 42,
  "title": "Fix authentication bug",
  "description": "",
  "project_id": 1,
  "status": "active",
  "priority": "high",
  "due_date": null,
  "created_at": "2025-11-28T10:00:00Z",
  "updated_at": "2025-11-28T10:00:00Z"
}
```

## Available Fields

| Field       | Flag            | Required | Valid Values           | Default |
|-------------|-----------------|----------|------------------------|---------|
| Project     | `--project`     | Yes      | Any registered project | -       |
| Title       | `--title`       | Yes      | Any text               | -       |
| Description | `--description` | No       | Any text               | empty   |
| Priority    | `--priority`    | No       | low, medium, high      | medium  |
| Status      | `--status`      | No       | active, waiting        | active  |
| Labels      | `--label`       | No       | Any text (repeatable)  | none    |
| Assignees   | `--assignee`    | No       | Username (repeatable)  | none    |
| Due Date    | `--due`         | No       | YYYY-MM-DD format      | none    |

## Prompting Strategy

**Key principle**: Only ask for what's missing. Parse as much as possible from
the user's request.

1. **Project**:
   - If in request: use it
   - If default exists: use it (tell user)
   - Otherwise: ask user to select

2. **Title**:
   - If in request: use it
   - Otherwise: ask user

3. **Optional Fields**:
   - Only use values provided in request
   - Don't prompt for optional fields unless user explicitly mentioned them
     but didn't provide the value
   - Status defaults to "active" unless user explicitly says "waiting"

## Error Handling

- **No projects exist**: Inform user they need to register a project first
- **Project not found**: List available projects and suggest correct name
- **Invalid date format**: Explain YYYY-MM-DD format and ask again
- **CLI errors**: Parse error output and show message
- **Missing title**: Prompt user for title (required field)
- **No default project and none specified**: List projects and ask user

## Notes

- Project name can be used (not just ID) for --project flag
- Title is the only required field besides project
- Labels and assignees are repeatable flags (can specify multiple)
- Due date must be in YYYY-MM-DD format
- Always use --format json for parsing output
- Status defaults to "active" - only set to "waiting" if user explicitly asks
- Use default project from `todu config show` when available
- Parse as much as possible from user request to minimize prompts
