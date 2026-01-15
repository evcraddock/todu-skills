---
name: task-comment-create
description: Add comments to tasks. Use when user says "add comment to task #*", "comment on #*", "add note to task *", or similar. (plugin:todu)
allowed-tools: todu
---

# Add Comment to Task

Adds comments to tasks using `todu task comment`.

## Examples

### Comment text provided

**User**: "Comment on task 214 saying 'Fixed in PR #42'"

Runs: `todu task comment 214 -m "Fixed in PR #42" --format json`

### Comment text not provided

**User**: "Add a comment to task 215"

1. Summarize the preceding activity on the task from the conversation
2. Runs `todu task comment 215 -m "<summary of activity>" --format json`

## CLI Commands

```bash
todu task comment <id> -m "Comment text" --format json
```

## Special Character Handling

| Character | Handling                          |
|-----------|-----------------------------------|
| `"`       | Use single quotes for outer       |
| `'`       | Use double quotes for outer       |
| `$`       | Escape as `\$`                    |

## Notes

- If comment text not provided, summarize preceding activity on the task from conversation
- Comments must be valid markdown
- Comments should be professional and detailed
- No confirmation needed - just add and show result
