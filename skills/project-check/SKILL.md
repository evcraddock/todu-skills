---
name: project-check
description: Check if the current git repository is registered as a project. Use when user says "check project", "is this registered", "project status", "check if project exists", or similar. (plugin:todu)
allowed-tools: todu
---

# Check Project Registration

Checks if the current directory's git repository is registered in todu.

## Process

1. Run `git remote -v` to get the origin URL
2. Parse URL to extract git system and owner/repo
3. Check `todu project list --format json` for matching external-id
4. Report registration state with project details

## URL Parsing

Extract owner/repo from common URL formats:

| Format | Example | Result |
|--------|---------|--------|
| SSH | `git@github.com:owner/repo.git` | github, owner/repo |
| HTTPS | `https://github.com/owner/repo.git` | github, owner/repo |
| Forgejo SSH | `git@git.example.com:owner/repo.git` | forgejo, owner/repo |
| Forgejo HTTPS | `https://git.example.com/owner/repo.git` | forgejo, owner/repo |

Strip `.git` suffix if present.

## CLI Commands

```bash
# Get git remote
git remote -v

# Check registered projects
todu project list --format json
```

## Output Format

Report in this format:

```
Registration: [Registered | Not Registered]
Project Name: <nickname> (if registered)
Git System: <github|forgejo|etc>
Repository: <owner/repo>
```

## Examples

### Registered project

```bash
$ git remote -v
origin  git@github.com:evcraddock/todu-skills.git (fetch)

$ todu project list --format json
# Returns project with external_id "evcraddock/todu-skills"
```

Output:
```
Registration: Registered
Project Name: todu-skills
Git System: github
Repository: evcraddock/todu-skills
```

### Unregistered project

```bash
$ git remote -v
origin  git@github.com:someuser/new-repo.git (fetch)

$ todu project list --format json
# No matching external_id
```

Output:
```
Registration: Not Registered
Git System: github
Repository: someuser/new-repo
```

## Notes

- Uses origin remote by default
- Detects system from hostname (github.com → github, git.* → forgejo)
- Check `todu system list` for configured git systems if hostname doesn't match
