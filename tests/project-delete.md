# Project Delete Skill Test

Test the project-delete skill with these prompts:

## Test 1: Delete project with cascade (delete tasks too)

```text
delete the test-github-repo project
```

Expected: Should ask about task handling, confirm deletion with cascade option

## Test 2: Delete project without cascade (keep tasks)

```text
remove the test-forgejo-repo project
```

Expected: Should ask if tasks should be deleted, allow choosing to keep tasks

## Test 3: Alternative phrasing - unregister

```text
unregister the todu-tests project
```

Expected: Should recognize "unregister" as delete request

## Test 4: Alternative phrasing - get rid of

```text
get rid of the todu-tests project
```

Expected: Should recognize "get rid of" as delete request

## Test 5: Cancel during task handling question

```text
delete the todu-tests project
```

Expected: User cancels when asked about task handling

## Test 6: Cancel during final confirmation

```text
delete the todu-tests project
```

Expected: User chooses task handling but cancels final confirmation

## Test 7: Error handling - non-existent project

```text
delete the nonexistent-project
```

Expected: Should list available projects and suggest correct name

## Test 8: Error handling - no projects

```text
delete a project
```

Expected: If no projects exist, inform user registry is empty

## Test 9: Show project details before deletion

```text
delete the todu-tests project
```

Expected: Should display full project details (name, description, status,
system, external_id)

## Test 10: Successful deletion with tasks

```text
delete the todu-tests project
```

Expected: Choose cascade, confirm, and verify success message

## Test 11: Successful deletion without tasks

```text
delete the todu-tests project
```

Expected: Choose no cascade, confirm, and verify success message
