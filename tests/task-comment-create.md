# Task Comment Create Skill Tests

## Test 1: Add comment with body included

User request:

```text
Comment on task 48 saying "This is a test comment"
```

Expected behavior:

- Parse ID=48, body="This is a test comment"
- Lint markdown before posting
- Execute only after lint passes:
  - `todu task comment 48 -m "This is a test comment" --format json`
- Display confirmation with comment body

## Test 2: Add comment with inferred body

User request:

```text
Add a comment to task 49
```

Expected behavior:

- Parse ID=49, body=null
- Summarize preceding task activity from conversation
- Format summary as markdown
- Lint markdown before CLI call
- Execute CLI command with summary text
- Display confirmation

## Test 3: Multi-line markdown comment input

User request:

```text
Comment on task 48 with:
### Progress update

- Finished parser cleanup
- Added tests for edge cases
- Verified lint passes
```

Expected behavior:

- Parse ID=48 with multi-line markdown body
- Preserve markdown structure (do not flatten to one line)
- Validate markdown with markdownlint-cli2 before CLI call
- Execute with multi-line `-m` value
- Display confirmation

## Test 4: Lint fails

User request:

```text
Comment on task 48 with malformed markdown
```

Expected behavior:

- Attempt markdown validation first
- If lint fails, do not run `todu task comment`
- Return lint errors and request/derive corrected text
- Re-run lint; only execute CLI after lint passes

## Test 5: Task not found

User request:

```text
Comment on task 99999 saying "This should fail"
```

Expected behavior:

- Lint comment markdown first
- Attempt to add comment to non-existent task
- Display error from CLI
- Handle gracefully
