---
name: project-update
description: MANDATORY skill for updating registered projects. NEVER call `todu project update` directly - ALWAYS use this skill via the Skill tool. Use when user says "update project *", "modify project *", "change project *", "update * project", "rename project *", or similar queries to update a project. (plugin:core@todu)
allowed-tools: todu
---

# Update Registered Project

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY update
project request.**

**NEVER EVER call `todu project update` directly. This skill provides essential
logic beyond just running the CLI:**

- Showing current project details
- Parsing direct updates from user request when provided
- Using AskUserQuestion to let user select fields when not specified
- Collecting new values for selected fields
- Validating updates before applying
- Providing clear feedback about changes

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new update request.

---

This skill updates fields of a registered project in the todu database using
the `todu project update` CLI command.

## When to Use

- User explicitly mentions updating/modifying/changing a project
- User says "update project [name]"
- User wants to fix incorrect project information
- User wants to rename a project
- User wants to change description, status, or priority
- User wants to modify sync strategy

**Note**: System and external_id cannot be changed. If user needs to change
these, suggest deleting and re-adding the project.

## What This Skill Does

1. **Identify Project**
   - Extract the project name from user's request
   - If not provided, run `todu project list --format json` and ask which to
     update

2. **Parse Direct Updates (if provided)**
   - Check if user's request includes specific updates (e.g., "rename X to Y",
     "mark X as done", "set priority high on X")
   - If updates are clear from request, skip field selection and go to step 5
   - If updates are ambiguous, proceed to step 3

3. **Load Current Project Details**
   - Run `todu project list --format json` to get all projects
   - Find the project by name (case-insensitive search)
   - Extract the project `id` (needed for update command)
   - Display current project details to user

4. **Select Fields to Update** (only if not parsed from request)
   - Use AskUserQuestion to ask which fields to update
   - Options: "Name", "Description", "Status", "Priority", "Sync Strategy"
   - Allow multiSelect: true (user can update multiple fields at once)
   - **Note**: System and external_id are not updatable
   - For each selected field, collect the new value

5. **Confirm and Apply Update**
   - Show summary of changes (old value → new value)
   - Confirm with user before applying
   - Call `todu project update <id>` with appropriate flags
   - Parse output to confirm success
   - Display success message with updated details

## Example Interactions

### Example 1: Direct update from request

**User**: "Rename todu-tests to my-tests"
**Skill**:

- Parses request: project="todu-tests", update name to "my-tests"
- Runs `todu project list --format json` to find 'todu-tests' and get ID
- Finds project with id=1
- Shows confirmation:

  ```text
  Changes to apply:
  - name: todu-tests → my-tests
  ```

- Asks: "Apply these changes?" (Yes/Cancel)
- If confirmed: Calls `todu project update 1 --name my-tests`
- Shows: "Project 'my-tests' updated successfully."

### Example 2: Multiple direct updates

**User**: "Mark todu-tests as done and set priority to low"
**Skill**:

- Parses request: project="todu-tests", status=done, priority=low
- Runs `todu project list --format json` to find 'todu-tests'
- Finds project with id=1
- Shows confirmation:

  ```text
  Changes to apply:
  - status: active → done
  - priority: medium → low
  ```

- If confirmed: Calls `todu project update 1 --status done --priority low`
- Shows: "Project 'todu-tests' updated successfully."

### Example 3: Interactive field selection

**User**: "Update the todu-tests project"
**Skill**:

- Runs `todu project list --format json` to find 'todu-tests'
- Finds project with id=1, name="todu-tests"
- Shows current details:

  ```text
  Current project details:
  - Name: todu-tests
  - Description: Test project for todu-skills development and testing
  - Status: active
  - Priority: medium
  - Sync Strategy: bidirectional
  - System: forgejo (cannot be changed)
  - External ID: f7b6d301-a9e5-48ca-b5c2-5c0ac5561765 (cannot be changed)
  ```

- Uses AskUserQuestion with question "Which fields would you like to update?"
  and header "Select Fields" with multiSelect enabled and options:
  - "Name" - Current: todu-tests
  - "Description" - Current: Test project for todu-skills...
  - "Status" - Current: active (active/done/cancelled)
  - "Priority" - Current: medium (low/medium/high)
  - "Sync Strategy" - Current: bidirectional (pull/push/bidirectional)
- User selects: "Description"
- Asks: "What is the new description?"
- User provides: "Updated test project description"
- Shows confirmation:

  ```text
  Changes to apply:
  - description: Test project for todu-skills... → Updated test project description
  ```

- Asks: "Apply these changes?" (Yes/Cancel)
- If confirmed: Calls `todu project update 1 --description "Updated test
  project description"`
- Shows: "Project 'todu-tests' updated successfully."

## CLI Interface

**List all projects** (to find project ID and current values):

```bash
todu project list --format json
```

Returns array of projects:

```json
[
  {
    "id": 1,
    "name": "todu-tests",
    "description": "Test project for todu-skills development and testing",
    "system_id": 1,
    "external_id": "f7b6d301-a9e5-48ca-b5c2-5c0ac5561765",
    "status": "active",
    "priority": "medium",
    "sync_strategy": "bidirectional",
    "created_at": "2025-11-19T19:53:12.72737Z",
    "updated_at": "2025-11-19T19:53:12.72737Z"
  }
]
```

**Update project** (requires project ID from list command):

```bash
todu project update <id> \
  [--name <new-name>] \
  [--description <description>] \
  [--status <active|done|cancelled>] \
  [--priority <low|medium|high>] \
  [--sync-strategy <pull|push|bidirectional>]
```

Example:

```bash
# Update description
todu project update 1 --description "New description"

# Update multiple fields
todu project update 1 --name new-name --status done --priority high

# Update priority only
todu project update 1 --priority low
```

**Success output:**

```text
Project 'my-tests' updated successfully.
```

**Limitations**:

- Cannot update `system_id` (the system type like github/forgejo)
- Cannot update `external_id` (the repo or external identifier)
- To change system or external_id, user must delete and re-add the project

## Updateable Fields

| Field         | Flag              | Valid Values                    |
|---------------|-------------------|---------------------------------|
| Name          | `--name`          | Any unique string               |
| Description   | `--description`   | Any text                        |
| Status        | `--status`        | active, done, cancelled         |
| Priority      | `--priority`      | low, medium, high               |
| Sync Strategy | `--sync-strategy` | pull, push, bidirectional       |

**Not updateable**: system_id, external_id (suggest delete + re-add)

## Direct Update Parsing

When user provides updates in their request, parse directly:

| User says                          | Parsed update                |
|------------------------------------|------------------------------|
| "rename X to Y"                    | name = Y                     |
| "change name to Y"                 | name = Y                     |
| "mark X as done"                   | status = done                |
| "cancel X"                         | status = cancelled           |
| "set priority high on X"           | priority = high              |
| "make X high priority"             | priority = high              |
| "set X to low priority"            | priority = low               |
| "change X description to Y"        | description = Y              |
| "set sync strategy to pull"        | sync_strategy = pull         |

If the update is clear, skip field selection and go straight to confirmation.

## Search Patterns

Natural language queries the skill should understand:

- "update project [name]" → interactive field selection
- "modify [name]" → interactive field selection
- "change [name] description" → update description field
- "rename [name] to [new-name]" → update name field directly
- "fix the [name] project" → interactive field selection
- "mark [name] as done" → update status to done directly
- "cancel [name]" → update status to cancelled directly
- "change [name] sync strategy" → update sync_strategy field
- "set [name] priority to high" → update priority directly
- "make [name] low priority" → update priority directly

## Error Handling

- **Project not found**: List available projects and suggest correct name
- **No changes specified**: Inform user no updates were selected
- **Invalid values**: Show validation error and ask again
- **Duplicate name**: If renaming, check new name doesn't already exist
- **Update failed**: Parse CLI error output and show message
- **CLI errors**: Check exit code and parse error output
- **Cannot update system/external_id**: Inform user these fields cannot be
  changed and suggest delete + re-add workflow

## Notes

- Updates preserve the original `created_at` timestamp
- The `updated_at` timestamp is automatically updated
- User can update multiple fields in one operation (multiSelect)
- Confirmation is required before applying changes
- User can always cancel during field selection or confirmation
- Must use project ID (not name) for the update command
- Status values: active, done, cancelled
- Priority values: low, medium, high
- Sync strategy values: pull, push, bidirectional
- System and external_id cannot be updated via this skill
- Parse direct updates from user request to skip unnecessary prompts
