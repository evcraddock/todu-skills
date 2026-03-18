---
name: task-create
description: Create tasks/issues. Use when user says "create a task", "create an issue", "new task", "add task to *", "create bug", "add bug", "new bug", or similar. (plugin:todu)
allowed-tools: todu
---

# Create Task

Creates tasks using `todu task create`.

## Examples

### Full details

**User**: "Create a high priority task in todu-skills: Fix authentication bug"

Runs: `todu task create --project todu-skills --title "Fix authentication bug" --priority high --format json`

### No project specified

**User**: "Create a task: Update documentation"

1. If the current repository clearly maps to a todu project, reuse it
2. Otherwise ask the user to choose from `todu project list --format json`
3. Runs: `todu task create --project <project> --title "Update documentation" --format json`

### Bug with reproduction steps

**User**: "Create a bug in todu.sh: Login fails on mobile"

Runs: `todu task create --project todu.sh --title "Login fails on mobile" --label bug --description "<detailed reproduction steps>" --format json`

## CLI Commands

```bash
# List projects when a project is not specified

todu project list --format json

# Create task

todu task create \
  --project <name> \
  --title <title> \
  --format json

# Optional flags
--description <text>
--priority <low|medium|high>
--label <label>
--due <YYYY-MM-DD>
--scheduled <YYYY-MM-DD>
```

## Notes

- If the project is specified, use it directly
- If no project is specified, infer it from the current repo when possible; otherwise ask the user
- Parse as much as possible from the user request to minimize prompts
- Description must be valid markdown
- Descriptions should be professional with detailed requirements
- **Bugs**: Include detailed reproduction steps in the description (steps to reproduce, expected behavior, actual behavior)
- Labels are repeatable flags
