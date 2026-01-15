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

1. Runs `git remote -v` to try to determine project from repo name
2. If not found, gets default project from `todu config show`
3. If no default, asks user to select from `todu project list --format json`
4. Runs: `todu task create --project <project> --title "Update documentation" --format json`

### Bug with reproduction steps

**User**: "Create a bug in todu.sh: Login fails on mobile"

Runs: `todu task create --project todu.sh --title "Login fails on mobile" --label bug --description "<detailed reproduction steps>" --format json`

## CLI Commands

```bash
# Get default project
todu config show

# List projects (if no default)
todu project list --format json

# Create task
todu task create \
  --project <name> \
  --title <title> \
  --format json

# Optional flags
--description <text>
--priority <low|medium|high>
--status <active|waiting>
--label <label>
--assignee <user>
--due <YYYY-MM-DD>
```

## Notes

- If project specified, use it directly (no verification needed)
- If no project: try `git remote -v` first, then default from `todu config show`, then ask user
- Parse as much as possible from user request to minimize prompts
- Description must be valid markdown
- Descriptions should be professional with detailed requirements
- **Bugs**: Include detailed reproduction steps in description (steps to reproduce, expected behavior, actual behavior)
- Labels and assignees are repeatable flags
