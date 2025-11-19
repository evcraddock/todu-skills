---
name: project-delete
description: MANDATORY skill for deleting registered projects. NEVER call scripts/delete-project.py directly - ALWAYS use this skill via the Skill tool. Use when user wants to delete, remove, or unregister a project. (plugin:core@todu)
---

# Delete Registered Project

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY delete
project request.**

**NEVER EVER call `todu project remove` directly. This skill provides essential
logic beyond just running the CLI:**

- Confirming deletion with the user using AskUserQuestion
- Displaying project details before deletion
- Handling errors gracefully
- Providing clear feedback about the deletion

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new delete request.

---

This skill deletes a registered project from the todu database using the
`todu project remove` CLI command.

## When to Use

- User explicitly mentions deleting/removing/unregistering a project
- User says "delete project [name]"
- User wants to remove a fake or test project
- User asks to remove a project from the registry

## What This Skill Does

1. **Identify Project**
   - Extract the project name from user's request
   - If not provided, run `todu project list --format json` and ask which to
     delete

2. **Load Project Details**
   - Run `todu project list --format json` to get all projects
   - Find the project by name (case-insensitive search)
   - Extract the project `id` (needed for remove command)
   - Display project details to user

3. **Ask About Task Handling**
   - Use AskUserQuestion to ask if user wants to delete associated tasks
   - Options: "Delete project and tasks (--cascade)" or "Delete project only"
   - This determines whether to use the --cascade flag

4. **Confirm Deletion**
   - Use AskUserQuestion to confirm deletion
   - Show project details: name, description, status, system
   - Show whether tasks will be deleted (based on cascade choice)
   - Ask: "Are you sure you want to delete this project?"
   - Options: "Yes, delete" or "No, cancel"

5. **Delete Project**
   - If confirmed, call `todu project remove <id>` with appropriate flags
   - Use `--cascade` if user chose to delete tasks
   - Use `--force` to skip CLI's built-in confirmation (we already confirmed)
   - Parse output to confirm success
   - Display success message with deleted project details
   - If cancelled, inform user no changes were made

## Example Interactions

**User**: "Delete the todu-tests project"
**Skill**:

- Runs `todu project list --format json` to find 'todu-tests'
- Finds project with id=22, name="todu-tests"
- Shows project details:

  ```text
  Project to delete:
  - Name: todu-tests
  - Description: Test project for development
  - Status: active
  - System: local
  - External ID: 9a2e6561-dbf8-4ff1-bc6d-69f47a43947f
  ```

- Asks about task handling:
  - Question: "What should happen to tasks associated with this project?"
  - Options: "Delete project and tasks (--cascade)" / "Delete project only"
- User selects: "Delete project and tasks (--cascade)"
- Confirms deletion:
  - Question: "Are you sure you want to delete 'todu-tests'? This will also
    delete all associated tasks."
  - Options: "Yes, delete" / "No, cancel"
- If "Yes": Calls `todu project remove 22 --cascade --force --format json`
- Shows: "✅ Project 'todu-tests' has been deleted successfully."

**User**: "Remove the test project"
**Skill**:

- Runs `todu project list --format json` to find 'test'
- If not found: "Project 'test' not found. Available projects: [list]"
- If found: Asks about tasks and confirms deletion as above

## CLI Interface

**List all projects** (to find project ID):

```bash
todu project list --format json
```

Returns array of projects with id, name, description, etc.

**Remove project** (requires project ID from list command):

```bash
# Delete project only (keep tasks)
todu project remove <id> --force --format json

# Delete project and all associated tasks
todu project remove <id> --cascade --force --format json
```

**Flags:**

- `--cascade`: Delete all tasks associated with this project
- `--force`: Skip the CLI's built-in confirmation prompt (we handle
  confirmation ourselves)
- `--format json`: Output in JSON format for parsing

**Example:**

```bash
# Delete project with ID 22 and all its tasks
todu project remove 22 --cascade --force --format json
```

**Output format**: The CLI outputs confirmation text. Parse output to verify
success.

## Task Deletion Behavior

The `--cascade` flag controls what happens to tasks associated with the project:

- **Without --cascade**: Only the project is deleted. Associated tasks remain
  in the database but become orphaned (no project association).

- **With --cascade**: Both the project and all its associated tasks are deleted
  from the database.

**Important**: Always ask the user which behavior they want using
AskUserQuestion before deleting.

## Confirmation Flow

**CRITICAL**: Use AskUserQuestion twice - first for task handling, then for
final confirmation:

### Step 1: Ask about task handling

```python
AskUserQuestion(
    questions=[{
        "question": f"What should happen to tasks associated with '{name}'?",
        "header": "Task Handling",
        "multiSelect": false,
        "options": [
            {
                "label": "Delete project and tasks",
                "description": "Remove project and all associated tasks (--cascade)"
            },
            {
                "label": "Delete project only",
                "description": "Keep tasks, only remove project"
            }
        ]
    }]
)
```

### Step 2: Final confirmation

```python
# Adjust message based on cascade choice
if cascade:
    task_msg = "This will also delete all associated tasks."
else:
    task_msg = "Associated tasks will be kept."

AskUserQuestion(
    questions=[{
        "question": f"Are you sure you want to delete the '{name}' project? {task_msg}",
        "header": "Confirm Delete",
        "multiSelect": false,
        "options": [
            {
                "label": "Yes, delete",
                "description": "Permanently remove this project"
            },
            {
                "label": "No, cancel",
                "description": "Keep the project"
            }
        ]
    }]
)
```

Only proceed with deletion if user selects "Yes, delete".

## Search Patterns

Natural language queries the skill should understand:

- "delete project [name]" → delete specific project
- "remove [name]" → delete specific project
- "unregister [name]" → delete specific project
- "delete the [name] project" → delete specific project
- "get rid of [name]" → delete specific project

## Error Handling

- **Project not found**: List available projects and suggest correct name
- **No projects registered**: Inform user no projects are registered
- **Delete failed**: Parse CLI error output and show message
- **CLI errors**: Check exit code and parse error output

## Notes

- Deletion is permanent - project must be re-registered if needed
- Must use project ID (not name) for the remove command
- Always use `--force` flag to skip CLI's built-in confirmation (we handle
  confirmation ourselves with AskUserQuestion)
- The `--cascade` flag determines whether associated tasks are also deleted
- Does not affect the actual repository/project, only the database
- Two-step confirmation: task handling choice + final confirmation
- User can cancel at any point (task handling or final confirmation)
- Without `--cascade`, tasks become orphaned but remain in the database
