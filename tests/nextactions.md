# Next Actions Skill Test

Test the nextactions skill with these prompts:

## Test 1: Basic next actions

```text
what's next?
```

Expected: List high priority tasks with status "inprogress" or "active" across
all projects (should show task #54 from setup)

## Test 2: Next actions query variant

```text
what are my next actions?
```

Expected: Same as Test 1 - show high priority inprogress/active tasks

## Test 3: Next actions for specific project

```text
next actions for todu-tests
```

Expected: List high priority inprogress/active tasks only from todu-tests
project (should show task #54)

## Test 4: What to work on next

```text
what should I work on next?
```

Expected: Same as Test 1 - show high priority inprogress/active tasks

## Test 5: Next action (singular)

```text
what is my next action?
```

Expected: Same as Test 1 - show high priority inprogress/active tasks

## Test 6: Invalid project handling

```text
next actions for nonexistent-project
```

Expected: Display error message about project not found (CLI handles gracefully)

## Test 7: Combined status check - active status

Create an inprogress high priority task first, then run:

```text
what's next?
```

Expected: Should show tasks from BOTH "inprogress" and "active" statuses,
filtered by high priority (both task #54 and the new inprogress task)

## Test 8: Filter excludes medium/low priority

Task #55 is medium priority. Running next actions should NOT show it:

```text
what's next?
```

Expected: Only show task #54 (high priority), not task #55 (medium priority)
