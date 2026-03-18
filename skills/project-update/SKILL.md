---
name: project-update
description: Update registered projects. Use when user says "update project *", "rename project *", "mark project * as done", or similar. (plugin:todu)
allowed-tools: todu
---

# Update Registered Project

Updates project fields using `todu project update`. If the user asks to change a
repository sync strategy, update the integration binding with
`todu integration set-strategy`.

## Examples

### Direct update from request

**User**: "Rename todu-tests to my-tests"

1. Confirms change: "name: todu-tests → my-tests"
2. Runs: `todu project update todu-tests --name my-tests`

### Multiple updates

**User**: "Mark todu-tests as done and set priority to low"

Runs: `todu project update todu-tests --status done --priority low`

### Sync strategy update

**User**: "Set the todu-tests sync strategy to pull"

1. Runs `todu integration list --project todu-tests --format json`
2. Finds the matching integration binding
3. Runs: `todu integration set-strategy <integration-id> --strategy pull`

### Interactive (no specific update given)

**User**: "Update the todu-tests project"

1. Shows current details
2. Asks which fields to update
3. Collects new values
4. Confirms and applies

## CLI Commands

```bash
# Show current project

todu project show <ref> --format json

# Update project fields

todu project update <ref> --name <new-name>
todu project update <ref> --description "text"
todu project update <ref> --status <active|done|canceled>
todu project update <ref> --priority <low|medium|high>

# Update integration strategy when requested

todu integration list --project <ref> --format json
todu integration set-strategy <integration-id> --strategy <pull|push|bidirectional|none>

# Multiple project fields

todu project update <ref> --name new-name --status done --priority high
```

## Updatable Fields

| Field         | Command / Flag                                         | Valid Values                    |
|---------------|--------------------------------------------------------|---------------------------------|
| Name          | `todu project update --name`                           | Any unique string               |
| Description   | `todu project update --description`                    | Any text                        |
| Status        | `todu project update --status`                         | active, done, canceled          |
| Priority      | `todu project update --priority`                       | low, medium, high               |
| Sync Strategy | `todu integration set-strategy --strategy`             | pull, push, bidirectional, none |

## Notes

- The current CLI accepts a project name or ID as `<ref>`
- Parse updates from the user request to avoid unnecessary prompts
- If multiple integration bindings exist for the same project, ask the user which one to update
