# Task Create Skill Test

Test the task-create skill with these prompts:

## Test 1: Create task with just title

```text
create a task in todu-tests
```

Expected: Ask for title, ask about optional fields, user declines, create
with just title

## Test 2: Create task with all fields

```text
create a new task
```

Expected: Ask which project, ask for title, ask about optional fields, user
accepts, gather all optional fields, create with all fields

## Test 3: Project not specified

```text
create a task
```

Expected: List all projects and ask user to select which one

## Test 4: Create task with description only

```text
create a task in todu-tests with description
```

Expected: Ask for title, ask about optional fields, gather description,
create task

## Test 5: Create task with priority

```text
create a high priority task
```

Expected: Ask which project, ask for title, gather priority, create task

## Test 6: Create task with labels

```text
create a task with labels bug and feature
```

Expected: Ask which project, ask for title, gather labels, create task

## Test 7: Create task with due date

```text
create a task due 2025-12-31
```

Expected: Ask which project, ask for title, gather due date, create task

## Test 8: Create task with assignees

```text
create a task assigned to alice
```

Expected: Ask which project, ask for title, gather assignees, create task

## Test 9: Error - no projects exist

```text
create a task
```

Expected: If no projects exist, inform user they need to register a project
first

## Test 10: Error - invalid date format

```text
create a task due tomorrow
```

Expected: Ask for due date in YYYY-MM-DD format if invalid format provided

## Test 11: Complex task with multiple fields

```text
create a task in todu-tests
```

Expected: Gather title, ask about optional fields, gather description,
priority (high), labels (feature, auth), due date (2025-12-31), assignees
(alice, bob)
