---
name: project-update
description: Update registered projects. Use when user says "update project *", "rename project *", "mark project * as done", or similar. (plugin:todu)
allowed-tools: todu
---

# Update Registered Project

Updates project fields using `todu project update`.

## Examples

### Direct update from request

**User**: "Rename todu-tests to my-tests"

1. Finds project ID via `todu project list --format json`
2. Confirms change: "name: todu-tests → my-tests"
3. Runs: `todu project update 1 --name my-tests`

### Multiple updates

**User**: "Mark todu-tests as done and set priority to low"

Runs: `todu project update 1 --status done --priority low`

### Interactive (no specific update given)

**User**: "Update the todu-tests project"

1. Shows current details
2. Asks which fields to update (multiSelect)
3. Collects new values
4. Confirms and applies

## CLI Commands

```bash
# Find project ID
todu project list --format json

# Update fields
todu project update <id> --name <new-name>
todu project update <id> --description "text"
todu project update <id> --status <active|done|cancelled>
todu project update <id> --priority <low|medium|high>
todu project update <id> --sync-strategy <pull|push|bidirectional>

# Multiple fields
todu project update <id> --name new-name --status done --priority high
```

## Updateable Fields

| Field         | Flag              | Valid Values                |
|---------------|-------------------|-----------------------------|
| Name          | `--name`          | Any unique string           |
| Description   | `--description`   | Any text                    |
| Status        | `--status`        | active, done, cancelled     |
| Priority      | `--priority`      | low, medium, high           |
| Sync Strategy | `--sync-strategy` | pull, push, bidirectional   |

**Not updateable**: system, external_id (delete and re-add instead)

## Notes

- Must use project ID (not name) for update command
- Parse updates from request to skip unnecessary prompts
