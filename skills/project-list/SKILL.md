---
name: project-list
description: List registered projects. Use when user says "list projects", "show projects", "what projects", or similar. (plugin:todu)
allowed-tools: todu
---

# List Registered Projects

Lists projects using `todu project list`.

**Default**: Show active projects unless the user asks for a different status.

## CLI Commands

```bash
# Default

todu project list --status active

# Show done projects

todu project list --status done

# Show canceled projects

todu project list --status canceled

# Show all projects (no filters)

todu project list
```

## Examples

- "show my projects" → `--status active`
- "show all my projects" → no filters
- "show done projects" → `--status done`
- "show canceled projects" → `--status canceled`

## Notes

- The current CLI filters projects by status only
- If the user asks for unsupported filtering such as provider or priority, list projects in JSON and filter the results after retrieval
