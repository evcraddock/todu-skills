---
name: project-check
description: Check if the current git repository is registered as a project. Use when user says "check project", "is this registered", "project status", "check if project exists", or similar. (plugin:todu)
allowed-tools: todu
---

# Check Project Registration

Checks whether the current directory's git repository is connected to a todu
project through an integration binding.

## Process

1. Run `git remote -v` to get the origin URL
2. Parse the URL to extract the provider and `owner/repo`
3. Run `todu integration list --format json`
4. Find an integration where `provider` and `targetRef` match the current repo
5. Run `todu project list --format json` to map the matching `projectId` to a project name
6. Report the registration state with project details

## URL Parsing

Extract `owner/repo` from common URL formats:

| Format | Example | Result |
|--------|---------|--------|
| SSH | `git@github.com:owner/repo.git` | github, owner/repo |
| HTTPS | `https://github.com/owner/repo.git` | github, owner/repo |
| Forgejo SSH | `git@git.example.com:owner/repo.git` | forgejo, owner/repo |
| Forgejo HTTPS | `https://git.example.com/owner/repo.git` | forgejo, owner/repo |

Strip the `.git` suffix if present.

## CLI Commands

```bash
# Get git remote

git remote -v

# Check integration bindings

todu integration list --format json

# Resolve project names

todu project list --format json
```

## Output Format

Report in this format:

```text
Registration: [Registered | Not Registered]
Project Name: <name> (if registered)
Provider: <github|forgejo|etc>
Repository: <owner/repo>
Integration ID: <id or ->
```

## Examples

### Registered project

```bash
$ git remote -v
origin  git@github.com:evcraddock/todu-skills.git (fetch)

$ todu integration list --format json
# Returns binding with provider "github" and targetRef "evcraddock/todu-skills"
```

Output:

```text
Registration: Registered
Project Name: todu-skills
Provider: github
Repository: evcraddock/todu-skills
Integration ID: ibind-12345678
```

### Unregistered project

```bash
$ git remote -v
origin  git@github.com:someuser/new-repo.git (fetch)

$ todu integration list --format json
# No matching targetRef
```

Output:

```text
Registration: Not Registered
Provider: github
Repository: someuser/new-repo
Integration ID: -
```

## Notes

- Use the `origin` remote by default
- Detect the provider from the hostname (`github.com` → `github`, common self-hosted git hosts → `forgejo` unless a different provider is obvious)
- If multiple integrations match, show all matching project names and ask the user which one they mean
