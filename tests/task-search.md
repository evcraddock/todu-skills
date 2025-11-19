# Task Search Skill Test

Test the task-search skill with these prompts:

## Test 1: Search all tasks

```text
show me all my tasks
```

Expected: List all tasks grouped by project, showing unified ID (#33 format),
title, status, priority, and labels

## Test 2: Filter by project

```text
list tasks in todu-tests
```

Expected: Show only tasks from todu-tests project, no grouping needed since
single project

## Test 3: Filter by status (active)

```text
show open tasks
```

Expected: List only active/open tasks across all projects, grouped by project

## Test 4: Filter by status (done)

```text
show completed tasks
```

Expected: List only done/completed tasks across all projects

## Test 5: Filter by priority

```text
show high priority tasks
```

Expected: List only tasks with priority=high

## Test 6: Filter by label

```text
show bugs
```

Expected: List tasks with "bug" label

## Test 7: Multiple filters

```text
show high priority bugs in todu-tests
```

Expected: Combine project=todu-tests, priority=high, label=bug filters

## Test 8: Search text

```text
find tasks about testing
```

Expected: Full-text search for "testing" in title/description

## Test 9: Empty results

```text
show tasks with label nonexistent
```

Expected: Display "No tasks found matching your criteria."

## Test 10: All projects overview

```text
list all tasks
```

Expected: Similar to Test 1, show all tasks grouped by project

## Test 11: Filter by assignee

```text
show tasks assigned to alice
```

Expected: List tasks where assignee includes "alice"

## Test 12: Multiple labels

```text
show tasks with labels testing and sample
```

Expected: List tasks that have both "testing" and "sample" labels
