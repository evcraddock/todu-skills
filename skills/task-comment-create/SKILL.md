---
name: task-comment-create
description: Add comments to tasks. Use when user says "add comment to task #*", "comment on #*", "add note to task *", or similar. (plugin:todu)
allowed-tools: todu, Bash
---

# Add Comment to Task

Adds task updates using `todu note add --task`. The current CLI stores these
updates as notes attached to the task.

## Behavior

1. Parse the task ID and comment text from the user request.
2. If comment text is missing, summarize preceding task activity from the conversation.
3. Prefer clear markdown structure for non-trivial updates (short heading and bullets).
4. Validate markdown with `markdownlint-cli2` before posting.
5. Only run `todu note add --task` if lint exits with code 0.

## Examples

### Comment text provided

**User**: "Comment on task 214 saying 'Fixed in PR #42'"

1. Build comment markdown
2. Lint comment markdown
3. Run: `todu note add --task 214 "Fixed in PR #42" --format json`

### Comment text not provided

**User**: "Add a comment to task 215"

1. Summarize preceding activity from the conversation
2. Format as markdown (multi-line is allowed and preferred when useful)
3. Lint the markdown
4. Run: `todu note add --task 215 "<markdown summary>" --format json`

## CLI Command

```bash
todu note add --task <id> "Comment markdown" --format json
```

## Safe Multi-Line Command Pattern

Use a shell variable so markdown formatting is preserved:

```bash
COMMENT=$(cat <<'MD'
### Update summary

- Item one
- Item two
MD
)

todu note add --task <id> "$COMMENT" --format json
```

## Markdown Validation Gate (Required)

Before **every** `todu note add --task` command:

1. Normalize line endings to LF (`\n`).
2. Ensure the markdown ends with exactly one trailing newline.
3. Lint markdown from stdin with `markdownlint-cli2`.
4. If lint fails, fix content and lint again.
5. Post only after lint passes.

Use this lint command pattern:

```bash
cfg=$(mktemp --suffix=.markdownlint-cli2.jsonc)
printf '{"config":{"MD041":false,"MD013":false}}\n' > "$cfg"
printf '%s\n' "$COMMENT" | markdownlint-cli2 - --config "$cfg"
rm -f "$cfg"
```

## Notes

- Multi-line markdown is supported and preferred for substantial updates
- One-line comments are fine for small updates
- Keep comments professional and specific about what changed
- No confirmation needed; add the note and show the result
