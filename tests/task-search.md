# Task Search Skill Test

Test the task-search skill with these prompts:

## Test 1: Search all tasks (default status filtering)

```text
show me all my tasks
```

Expected: List tasks with status "inprogress" AND "active" (two queries combined)
across all projects, grouped by project, showing unified ID (#33 format), title,
status, priority, and labels

## Test 2: Filter by project (default status filtering)

```text
list tasks in todu-tests
```

Expected: Show tasks with status "inprogress" AND "active" (two queries combined)
from todu-tests project only. No grouping needed since single project

## Test 3: Filter by status (explicit active)

```text
show open tasks
```

Expected: List only active/open tasks (single query, status explicitly specified)
across all projects, grouped by project

## Test 4: Filter by status (explicit done)

```text
show completed tasks
```

Expected: List only done/completed tasks (single query, status explicitly
specified) across all projects

## Test 5: Filter by priority (default status filtering)

```text
show high priority tasks
```

Expected: List tasks with priority=high and status "inprogress" AND "active"
(two queries combined)

## Test 6: Filter by label (default status filtering)

```text
show bugs
```

Expected: List tasks with "bug" label and status "inprogress" AND "active"
(two queries combined)

## Test 7: Multiple filters (default status filtering)

```text
show high priority bugs in todu-tests
```

Expected: Combine project=todu-tests, priority=high, label=bug filters with
status "inprogress" AND "active" (two queries combined)

## Test 8: Search text (default status filtering)

```text
find tasks about testing
```

Expected: Full-text search for "testing" in title/description with status
"inprogress" AND "active" (two queries combined)

## Test 9: Empty results

```text
show tasks with label nonexistent
```

Expected: Display "No tasks found matching your criteria."

## Test 10: All projects overview (default status filtering)

```text
list all tasks
```

Expected: Similar to Test 1, show tasks with status "inprogress" AND "active"
(two queries combined) across all projects, grouped by project

## Test 11: Filter by assignee (default status filtering)

```text
show tasks assigned to alice
```

Expected: List tasks where assignee includes "alice" with status "inprogress"
AND "active" (two queries combined)

## Test 12: Multiple labels (default status filtering)

```text
show tasks with labels testing and sample
```

Expected: List tasks that have both "testing" and "sample" labels with status
"inprogress" AND "active" (two queries combined)
