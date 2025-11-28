---
name: project-delete
description: MANDATORY skill for deleting registered projects. NEVER call `todu project remove` directly - ALWAYS use this skill via the Skill tool. Use when user says "delete project *", "remove project *", "unregister project *", "delete * project", "remove *", or similar queries to delete a project. (plugin:core@todu)
allowed-tools: todu
---

# Delete Registered Project

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY delete
project request.**

**NEVER EVER call `todu project remove` directly. This skill provides essential
logic beyond just running the CLI:**

- Showing task count before deletion
- Single confirmation with cascade option
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

3. **Count Associated Tasks**
   - Run `todu task list --project <name> --format json` to count tasks
   - Display task count to user (e.g., "This project has 5 associated tasks")

4. **Confirm Deletion (Single Step)**
   - If project has NO tasks: simple yes/no confirmation
   - If project HAS tasks: ask about cascade in same confirmation
   - Use AskUserQuestion with appropriate options based on task count

5. **Delete Project**
   - If confirmed, call `todu project remove <id>` with appropriate flags
   - Use `--cascade` if user chose to delete tasks
   - Use `--force` to skip CLI's built-in confirmation (we already confirmed)
   - Display success message with deleted project details
   - If cancelled, inform user no changes were made

## Example Interactions

### Example 1: Project with tasks

**User**: "Delete the todu-tests project"
**Skill**:

- Runs `todu project list --format json` to find 'todu-tests'
- Finds project with id=22, name="todu-tests"
- Runs `todu task list --project todu-tests --format json` → 5 tasks found
- Shows project details:

  ```text
  Project to delete:
  - Name: todu-tests
  - Description: Test project for development
  - Status: active
  - Associated tasks: 5
  ```

- Single confirmation with cascade options:
  - Question: "Delete project 'todu-tests'? (5 associated tasks)"
  - Options:
    - "Delete project only" - Keep associated tasks (they become orphaned)
    - "Delete with tasks" - Remove project and all 5 tasks (--cascade)
    - "Cancel" - Keep the project
- User selects: "Delete with tasks"
- Calls `todu project remove 22 --cascade --force`
- Shows: "Project 'todu-tests' (ID: 22) deleted successfully with 5 tasks."

### Example 2: Project with no tasks

**User**: "Remove the empty-project"
**Skill**:

- Runs `todu project list --format json` to find 'empty-project'
- Finds project with id=15, name="empty-project"
- Runs `todu task list --project empty-project --format json` → 0 tasks
- Shows project details:

  ```text
  Project to delete:
  - Name: empty-project
  - Description: An empty test project
  - Status: active
  - Associated tasks: 0
  ```

- Simple confirmation (no cascade needed):
  - Question: "Delete project 'empty-project'?"
  - Options:
    - "Yes, delete" - Permanently remove this project
    - "Cancel" - Keep the project
- User selects: "Yes, delete"
- Calls `todu project remove 15 --force`
- Shows: "Project 'empty-project' (ID: 15) deleted successfully."

### Example 3: Project not found

**User**: "Delete the test project"
**Skill**:

- Runs `todu project list --format json` to find 'test'
- Not found: "Project 'test' not found. Available projects: todu-skills,
  todu-tests, my-project"

## CLI Interface

**List all projects** (to find project ID):

```bash
todu project list --format json
```

Returns array of projects with id, name, description, etc.

**Count associated tasks:**

```bash
todu task list --project <name> --format json
```

Returns array of tasks - count the results to show task count.

**Remove project** (requires project ID from list command):

```bash
# Delete project only (keep tasks - they become orphaned)
todu project remove <id> --force

# Delete project and all associated tasks
todu project remove <id> --cascade --force
```

**Flags:**

- `--cascade`: Delete all tasks associated with this project
- `--force`: Skip the CLI's built-in confirmation prompt (we handle
  confirmation ourselves)

**Example:**

```bash
# Delete project with ID 22 and all its tasks
todu project remove 22 --cascade --force
```

**Success output:**

```text
Project 'todu-tests' (ID: 22) deleted successfully.
```

## Confirmation Flow

**CRITICAL**: Use a SINGLE AskUserQuestion call. The options vary based on
task count:

### If project has tasks (count > 0)

Use AskUserQuestion with question "Delete project '{name}'? ({count} associated
tasks)" and header "Delete" with these options:

- **Delete project only**: Keep associated tasks (WARNING: tasks become
  orphaned with no project association - this is rarely useful)
- **Delete with tasks**: Remove project and all {count} tasks (--cascade)
- **Cancel**: Keep the project

### If project has no tasks (count = 0)

Use AskUserQuestion with question "Delete project '{name}'?" and header
"Delete" with these options:

- **Yes, delete**: Permanently remove this project
- **Cancel**: Keep the project

Only proceed with deletion if user selects a delete option (not "Cancel").

## Task Deletion Behavior

The `--cascade` flag controls what happens to tasks associated with the project:

- **Without --cascade**: Only the project is deleted. Associated tasks remain
  in the database but become orphaned (no project association). **WARNING**:
  Orphaned tasks are difficult to find and manage. This option is rarely
  useful - consider warning the user if they choose this.

- **With --cascade**: Both the project and all its associated tasks are deleted
  from the database. This is usually the preferred option when tasks exist.

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
- Single confirmation step that includes cascade choice when tasks exist
- Skip cascade question entirely when project has no tasks
- Warn users that "delete project only" leaves orphaned tasks (rarely useful)
