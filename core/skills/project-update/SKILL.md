---
name: project-update
description: MANDATORY skill for updating registered projects. NEVER call scripts/update-project.py directly - ALWAYS use this skill via the Skill tool. Use when user wants to update, modify, or change a project. (plugin:core@todu)
---

# Update Registered Project

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY update
project request.**

**NEVER EVER call `todu project update` directly. This skill provides essential
logic beyond just running the CLI:**

- Showing current project details
- Using AskUserQuestion to let user select which fields to update
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
- User wants to change description or status
- User wants to modify sync strategy

**Note**: System and external_id cannot be changed. If user needs to change
these, suggest deleting and re-adding the project.

## What This Skill Does

1. **Identify Project**
   - Extract the project name from user's request
   - If not provided, run `todu project list --format json` and ask which to update

2. **Load Current Project Details**
   - Run `todu project list --format json` to get all projects
   - Find the project by name (case-insensitive search)
   - Extract the project `id` (needed for update command)
   - Display current project details to user

3. **Select Fields to Update**
   - Use AskUserQuestion to ask which fields to update
   - Options: "Name", "Description", "Status" (active/done/cancelled),
    "Sync Strategy" (pull/push/bidirectional)
   - Allow multiSelect: true (user can update multiple fields at once)
   - **Note**: System and external_id are not updatable

4. **Collect New Values**
   - For each selected field, ask user for the new value
   - **Name**: Ask for new project name (text input)
   - **Description**: Ask for new description (text input)
   - **Status**: Use AskUserQuestion with options (active/done/cancelled)
   - **Sync Strategy**: Use AskUserQuestion with options (pull/push/bidirectional)

5. **Confirm and Apply Update**
   - Show summary of changes (old value -> new value)
   - Confirm with user before applying
   - Call `todu project update <id>` with appropriate flags
   - Parse JSON output with `--format json`
   - Display success message with updated details

## Example Interactions

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
  - Sync Strategy: bidirectional
  - System: forgejo (cannot be changed)
  - External ID: f7b6d301-a9e5-48ca-b5c2-5c0ac5561765 (cannot be changed)
  ```

- Uses AskUserQuestion:
  - Question: "Which fields would you like to update?"
  - Options: "Name", "Description", "Status", "Sync Strategy"
  - multiSelect: true
- User selects: "Description"
- Asks: "What is the new description?"
- User provides: "Updated test project description"
- Shows confirmation:

  ```text
  Changes to apply:
  - description: Test project for todu-skills development and testing
                 -> Updated test project description
  ```

- Asks: "Apply these changes?"
- If confirmed: Calls `todu project update 1 --description
  "Updated test project description" --format json`
- Shows: "✅ Project 'todu-tests' updated successfully."

**User**: "Rename todu-tests to my-tests and mark it done"
**Skill**:

- Runs `todu project list --format json` to find 'todu-tests'
- Finds project with id=1
- Shows current details
- Infers user wants to update name and status
- Asks for confirmation or uses AskUserQuestion if ambiguous
- Shows confirmation:

  ```text
  Changes to apply:
  - name: todu-tests -> my-tests
  - status: active -> done
  ```

- If confirmed: Calls `todu project update 1 --name my-tests
  --status done --format json`
- Shows: "✅ Project 'my-tests' updated successfully."

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
  [--sync-strategy <pull|push|bidirectional>] \
  --format json
```

Example:

```bash
# Update description
todu project update 1 --description "New description" --format json

# Update multiple fields
todu project update 1 --name new-name --status done --format json
```

**Output format**: The CLI outputs JSON when `--format json` is used. Parse
the output to confirm success and extract updated values.

**Limitations**:

- Cannot update `system_id` (the system type like github/forgejo)
- Cannot update `external_id` (the repo or external identifier)
- To change system or external_id, user must delete and re-add the project

## Field Selection Flow

**CRITICAL**: Use AskUserQuestion to let user choose fields:

```python
AskUserQuestion(
    questions=[{
        "question": "Which fields would you like to update?",
        "header": "Select Fields",
        "multiSelect": true,
        "options": [
            {
                "label": "Name",
                "description": f"Current: {current_name}"
            },
            {
                "label": "Description",
                "description": f"Current: {current_description or '(empty)'}"
            },
            {
                "label": "Status",
                "description": f"Current: {current_status} (active/done/cancelled)"
            },
            {
                "label": "Sync Strategy",
                "description": f"Current: {current_sync_strategy} (pull/push/bidirectional)"
            }
        ]
    }]
)
```

**Note**: System and external_id are not shown as options because they cannot
be updated.

## Value Collection

For each selected field:

**Name**: Ask user for new project name (text input via AskUserQuestion
"Other" option)

**Description**: Ask user for new description (text input via AskUserQuestion
"Other" option)

**Status**: Use AskUserQuestion with predefined options:

- active
- done
- cancelled

**Sync Strategy**: Use AskUserQuestion with predefined options:

- pull (only sync from external system to todu)
- push (only sync from todu to external system)
- bidirectional (sync both ways)

## Confirmation Flow

Before applying updates, show summary and confirm:

```text
Changes to apply:
- name: todu-tests -> my-tests
- status: active -> archived

Apply these changes? (yes/no)
```

Only proceed if user confirms.

## Search Patterns

Natural language queries the skill should understand:

- "update project [name]" → update specific project
- "modify [name]" → update specific project
- "change [name] description" → update description field
- "rename [name] to [new-name]" → update name field
- "fix the [name] project" → update any fields
- "mark [name] as done" → update status to done
- "cancel [name]" → update status to cancelled
- "change [name] sync strategy" → update sync_strategy field

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
- Sync strategy values: pull, push, bidirectional
- System and external_id cannot be updated via this skill
