---
name: core-task-comment-create
description: MANDATORY skill for adding comments to tasks/issues. NEVER call comment scripts directly - ALWAYS use this skill via the Skill tool. Use when user says "add comment to task #*", "comment on #*", "add comment on task *", "add a comment to #*", "add note to task *", or similar queries to add a comment. (plugin:core@todu)
---

# Add Comment to Task/Issue

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY comment request.**

**This skill provides essential logic beyond just running the CLI:**

- Parsing task ID from natural language requests
- Extracting comment body from user input
- Prompting for comment body if not provided
- Supporting multi-line comments with markdown
- Displaying confirmation with comment preview

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new comment request.

---

This skill adds comments to tasks/issues using the `todu task comment` CLI command.

## When to Use

- User wants to add a comment to a task/issue
- User says "comment on issue X"
- User says "add note to task Y"
- User provides comment with task identifier

## What This Skill Does

1. **Parse Comment Request**
   - Extract task ID from user message
   - Extract comment body if provided in request
   - If no body, will prompt user

2. **Get Comment Body** (if not provided)
   - Prompt user for comment text
   - Can be multi-line
   - Support markdown formatting

3. **Build CLI Command**
   - Start with: `todu task comment <id>`
   - Add comment text using `-m` flag or as argument
   - For multi-line, use `-m` flag with quoted text
   - Use `--format json` for parsing output

4. **Execute and Parse**
   - Run the CLI command
   - Parse JSON output
   - Extract comment details

5. **Display Confirmation**
   - Show that comment was added
   - Display comment body
   - Show task information

## Example Interactions

### Example 1: Comment with Body Included

**User**: "Comment on task 214 saying 'Fixed in PR #42'"

**Skill**:

1. Parses: ID=214, body="Fixed in PR #42"
2. Executes: `todu task comment 214 -m "Fixed in PR #42" --format json`
3. Parses JSON output
4. Shows:

```text
✅ Added comment to task #214

Comment:
  Fixed in PR #42
```

### Example 2: Comment with Prompt

**User**: "Add a comment to task 215"

**Skill**:

1. Parses: ID=215, body=null
2. Uses AskUserQuestion tool to prompt for comment
3. User enters:

```text
Tested the fix and it works well.

Some notes:
- Performance is better
- No regressions found
- Ready to deploy
```

1. Executes: `todu task comment 215 -m "Tested the fix..." --format json`
2. Shows confirmation

### Example 3: Multi-line Comment

**User**: "Comment on task 220: this is still happening in production"

**Skill**:

1. Parses: ID=220, body="this is still happening in production"
2. Executes:
   `todu task comment 220 -m "this is still happening in production"
   --format json`
3. Shows confirmation

## Natural Language Parsing

The skill understands these patterns:

- "comment on task 214 saying 'text here'"
- "add comment to task 215: text here"
- "comment on task 220 with 'text'"
- "note on task 214: text here"
- "add note to task #42 saying text"

Extract the task ID (numeric) and the comment body from the user's request.

## CLI Command Reference

**Add comment with text as argument:**

```bash
todu task comment <id> "Comment text here" --format json
```

**Add comment with -m flag (preferred for multi-line):**

```bash
todu task comment <id> -m "Comment text here" --format json
```

**Multi-line comment example:**

```bash
todu task comment 214 -m "This is a multi-line comment.

It supports markdown:
- Bullet points
- **Bold text**
- Code blocks" --format json
```

## JSON Output Format

The CLI returns a comment object:

```json
{
  "id": 123,
  "task_id": 214,
  "body": "Comment text here",
  "author": "user",
  "created_at": "2025-11-19T10:00:00Z",
  "updated_at": "2025-11-19T10:00:00Z"
}
```

## Markdown Support

Comments support markdown formatting:

```markdown
**Bold text**
*Italic text*
- Bullet points
- More points

Code blocks:
\`\`\`python
def hello():
    print("world")
\`\`\`

Links: [text](url)
```

## Prompting for Comment Body

When comment body is not provided in the user request, use the
AskUserQuestion tool:

1. Ask user to provide the comment text
2. Mention that markdown is supported
3. User can provide multi-line text
4. Use the provided text with the CLI command

Alternatively, you can ask the user directly in your response to provide the
comment text.

## Error Handling

- **Task not found**: Display error message from CLI
- **Empty comment**: "Comment body cannot be empty. Please provide a
  comment."
- **API errors**: Display error details from CLI output
- **Network errors**: Show error and suggest retry

## Display Formatting

After successfully adding a comment, display:

```text
✅ Added comment to task #<id>

Comment:
  <comment body>
```

Keep it simple and concise. No need to display full JSON output to user.

## Notes

- Always use `--format json` for parsing CLI output
- The task ID must be numeric (the unified todu ID)
- Use `-m` flag for cleaner command construction, especially for multi-line
- Properly escape quotes in comment body when building command
- Markdown in comment body is preserved by the CLI
- Comment body cannot be empty

## Success Criteria

- ✅ Parse task ID from user request
- ✅ Extract comment body from user request
- ✅ Prompt for comment if not provided
- ✅ Build correct CLI command with `-m` flag
- ✅ Execute command and parse JSON response
- ✅ Display confirmation message
- ✅ Support multi-line comments
- ✅ Support markdown formatting
- ✅ Handle errors gracefully
