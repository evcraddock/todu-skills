---
name: project-register
description: Register a new project. Use when user says "register project *", "add project *", or similar. (plugin:todu)
allowed-tools: todu
---

# Register Project

Registers a project using `todu project create`. For external repositories,
create the project first and then attach an integration binding with
`todu integration add`.

## Process

1. Check existing projects via `todu project list --format json`
2. For external repositories, also check existing bindings via `todu integration list --format json`
3. Generate a project name from the repo or requested project name
4. Check for name conflicts
5. If there is a conflict, ask the user to choose an alternative
6. Create the project with `todu project create`
7. If this is an external repo, add the integration binding with `todu integration add`

## Examples

### External repo (GitHub/Forgejo)

**User**: "Register evcraddock/rott"

1. Checks project list and integration list → not found
2. Suggests project name: "rott" → no conflict
3. Runs: `todu project create --name rott --format json`
4. Runs: `todu integration add --provider github --project rott --target-kind repository --target evcraddock/rott --strategy bidirectional --format json`

### Name conflict

**User**: "Register owner/repo-name"

1. Suggests `repo-name` → already exists
2. Asks user: `repo-name-2` / `repo-name-owner` / Other
3. Creates the project with the chosen name
4. Adds the integration binding

### Local project

**User**: "Create a local project called shopping-list"

Runs: `todu project create --name shopping-list --format json`

## CLI Commands

```bash
# Check existing projects

todu project list --format json

# Check existing integrations

todu integration list --format json

# Create project

todu project create --name <project-name> --format json

# Attach external repository

todu integration add \
  --provider <provider> \
  --project <project-name> \
  --target-kind repository \
  --target <owner/repo> \
  --strategy bidirectional \
  --format json

# Optional flags for project creation
--priority <low|medium|high>
--description "text"
```

## Name Conflict Resolution

Ask the user with options such as:
- `{name}-2` - numbered suffix
- `{name}-{owner}` - include repo owner

## Notes

- Use `github` for GitHub repositories and `forgejo` for Forgejo repositories unless the user specifies a different provider
- Project names must be unique
- For repository integrations, use `--target-kind repository`
- Priority defaults to medium if not provided
