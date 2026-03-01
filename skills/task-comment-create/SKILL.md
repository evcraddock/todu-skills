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

| Character | Handling |
|-----------|----------|
| `"` | Use single quotes for outer |
| `'` | Use double quotes for outer |
| `$` | Escape as `\$` |
| Newline chars (`LF`/`CRLF`) | Do not include in final comment text; replace with spaces |
| Literal escape tokens (`\\n`, `\\r`, `\\r\\n`, `\\N`) | Forbidden in final comment text; replace with spaces |

## Notes

- Comment text must be exactly one line in the `-m` value
- Before composing the command, normalize text: replace newline characters and literal escape tokens (`\\n`, `\\r`, `\\r\\n`, `\\N`) with spaces, collapse repeated whitespace, then trim
- Validate final `-m` value contains no newline characters and no literal `\\n`/`\\r`/`\\N`
- Ensure the normalized final `-m` value is still valid markdown (single-line markdown is fine; use inline markdown like `**bold**`, `_italic_`, ``code``, and links)
- If comment text not provided, summarize preceding activity on the task from conversation
- Comments should be professional and detailed
- No confirmation needed - just add and show result
