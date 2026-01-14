---
name: core-task-comment-create
description: MANDATORY skill for adding comments to tasks/issues. NEVER call comment scripts directly - ALWAYS use this skill via the Skill tool. Use when user says "add comment to task #*", "comment on #*", "add comment on task *", "add a comment to #*", "add note to task *", or similar queries to add a comment. (plugin:core@todu)
allowed-tools: todu
---

# Add Comment to Task/Issue

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY comment
request.**

**This skill provides essential logic beyond just running the CLI:**

- Parsing task ID from natural language requests
- Extracting comment body from user input
- Prompting for comment body if not provided
- Verifying task exists and showing task title before adding
- Supporting multi-line comments with markdown

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new comment request.

---

This skill adds comments to tasks/issues using the `todu task comment` CLI
command.

## When to Use

- User wants to add a comment to a task/issue
- User says "comment on issue X"
- User says "add note to task Y"
- User provides comment with task identifier

## What This Skill Does

1. **Parse Comment Request**
   - Extract task ID from user message
   - Extract comment body if provided in request
   - If no task ID, ask user which task to comment on
   - If no body, prompt user for comment text

2. **Verify Task and Show Context**
   - Run `todu task show <id> --format json` to verify task exists
   - Display task title so user confirms they're commenting on the right task
   - Example: "Adding comment to task #214: Fix authentication bug"

3. **Get Comment Body** (if not provided)
   - Prompt user for comment text
   - Mention that markdown is supported
   - Can be multi-line

4. **Build and Execute CLI Command**
   - Build: `todu task comment <id> -m "<body>" --format json`
   - Handle special characters in comment body (escape quotes)
   - Execute command and parse JSON output

5. **Display Result**
   - Show that comment was added
   - Display comment body
   - Show task information

## Example Interactions

### Example 1: Comment with body included

**User**: "Comment on task 214 saying 'Fixed in PR #42'"

**Skill**:

1. Parses: ID=214, body="Fixed in PR #42"
2. Runs: `todu task show 214 --format json` → title="Fix authentication bug"
3. Shows: "Adding comment to task #214: Fix authentication bug"
4. Executes: `todu task comment 214 -m "Fixed in PR #42" --format json`
5. Shows:

   ```text
   Added comment to task #214

   Comment:
     Fixed in PR #42
   ```

### Example 2: Comment without body

**User**: "Add a comment to task 215"

**Skill**:

1. Parses: ID=215, body=null
2. Runs: `todu task show 215 --format json` → title="Update documentation"
3. Shows: "Adding comment to task #215: Update documentation"
4. Asks user: "What would you like to say? (Markdown supported)"
5. User enters: "Tested the fix and it works well."
6. Executes: `todu task comment 215 -m "Tested the fix and it works well."
   --format json`
7. Shows confirmation

### Example 3: No task ID provided

**User**: "Add a comment"

**Skill**:

1. Parses: ID=null, body=null
2. Asks user: "Which task would you like to comment on? Please provide the
   task ID."
3. User provides: "214"
4. Continues with task verification and comment flow

### Example 4: Multi-line comment with markdown

**User**: "Comment on task 220: this is still happening in production"

**Skill**:

1. Parses: ID=220, body="this is still happening in production"
2. Runs: `todu task show 220 --format json` → title="Production bug"
3. Shows: "Adding comment to task #220: Production bug"
4. Executes: `todu task comment 220 -m "this is still happening in production"
   --format json`
5. Shows confirmation

## Natural Language Parsing

The skill understands these patterns:

- "comment on task 214 saying 'text here'"
- "add comment to task 215: text here"
- "comment on task 220 with 'text'"
- "note on task 214: text here"
- "add note to task #42 saying text"

Extract the task ID (numeric) and the comment body from the user's request.

## CLI Command Reference

**Verify task exists:**

```bash
todu task show <id> --format json
```

**Add comment with -m flag (preferred):**

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

## Special Character Handling

When building the CLI command, handle special characters in the comment body:

| Character | Handling                                      |
|-----------|-----------------------------------------------|
| `"`       | Escape as `\"` or use single quotes for outer |
| `'`       | Escape as `\'` or use double quotes for outer |
| `` ` ``   | Safe inside double quotes                     |
| `$`       | Escape as `\$` to prevent variable expansion  |
| `\`       | Escape as `\\`                                |

**Example with quotes:**

```bash
# Comment contains double quotes
todu task comment 214 -m 'User said "it works"' --format json

# Comment contains single quotes
todu task comment 214 -m "It's working now" --format json
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

## Display Formatting

After successfully adding a comment, display:

```text
Added comment to task #<id>

Comment:
  <comment body>
```

Keep it simple and concise. No need to display full JSON output to user.

## Error Handling

- **Task not found**: "Task #X not found. Please check the task ID."
- **Empty comment**: "Comment body cannot be empty. Please provide a comment."
- **No task ID**: Ask user which task to comment on
- **API errors**: Display error details from CLI output
- **Network errors**: Show error and suggest retry

## Notes

- Always use `--format json` for parsing CLI output
- The task ID must be numeric (the unified todu ID)
- Use `-m` flag for cleaner command construction, especially for multi-line
- Verify task exists before adding comment to show context
- Markdown in comment body is preserved by the CLI
- Comment body cannot be empty
- No confirmation needed before adding - just add and show result
