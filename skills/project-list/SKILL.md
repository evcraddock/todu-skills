---
name: project-list
description: List registered projects. Use when user says "list projects", "show projects", "what projects", or similar. (plugin:todu)
allowed-tools: todu
---

# List Registered Projects

Lists projects using `todu project list`.

**Default**: Active status with high or medium priority (unless user specifies otherwise).

## CLI Commands

```bash
# Default (active, high/medium priority)
todu project list --status active --priority high,medium

# All active projects
todu project list --status active

# Filter by system
todu project list --system github --status active

# Filter by specific priority
todu project list --priority high --status active

# Show done projects
todu project list --status done

# Show all projects (no filters)
todu project list
```

## Examples

- "show my projects" → `--status active --priority high,medium`
- "show all my projects" → no filters
- "show my github projects" → `--system github --status active`
- "show high priority projects" → `--priority high --status active`
- "show done projects" → `--status done`
