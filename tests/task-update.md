# Task Update Skill Test

Test the task-update skill with these prompts:

## Test 1: Close task

```text
mark task 39 as done
```

Expected: Execute `todu task close 39` and confirm task closed

## Test 2: Update status to waiting

```text
set task 39 to waiting
```

Expected: Execute `todu task update 39 --status waiting` and confirm status changed

## Test 3: Update status to active

```text
start working on task 39
```

Expected: Execute `todu task update 39 --status active` and confirm status changed

## Test 4: Set priority

```text
set priority high on task 39
```

Expected: Execute `todu task update 39 --priority high` and confirm priority changed

## Test 5: Add single label

```text
add label bug to task 39
```

Expected: Execute `todu task update 39 --add-label bug` and confirm label added

## Test 6: Add multiple labels

```text
add labels bug and enhancement to task 39
```

Expected: Execute `todu task update 39 --add-label bug --add-label enhancement`
and confirm both labels added

## Test 7: Remove label

```text
remove label testing from task 39
```

Expected: Execute `todu task update 39 --remove-label testing` and confirm
label removed

## Test 8: Assign to user

```text
assign task 39 to alice
```

Expected: Execute `todu task update 39 --add-assignee alice` and confirm
assignee added

## Test 9: Assign to multiple users

```text
assign task 39 to alice and bob
```

Expected: Execute `todu task update 39 --add-assignee alice --add-assignee bob`
and confirm both assignees added

## Test 10: Unassign user

```text
unassign alice from task 39
```

Expected: Execute `todu task update 39 --remove-assignee alice` and confirm
assignee removed

## Test 11: Update title

```text
rename task 39 to 'Updated task title'
```

Expected: Execute `todu task update 39 --title "Updated task title"` and
confirm title changed

## Test 12: Update description

```text
update description of task 39 to 'New description text'
```

Expected: Execute `todu task update 39 --description "New description text"`
and confirm description changed

## Test 13: Set due date

```text
set due date to 2025-12-31 on task 39
```

Expected: Execute `todu task update 39 --due 2025-12-31` and confirm due date set

## Test 14: Multiple updates

```text
set task 39 to active with high priority and add label bug
```

Expected: Execute `todu task update 39 --status active --priority high
--add-label bug` and confirm all changes

## Test 15: Close with natural language

```text
complete task 40
```

Expected: Execute `todu task close 40` and confirm task closed
