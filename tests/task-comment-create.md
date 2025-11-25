# Task Comment Create Skill Tests

## Test 1: Add comment with body included

User request:

```text
Comment on task 48 saying "This is a test comment"
```

Expected behavior:

- Parse ID=48, body="This is a test comment"
- Execute: `todu task comment 48 -m "This is a test comment" --format json`
- Display confirmation with comment body

## Test 2: Add comment with prompt

User request:

```text
Add a comment to task 49
```

Expected behavior:

- Parse ID=49, body=null
- Prompt user for comment body
- Execute CLI command with provided text
- Display confirmation

## Test 3: Multi-line comment

User request:

```text
Comment on task 48: This is a multi-line comment with:
- Bullet points
- **Bold text**
- More details
```

Expected behavior:

- Parse ID=48 with multi-line body
- Execute with `-m` flag for multi-line
- Display confirmation

## Test 4: Task not found

User request:

```text
Comment on task 99999 saying "This should fail"
```

Expected behavior:

- Attempt to add comment to non-existent task
- Display error from CLI
- Handle gracefully
